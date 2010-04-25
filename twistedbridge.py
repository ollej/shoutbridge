# -*- coding: utf-8 -*-

from twisted.internet import task
from twisted.internet import reactor
from twisted.names.srvconnect import SRVConnector
from twisted.words.xish import domish, xpath
from twisted.words.protocols.jabber import xmlstream, client, jid
from shoutbox import *
from utilities import *
import platform
from time import time
from datetime import datetime, date

class BridgeError(Exception):
    "Unknown Bridge Error"

class BridgeConnectionError(BridgeError):
    "Could not connect to XMPP."

class BridgeAuthenticationError(BridgeError):
    "Could not authenticate."

class BridgeWrongTypeError(BridgeError):
    "Incorrect type."

class BridgeMissingAttributeError(BridgeError):
    "A required attribute is missing."

class BridgeNoXmlStream(BridgeError):
    "No active xml stream available."

class XMPPClientConnector(SRVConnector):
    def __init__(self, reactor, domain, factory):
        SRVConnector.__init__(self, reactor, 'xmpp-client', domain, factory)

    def pickServer(self):
        host, port = SRVConnector.pickServer(self)

        if not self.servers and not self.orderedServers:
            # no SRV record, fall back..
            port = 5222

        return host, port

class TwistedBridge(object):
    client_name = "Shoutbridge"
    client_version = "0.1"
    client_supported_features = ['jabber:iq:last', 'jabber:iq:version']
    login = ""
    passwd = ""
    room = ""
    host = ""
    port = 5222
    roomjid = ""
    resource = ""
    shoutbox = None
    xmlstream = None
    roster = dict()
    cfg = None
    current_nick = None
    last_time = 0

    def __init__(self, sbox, cfg):
        """
        Instantiate an XMPP bridge using XMPP login details and a shoutbox object.
        """
        # cfg.xmpp_login, cfg.xmpp_pass, cfg.xmpp_host, cfg.xmpp_port, cfg.xmpp_room
        self.shoutbox = sbox
        self.login = cfg.xmpp_login
        self.passwd = cfg.xmpp_pass
        self.host = cfg.xmpp_host
        self.port = cfg.xmpp_port
        (self.room, foo, self.resource) = cfg.xmpp_room.rpartition('/')
        self.roomjid = cfg.xmpp_room
        self.cfg = cfg
        self.current_nick = self.resource
        self.update_last_time()

        # Make an XMPP connection
        self.make_connection()

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

    def rawDataIn(self, buf):
        print "RECV: %s" % unicode(buf, 'utf-8')

    def rawDataOut(self, buf):
        print "SEND: %s" % unicode(buf, 'utf-8')

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

    def authenticated(self, xs):
        print "Authenticated."
        # Send initial presence
        #self.send_presence_status()

        # Connect to conference room
        self.join_room(self.roomjid)

    def init_failed(self, failure):
        print "Initialization failed."
        print failure
        self.xmlstream.sendFooter()

    def join_room(self, room):
        self.send_presence(
            frm=self.login + '/' + self.cfg.xmpp_resource,
            to=room,
            children=dict(
                x=u'http://jabber.org/protocol/muc',
            ),
        )
        # TODO: Answer room configuration request.
        # TODO: Wait until server responds on room join before continuing.

    def add_to_roster(self, nick, jid):
        if nick in self.roster:
            return self.roster[nick]
        try:
            user = self.shoutbox.getUserByJid(jid)
        except ShoutboxUserNotFoundError:
            # Default to anonymous user with JID as username
            user = User(1, jid, '')
        self.roster[nick] = user
        self.logprint("Adding to roster:", nick)
        return user

    def delete_from_roster(self, nick):
        if nick in self.roster:
            del self.roster[nick]
            self.logprint("Removing from roster:", nick)
            return True
        return False

    def get_from_roster(self, nick, jid):
        if not nick in self.roster:
            self.add_to_roster(nick, jid)
        return self.roster[nick]

    def remove_jid_from_roster(self, jid, nick=None):
        self.logprint("Removing self from roster:", jid, nick)
        if nick and nick in self.roster:
            usr = self.roster[nick]
            list = dict(nick=usr)
        else:
            list = self.roster
        if list:
            for k, u in list.items(): 
                if u.jid == jid:
                    self.delete_from_roster(k)

    def get_os_info(self):
        return str(platform.platform())

    def strip_tags(self, s):
        """
        Strip html tags from s
        """
        # this list is neccesarry because chk() would otherwise not know
        # that intag in strip_tags() is ment, and not a new intag variable in chk().
        intag = [False]

        def chk(c):
            if intag[0]:
                intag[0] = (c != '>')
                return False
            elif c == '<':
                intag[0] = True
                return False
            return True

        return ''.join(c for c in s if chk(c))

    def clean_message(self, text):
        """
        Clean text of unwanted content.
        """
        text = self.strip_tags(text)
        return text

    def update_last_time(self):
        self.last_time = time()

    def get_last_activity(self):
        return str(int(time() - self.last_time))

    def logprint(self, *message):
        #print "--------------------------------------------------------------"
        print datetime.now().strftime(self.cfg.log_date_format), '-',
        for m in message:
            print m,
        print "\n--------------------------------------------------------------"

    def change_nick(self, nick):
        if self.cfg.show_nick == "True":
            return
        # If nick is unavailable, append "_" and try again.
        if nick and nick != self.current_nick:
            # If nick is already in roster, but with shoutbridge jid, remove it.
            self.remove_jid_from_roster(self.login, nick)
            if nick in self.roster:
                return self.change_nick(nick + '_')
            self.current_nick = nick
            self.send_presence(
                to=self.room + '/' + nick
            )
            return nick

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

    def lookup_iq_method(self, command):
        return getattr(self, 'handle_iq_' + command.upper(), None) or self.handle_iq_DEFAULT

    def handle_iq_DEFAULT(self, frm=None, to=None, id=None, query=None):
        self.logprint("Unknown incoming IQ stanza:", frm, to, id, query)

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

    def handle_iq_RESULT(self, frm=None, to=None, id=None, query=None):
        """
        IQ result is ignored.
        """
        pass

    def handle_iq_SET(self, frm=None, to=None, id=None, query=None):
        """
        IQ set not yet implemented, return error.
        """
        self.send_iq_error(to=frm, id=id, query=query)

    def handle_iq_ERROR(self, frm=None, to=None, id=None, query=None):
        """
        IQ error stanza is just logged.
        """
        self.logprint("Received IQ error stanza:", frm, id, query.toXml())

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

    def lookup_presence_method(self, command):
        return getattr(self, 'handle_presence_' + command.upper(), None) or self.handle_presence_DEFAULT

    def handle_presence_DEFAULT(self, pres, fromjid=None, **kwargs):
        print "Received unknown presence:", pres.toXml()

    def handle_presence_ERROR(self, pres, fromjid=None, **kwargs):
        print "Received error presence:", pres.toXml()
        if pres.error and pres.error.hasAttribute('code'):
            code = pres.error['code']
        if code == "409":
            # Nick taken, default to original nick.
            self.change_nick(self.resource)

    def handle_presence_UNAVAILABLE(self, pres, nick=None, **kwargs):
        self.delete_from_roster(nick)

    def handle_presence_AVAILABLE(self, pres, fromstr=None, nick=None, **kwargs):
        user = self.add_to_roster(nick, fromstr)

    def handle_presence_UNSUBSCRIBE(self, pres, fromjid=None, **kwargs):
        self.send_presence(
            type="unsubscribed",
            to=fromjid,
        )

    def handle_presence_SUBSCRIBE(self, pres, fromjid=None, **kwargs):
        self.send_presence(
            type="subscribed",
            to=fromjid,
        )

    def send_presence_status(self, show=None, status=None):
        """
        Convenience method to send status information.
        """
        if status:
            self.cfg.xmpp_status = status
        else:
            status = self.cfg.xmpp_status
        if not show:
            show = "chat"
        self.send_presence(xmlns='jabber:client', show=show, status=status)

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

    def ping(self):
        """
        Emulate user being active by sending presence status to server and
        updating last active time.
        """
        self.update_last_time()
        self.send_presence_status()

    def process_shoutbox_messages(self):
        if not self.xmlstream:
            return False

        # Read shoutbox messages.
        # TODO: Should possibly use E-tag and options to see if anything has changed.
        msgs = self.shoutbox.readShouts()
        self.logprint("Number of messages received:", len(msgs))
        for m in msgs:
            text = self.clean_message(m.text)
            if self.cfg.show_time == "True" and self.cfg.show_nick == "True":
                text = "%s <%s> %s" % (m.time, m.name, text)
            elif self.cfg.show_time == "True":
                text = "%s %s" % (m.time, text)
            elif self.cfg.show_nick == "True":
                text = "<%s> %s" % (m.name, text)
            self.send_message(self.room, text, nick=m.name)

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

