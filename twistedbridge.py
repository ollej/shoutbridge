# -*- coding: utf-8 -*-

from twisted.internet import task
from twisted.internet import reactor
from twisted.names.srvconnect import SRVConnector
from twisted.words.xish import domish, xpath
from twisted.words.protocols.jabber import xmlstream, client, jid
from shoutbox import *

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

    def __init__(self, sbox, login, passwd, host, port=5222, room=""):
        """
        Instantiate an XMPP bridge using XMPP login details and a shoutbox object.
        """
        self.shoutbox = sbox
        self.login = login
        self.passwd = passwd
        self.host = host
        self.port = port
        (self.room, foo, self.resource) = room.rpartition('/')
        self.roomjid = room

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
        print "RECV: %s" % unicode(buf, 'utf-8').encode('ascii', 'replace')

    def rawDataOut(self, buf):
        print "SEND: %s" % unicode(buf, 'utf-8').encode('ascii', 'replace')

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
        presence = domish.Element((None, 'presence'))
        xs.send(presence)
        #reactor.callLater(35, xs.sendFooter)

        # Connect to conference room
        self.join_room(self.roomjid)

    def init_failed(self, failure):
        print "Initialization failed."
        print failure
        self.xmlstream.sendFooter()

    def join_room(self, room):
        presence = domish.Element((None, 'presence'))
        presence['from'] = self.login + '/' + 'blaj'
        presence['to'] = room
        presence.addElement('x', u'http://jabber.org/protocol/muc')
        print "Joining room:", presence.toXml()
        self.xmlstream.send(presence)

    def handle_presence(self, pres):
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
            user = self.shoutbox.getUserByLogin(jid)
        except ShoutboxUserNotFoundError:
            # Default to anonymous user with JID as username
            user = User(1, jid, '', '')
        self.roster[nick] = user

    def get_from_roster(self, nick, jid):
        if not nick in self.roster:
            self.add_to_roster(nick, jid)
        return self.roster[nick]

    def handle_message(self, mess):
        """
        Handle an XMPP message.
        """
        type = mess.getAttribute('type')
        fromstr = mess.getAttribute('from')
        fromjid = jid.JID(fromstr)

        # Groupchat messages have different from jid
        if type == 'groupchat':
            (fromstr, sep, nick) = fromstr.rpartition('/')
        else:
            nick = fromjid.user + '@' + fromjid.host

        # Skip if message is sent by shoutbridge
        print "Nick is", nick
        if nick == self.resource:
            print "Got message from myself."
            return

        # Untangle xml mess to retrieve data.
        # Should preferrably be using xpath
        for e in mess.elements():
            # Get message body.
            if e.name == "body":
                body = unicode(e.__str__())
            if e.name == "x":
                if e.defaultUri in ['jabber:x:delay', 'urn:xmpp:delay']:
                    # This is a delayed message, skip it.
                    print "Skipping delayed message."
                    return
                elif e.defaultUri == 'http://jabber.org/protocol/muc#user':
                    for f in e.elements():
                        if f.name == 'status':
                            if f.getAttribute('code') == '100':
                                print "Anonymous room message, skipping."
                                return

        # Send message.
        if body and type in ['message', 'chat', 'groupchat', None]: 
            user = self.get_from_roster(nick, fromstr)
            print "Relaying message to shoutbox:", user, user.name, body
            self.shoutbox.sendShout(user, body)
        else:
            print "What is this?", mess.toXml()

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

    def send_message(self, tojid, text):
        """
        Send an text as XMPP message to tojid
        """
        try:
            message = domish.Element((None, 'message'))
            message['to'] = tojid
            message['from'] = self.login
            message['type'] = 'groupchat'
            message.addElement('body', content=text)
            id = self.xmlstream.send(message)
            print 'Sent message with id', id
        except UnicodeDecodeError:
            print "Unicode Decode Error: ", text

    def process_shoutbox_messages(self):
        if not self.xmlstream:
            return False
        msgs = self.shoutbox.readShouts()
        for m in msgs:
            text = self.clean_message(m.text)
            text = "%s <%s> %s" % (m.time, m.name, text)
            self.send_message(self.room, text)

    def listen(self):
        """
        Start listening on XMPP and Shoutbox, relaying messages.
        """
        try:
            # Send messages from shoutbox every 10 seconds
            l = task.LoopingCall(self.process_shoutbox_messages)
            l.start(2.0)
            # Start the reactor
            reactor.run()
        except KeyboardInterrupt:
            print "Exiting..."

