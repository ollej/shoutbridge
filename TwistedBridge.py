# -*- coding: utf-8 -*-

from twisted.internet import task
from twisted.internet import reactor
from twisted.names.srvconnect import SRVConnector
from twisted.words.xish import domish, xpath
from twisted.words.protocols.jabber import xmlstream, client, jid
import platform
from time import time
from datetime import datetime, date

from Shoutbox import *
from utilities import *
from XmppBridge import *

class XMPPClientConnector(SRVConnector):
    def __init__(self, reactor, domain, factory):
        SRVConnector.__init__(self, reactor, 'xmpp-client', domain, factory)

    def pickServer(self):
        host, port = SRVConnector.pickServer(self)

        if not self.servers and not self.orderedServers:
            # no SRV record, fall back..
            port = 5222

        return host, port

class TwistedBridge(XmppBridge):
    client_supported_features = ['jabber:iq:last', 'jabber:iq:version']
    login = ""
    passwd = ""
    room = ""
    host = ""
    port = 5222
    roomjid = ""
    resource = ""
    xmlstream = None
    last_time = 0

    def make_connection(self):
        """
        Make an XMPP connection and authorize the user.
        """
        self.jid = jid.JID(self.login)
        f = client.XMPPClientFactory(self.jid, self.passwd)
        f.addBootstrap(xmlstream.STREAM_CONNECTED_EVENT, self.connected)
        f.addBootstrap(xmlstream.STREAM_END_EVENT, self.disconnected)
        f.addBootstrap(xmlstream.STREAM_AUTHD_EVENT, self.authenticated)
        f.addBootstrap(xmlstream.INIT_FAILED_EVENT, self.init_failed)
        connector = XMPPClientConnector(reactor, self.jid.host, f)
        connector.connect()

    def close_connection(self):
        self.send_presence(type="unavailable", reason="Quitting...")
        self.xmlstream.sendFooter()

    def connected(self, xs):
        print 'Connected.'
        self.xmlstream = xs

        # Consider last activity time to be when connected.
        self.update_last_time()

        # Log all traffic
        xs.rawDataInFn = self.rawDataIn
        xs.rawDataOutFn = self.rawDataOut

        # Add Event observers
        xs.addObserver("/message[@type='groupchat']", self.handle_message)
        #xs.addObserver("/message[@type='chat']", self.handle_message)
        xs.addObserver("/presence", self.handle_presence)
        xs.addObserver("/iq", self.handle_iq)

    def disconnected(self, xs):
        print 'Disconnected.'
        #reactor.stop()

    def init_failed(self, failure):
        print "Initialization failed."
        print failure
        self.xmlstream.sendFooter()

    def send_stanza(self, stanza):
        if not self.xmlstream:
            self.logprint("Stanza not sent, no xml stream:\n", stanza.toXml())
            return False
        self.logprint("Sending stanza:\n", stanza.toXml())
        self.xmlstream.send(stanza)

    def handle_iq(self, iq):
        """
        Handles incoming IQ stanzas and dispatches to specific handle methods.
        """
        frm = iq.getAttribute('from')
        to = iq.getAttribute('to')
        id = iq.getAttribute('id')
        type = iq.getAttribute('type')
        self.lookup_iq_method(type)(frm=frm, to=to, id=id, query=iq.query)

    def handle_iq_GET(self, frm=None, to=None, id=None, query=None):
        if query.defaultUri == 'jabber:iq:last':
            self.send_iq_last(to=frm, id=id)
        elif query.defaultUri == 'jabber:iq:version':
            self.send_iq_version(to=frm, id=id)
        elif query.defaultUri == 'http://jabber.org/protocol/disco#info':
            self.handle_iq_DISCO(frm=frm, to=to, id=id, query=query)
        else:
            # Default to sending back error for unknown get iq.
            self.send_iq_error(to=frm, id=id, query=query)

    def send_iq_version(self, frm=None, to=None, id=None):
        """
        Returns iq stanza with client and system information.
        """
        querynode = domish.Element(('jabber:iq:version', 'query'))
        querynode.addElement('name', content=self.client_name)
        querynode.addElement('version', content=self.client_version)
        querynode.addElement('os', content=self.get_os_info())
        self.send_iq('result', id, to=to, children=[querynode])

    def send_iq_last(self, to=None, id=None):
        """
        Return IQ stanza with information on seconds since last client usage.
        """
        query = domish.Element(('jabber:iq:last', 'query'))
        query['seconds'] = self.get_last_activity()
        self.send_iq('result', id, to=to, children=[query])

    def send_iq_disco(self, frm=None, to=None, id=None, query=None):
        """
        Send IQ stanza with discovery information.
        """
        resultquery = domish.Element(('http://jabber.org/protocol/disco#info', 'query'))
        for f in self.client_supported_features:
            feature = domish.Element((None, 'feature'))
            feature['var'] = f
            resultquery.addChild(feature)
        self.send_iq("result", id, to=to, children=[resultquery])

    def send_iq_error(self, to=None, id=None, type=None, query=None, condition=None):
        """
        Build and send IQ error stanza.
        """
        errornode = domish.Element((None, 'error'))
        if not type:
            type = 'cancel'
        if type not in ['cancel', 'continue', 'modify', 'auth', 'wait']:
            raise BridgeWrongTypeError
        errornode['type'] = type
        if not condition:
            condition = 'feature-not-implemented'
        errornode.addElement(condition, defaultUri='urn:ietf:params:xml:ns:xmpp-stanzas')
        if reason:
            errornode.addElement('text', defaultUri='urn:ietf:params:xml:ns:xmpp-stanzas', content=reason)
        self.send_iq("error", id, to=to, children=[query, errornode])

    def send_iq(self, type, id, frm=None, to=None, children=None, querytype=None):
        """
        Sends an IQ stanza on the xml stream.
        """
        if type not in ['set', 'get', 'result', 'error']:
            raise BridgeWrongTypeError

        iq = domish.Element((None, 'iq'))
        iq['type'] = type
        if not frm:
            frm = self.login + '/' + self.current_nick
        iq['from'] = frm
        iq['id'] = id
        if to:
            iq['to'] = to
        if children:
            for child in children:
                iq.addChild(child)
        self.send_stanza(iq)

    def handle_presence(self, pres):
        if not pres:
            return False
        # Parse presence information.
        (login, sep, nick) = pres['from'].rpartition('/')
        fromjid = jid.JID(pres['from'])
        for x in pres.elements(('http://jabber.org/protocol/muc#user', 'x')):
            if x.item and x.item.hasAttribute('jid'):
                fromjid = jid.JID(x.item['jid'])
        fromstr = fromjid.user + '@' + fromjid.host

        # Call the proper presence handler.
        if pres.hasAttribute('type'):
            self.lookup_presence_method(pres['type'])(pres, fromjid=fromjid, fromstr=fromstr,
                                                      login=login, nick=nick)
        else:
            self.handle_presence_AVAILABLE(pres, fromstr=fromstr, nick=nick)

    def handle_presence_DEFAULT(self, pres, fromjid=None, **kwargs):
        print "Received unknown presence:", pres.toXml()

    def handle_presence_ERROR(self, pres, fromjid=None, **kwargs):
        print "Received error presence:", pres.toXml()
        if pres.error and pres.error.hasAttribute('code'):
            code = pres.error['code']
        if code == "409":
            # Nick taken, default to original nick.
            self.change_nick(self.resource)

    def send_presence(self, xmlns=None, type=None, status=None, show=None,
                     frm=None, to=None, children=None):
        """
        Build and send presence stanza.
        """
        presence = domish.Element((xmlns, 'presence'))
        if frm:
            presence['from'] = frm
        if to:
            presence['to'] = to
        if type:
            presence['type'] = type
        if status:
            presence.addElement('status', content=status)
        if show in ('chat', 'dnd', 'away', 'xa'):
            presence.addElement('show', content=show)
        if children:
            for k, v in children.items():
                presence.addElement(k, content=v)
        self.send_stanza(presence)

    def handle_message(self, mess):
        """
        Handle an XMPP message.
        """
        if mess.x and mess.x.defaultUri:
            # Check if message is delayed.
            if mess.x.defaultUri in ['jabber:x:delay', 'urn:xmpp:delay']:
                self.logprint("Skipping delayed message.")
                return

            # Ignore status message about anonymous room.
            if mess.x.defaultUri == 'http://jabber.org/protocol/muc#user':
                if mess.x.status and mess.x.status.getAttribute('code') == '100':
                    self.logprint("Anonymous room message, skipping.")
                    return

        fromstr = mess.getAttribute('from')
        fromjid = jid.JID(fromstr)

        # Groupchat messages have different from jid
        if mess['type'] == 'groupchat':
            (fromstr, sep, nick) = fromstr.rpartition('/')
        else:
            nick = fromjid.user + '@' + fromjid.host

        # Skip if message is sent by shoutbridge
        print "Nick is", nick
        fromuser = self.roster.get(nick)
        if fromuser and fromuser.name == self.login or nick == self.current_nick:
            self.logprint("Got message from myself, skipping...")
            return

        # Trigger handleXmppMessage event
        mess = self.trigger_plugin_event('XmppMessage', mess)

        # Get message body.
        body = getElStr(mess.body)

        # Send message.
        if body and mess['type'] in ['message', 'chat', 'groupchat', None]: 
            user = self.get_from_roster(nick, fromstr)
            self.logprint("Relaying message to shoutbox:", user.id, user.jid, user.name, "\n", body)
            self.update_last_time()
            self.shoutbox.sendShout(user, body)
        else:
            self.logprint("Unknown message:", mess.toXml())

    def send_message(self, tojid, text, nick=None):
        """
        Send an text as XMPP message to tojid
        """
        try:
            if nick:
                self.change_nick(nick)
            message = domish.Element((None, 'message'))
            message['to'] = tojid
            message['from'] = self.login + '/' + nick
            message['type'] = 'groupchat'
            message.addElement('body', content=text)
            self.update_last_time()
            self.send_stanza(message)
        except UnicodeDecodeError:
            print "Unicode Decode Error: ", text

    def listen(self):
        """
        Start listening on XMPP and Shoutbox, relaying messages.
        """
        try:
            # Send messages from shoutbox every few seconds
            l = task.LoopingCall(self.process_shoutbox_messages)
            l.start(float(self.cfg.loop_time))
            l2 = task.LoopingCall(self.ping)
            l2.start(60.0)
            # Start the reactor
            reactor.run()
        except KeyboardInterrupt:
            self.close_connection()
            print "Exiting..."

