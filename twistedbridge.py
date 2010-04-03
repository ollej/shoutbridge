# -*- coding: utf-8 -*-

from twisted.internet import task
from twisted.internet import reactor
from twisted.names.srvconnect import SRVConnector
from twisted.words.xish import domish
from twisted.words.protocols.jabber import xmlstream, client, jid

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
    shoutbox = None
    xmlstream = None
    roster = []

    def __init__(self, sbox, login, passwd, host, port=5222, room=""):
        """
        Instantiate an XMPP bridge using XMPP login details and a shoutbox object.
        """
        self.shoutbox = sbox
        self.login = login
        self.passwd = passwd
        self.host = host
        self.port = port
        self.room = room

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

    def disconnected(self, xs):
        print 'Disconnected.'
        reactor.stop()

    def authenticated(self, xs):
        print "Authenticated."
        presence = domish.Element((None, 'presence'))
        xs.send(presence)
        #reactor.callLater(35, xs.sendFooter)

    def init_failed(self, failure):
        print "Initialization failed."
        print failure
        self.xmlstream.sendFooter()

    def handle_presence(self, conn, pres):
        nick = pres.getFrom().getResource()
        type = pres.getType()
        print "Presence stanza received:", nick, type
        if type == 'unavailable':
            if nick in self.roster:
                self.roster.remove(nick)
                print "Adding to roster:", nick
        else:
            if nick not in self.roster:
                self.roster.append(nick)
                print "Removing from roster:", nick


    def handle_message(self, conn, mess):
        """
        Handle an XMPP message.
        """
        type = mess.getType()
        fromjid = mess.getFrom().getStripped()
        nick = mess.getFrom().getResource()
        print "Message stanza received:", fromjid, '/', nick, type
        if type in ['message', 'chat', None]: 
            # and fromjid == self.remotejid:
            text = mess.getBody()
            try:
                user = self.shoutbox.getUserByLogin(fromjid)
            except ShoutboxUserNotFoundError:
                # Default to anonymous user with JID as username
                user = User(1, nick, '', '')
            self.shoutbox.sendShout(user, text)

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
            message['type'] = 'chat'
            message.addElement('body', content=text)
            id = self.xmlstream.send(message)
            print 'Sent message with id', id
        except UnicodeDecodeError:
            print "Unicode Decode Error: " + text

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
            l.start(10.0)
            # Start the reactor
            reactor.run()
        except KeyboardInterrupt:
            print "Exiting..."

