# -*- coding: utf-8 -*-

from twisted.internet import task
from twisted.internet import reactor
from twisted.names.srvconnect import SRVConnector
from twisted.words.xish import domish, xpath
from twisted.words.protocols.jabber import xmlstream, client, jid
from shoutbox import *
from utilities import *

class BridgeError(Exception):
    "Unknown Bridge Error"

class BridgeConnectionError(BridgeError):
    "Could not connect to XMPP."

class BridgeAuthenticationError(BridgeError):
    "Could not authenticate."

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

    def rawDataIn(self, buf):
        print "RECV: %s" % unicode(buf, 'utf-8') #.encode('ascii', 'replace')

    def rawDataOut(self, buf):
        print "SEND: %s" % unicode(buf, 'utf-8') #.encode('ascii', 'replace')

    def connected(self, xs):
        print 'Connected.'
        self.xmlstream = xs

        # Log all traffic
        xs.rawDataInFn = self.rawDataIn
        xs.rawDataOutFn = self.rawDataOut

        # Add Event observers
        xs.addObserver("/message[@type='groupchat']", self.handle_message)
        #xs.addObserver("/message[@type='chat']", self.handle_message)
        xs.addObserver("/presence", self.handle_presence)

    def disconnected(self, xs):
        print 'Disconnected.'
        #reactor.stop()

    def authenticated(self, xs):
        print "Authenticated."
        # Send initial presence
        self.send_presence(xmlns='jabber:client', show="chat", status=self.cfg.xmpp_status)

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

        #presence = domish.Element((None, 'presence'))
        #presence['from'] = self.login + '/' + self.cfg.xmpp_resource
        #presence['to'] = room
        #presence.addElement('x', u'http://jabber.org/protocol/muc')
        #print "Joining room:", presence.toXml()
        #self.xmlstream.send(presence)

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
            self.update_nick(self.resource)

    def handle_presence_UNAVAILABLE(self, pres, nick=None, **kwargs):
        if nick in self.roster:
            del self.roster[nick]
            print "Removing from roster:", nick

    def handle_presence_AVAILABLE(self, pres, fromstr=None, nick=None, **kwargs):
         if nick not in self.roster:
            self.add_to_roster(nick, fromstr)
            print "Adding to roster:", nick

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

    def handle_presence_old(self, pres):
        type = pres.getAttribute('type')
        fromstr = pres.getAttribute('from')
        (login, sep, nick) = fromstr.rpartition('/')
        fromjid = jid.JID(fromstr)
        # FIXME: This is silly, I need xpaths working.
        for e in pres.elements():
            if e.name == 'x':
                for f in e.elements():
                    if f.name == 'item':
                        if f.hasAttribute('jid'):
                            fromjid = jid.JID(f['jid'])
                            break
        fromstr = fromjid.user + '@' + fromjid.host
        if type == 'unavailable':
            if nick in self.roster:
                del self.roster[nick]
                print "Removing from roster:", nick
        else:
            if nick not in self.roster:
                self.add_to_roster(nick, fromstr)
                print "Adding to roster:", nick
        print "Roster: ", str(self.roster)

    def add_to_roster(self, nick, jid):
        try:
            user = self.shoutbox.getUserByJid(jid)
        except ShoutboxUserNotFoundError:
            # Default to anonymous user with JID as username
            user = User(1, jid, '')
        self.roster[nick] = user

    def get_from_roster(self, nick, jid):
        if not nick in self.roster:
            self.add_to_roster(nick, jid)
        return self.roster[nick]

    def handle_message(self, mess):
        """
        Handle an XMPP message.
        """
        if mess.x and mess.x.defaultUri:
            print mess.x.defaultUri
            # Check if message is delayed.
            if mess.x.defaultUri in ['jabber:x:delay', 'urn:xmpp:delay']:
                print "--------------------------------------------------------------"
                print "Skipping delayed message."
                print "--------------------------------------------------------------"
                return

            # Ignore status message about anonymous room.
            if mess.x.defaultUri == 'http://jabber.org/protocol/muc#user':
                if mess.x.status and mess.x.status.getAttribute('code') == '100':
                    print "--------------------------------------------------------------"
                    print "Anonymous room message, skipping."
                    print "--------------------------------------------------------------"
                    return

        fromstr = mess.getAttribute('from')
        fromjid = jid.JID(fromstr)

        # Groupchat messages have different from jid
        if mess['type'] == 'groupchat':
            (fromstr, sep, nick) = fromstr.rpartition('/')
        else:
            nick = fromjid.user + '@' + fromjid.host

        # Skip if message is sent by shoutbridge
        # TODO: Not foolproof, need better way to check who sent message.
        print "Nick is", nick
        #if nick == self.resource or nick == self.current_nick:
        fromuser = self.roster.get(nick)
        #print "Fromuser:", fromuser
        #print "fromuser.id", fromuser.id
        #print "fromuser.name", fromuser.name
        #print "fromuser.jid:", fromuser.jid
        #print "self.login:", self.login
        #print "self.resource:", self.resource
        #print "fromstr:", fromstr
        #print "current_nick:", self.current_nick
        if fromuser and fromuser.name == self.login or nick == self.current_nick:
            print "--------------------------------------------------------------"
            print "Got message from myself, skipping..."
            print "--------------------------------------------------------------"
            return

        # Get message body.
        body = getElStr(mess.body)

        # Send message.
        if body and mess['type'] in ['message', 'chat', 'groupchat', None]: 
            user = self.get_from_roster(nick, fromstr)
            print "Relaying message to shoutbox:", user, user.id, user.jid, user.name, body
            self.shoutbox.sendShout(user, body)
        else:
            print "--------------------------------------------------------------"
            print "Unknown message:", mess.toXml()
            print "--------------------------------------------------------------"

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

    def update_nick(self, nick):
        if self.cfg.show_nick == "True":
            return
        if nick and nick != self.current_nick:
            self.current_nick = nick
            self.send_presence(
                to=self.room + '/' + nick
            )

    def send_message(self, tojid, text, nick=None):
        """
        Send an text as XMPP message to tojid
        """
        try:
            if nick:
                self.update_nick(nick)
            message = domish.Element((None, 'message'))
            message['to'] = tojid
            message['from'] = self.login + '/' + nick
            message['type'] = 'groupchat'
            message.addElement('body', content=text)
            id = self.xmlstream.send(message)
            print 'Sent message with id', id
        except UnicodeDecodeError:
            print "Unicode Decode Error: ", text

    def send_presence(self, xmlns=None, type=None, status=None, show=None,
                     frm=None, to=None, children=None):
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
        self.xmlstream.send(presence)

    def process_shoutbox_messages(self):
        if not self.xmlstream:
            return False
        self.send_presence(show="chat", status=self.cfg.xmpp_status)
        if not self.xmlstream:
            return False
        msgs = self.shoutbox.readShouts()
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
            # Start the reactor
            reactor.run()
        except KeyboardInterrupt:
            self.send_presence(type="unavailable", reason="Quitting...")
            print "Exiting..."

