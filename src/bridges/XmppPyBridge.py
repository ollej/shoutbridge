# -*- coding: utf-8 -*-

import sys
import os
import xmpp
import time
import re

from bridges.XmppBridge import *

class XmppPyBridge(XmppBridge):
    login = ""
    passwd = ""
    room = ""
    host = ""
    port = 5222
    discoName = "Shoutbridge"
    shoutbox = None
    roster = []

    def __init__(self, sbox, cfg):
        """
        Instantiate an XMPP bridge using XMPP login details and a shoutbox object.
        """
        self.shoutbox = sbox
        self.login = cfg.xmpp_login
        self.passwd = cfg.xmpp_pass
        self.host = cfg.xmpp_host
        if cfg.xmpp_port:
            self.port = cfg.xmpp_port
        self.room = cfg.xmpp_room

        # Make an XMPP connection
        self.make_connection()

        # Register handlers
        self.register_handlers()

    def __del__(self):
        if self.cl:
            self.cl.disconnect()

    def make_connection(self):
        """
        Make an XMPP connection and authorize the user.
        """
        self.jid = xmpp.protocol.JID(self.login)
        debug = xmpp.debug.Debug() #['always', 'nodebuilder']
        self.cl = xmpp.Client(self.jid.getDomain(), debug=debug)
        self.con = self.cl.connect()
        #self.cl = xmpp.client.Component(self.jid.getDomain(), self.port, debug=debug)
        #self.con = self.cl.connect((self.jid.getDomain(), self.port))
        if not self.con:
            raise BridgeConnectionError
        print 'Connected with', self.con
        self.auth = self.cl.auth(self.jid.getNode(), self.passwd, resource=self.jid.getResource())
        if not self.auth:
            raise BridgeAuthenticationError
        print 'Authenticated using', self.auth

    def register_handlers(self):
        """
        Register message handlers
        """
        self.cl.RegisterHandler('iq', self.handle_iq)
        self.cl.RegisterHandler('presence', self.handle_presence)
        self.cl.RegisterHandler('message', self.handle_message)
        self.disco = xmpp.browser.Browser()
        self.disco.PlugIn(self.cl)
        self.disco.setDiscoHandler(self.xmpp_base_disco,node='', jid=self.login)

    # Disco Handlers
    def xmpp_base_disco(self, con, event, type):
        fromjid = event.getFrom().__str__()
        to = event.getTo()
        node = event.getQuerynode();
        #Type is either 'info' or 'items'
        if to == self.login:
            if node == None:
                if type == 'info':
                    return {
                        'ids': [
                            {'category': 'gateway', 'type': 'smtp', 'name': self.discoName}],
                        'features': [NS_VERSION, NS_COMMANDS]}
                if type == 'items':
                    return []
            else:
                self.cl.send(Error(event, ERR_ITEM_NOT_FOUND))
                raise NodeProcessed
        else:
            self.cl.send(Error(event, MALFORMED_JID))
            raise NodeProcessed

    def handle_iq(self, conn, iq_node):
        """
        Handler for processing some "get" query from custom namespace
        """
        print "Iq stanza received:", iq_node.getType(), iq_node.getFrom().getResource()
        reply = iq_node.buildReply('result')
        # ... put some content into reply node
        conn.send(reply)
        raise NodeProcessed  # This stanza is fully processed

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
            id = self.cl.send(xmpp.protocol.Message(tojid, text))
            print 'Sent message with id', id
        except UnicodeDecodeError:
            print "Unicode Decode Error: " + text

    def process_shoutbox_messages(self):
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
            while 1:
                print "Loop..."
                # Process incoming XMPP messages.
                self.cl.Process(5)

                # Process shoutbox messages.
                self.process_shoutbox_messages()

                # Sleep before next loop iteration.
                #time.sleep(1)

                # Reconnect to XMPP if necessary.
                if not self.cl.isConnected():
                    self.cl.reconnectAndReauth()

        except KeyboardInterrupt:
            print "Exiting..."

