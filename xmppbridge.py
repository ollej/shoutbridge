# -*- coding: utf-8 -*-

import sys,os,xmpp,time,re

class XmppBridge(object):
    login = ""
    passwd = ""
    room = ""
    host = ""
    port = 5222
    shoutbox = None

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
        self.jid = xmpp.protocol.JID(self.login)
        self.cl = xmpp.Client(self.jid.getDomain(), debug=[])
        self.con = self.cl.connect()
        if not self.con:
            raise Exception('Could not connect!')
        print 'Connected with', self.con
        self.auth = self.cl.auth(self.jid.getNode(), self.passwd, resource=self.jid.getResource())
        if not self.auth:
            raise Exception('Could not authenticate!')
        print 'Authenticated using', self.auth

    def __del__(self):
        if self.cl:
            self.cl.disconnect()

    def strip_tags(self, s):
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

    def replace_graemlins(self, text):
        if text.find('<<GRAEMLIN_URL>>') < 0:
            return text
        for s in self.graemlins:
            text = text.replace(s, '')
        return text

    def clean_message(self, text):
        #text = self.replace_graemlins(text)
        #text = text.replace('<<GRAEMLIN_URL>>', '')
        text = self.strip_tags(text)
        return text

    def send_message(self, tojid, text):
        try:
            id = self.cl.send(xmpp.protocol.Message(tojid, text))
            print 'Sent message with id', id
        except UnicodeDecodeError:
            print "Unicode Decode Error: " + text

    def listen(self):
        """
        Start listening on XMPP and Shoutbox, relaying messages.
        """
        try:
            while 1:
                print "Loop..."
                msgs = self.shoutbox.readShouts()
                for m in msgs:
                    text = self.clean_message(m.text)
                    text = "%s <%s> %s" % (m.time, m.name, text)
                    self.send_message(self.login, text)
                time.sleep(1)
        except KeyboardInterrupt:
            print "Exiting..."

