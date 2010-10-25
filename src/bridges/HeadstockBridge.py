# -*- coding: utf-8 -*-

"""
The MIT License

Copyright (c) 2010 Olle Johansson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

"""
Bridge using headstock library.
Unfortunately, it doesn't work. Connection is dropped immediately.
"""

from headstock.lib.utils import generate_unique
from bridge import Element as E
from bridge.common import XMPP_CLIENT_NS, XMPP_ROSTER_NS
from headstock.client import AsyncClient
import headstock

from bridges.XmppBridge import *
from shoutbox.Shoutbox import *

class HeadstockBridge(XmppBridge):
    login = ""
    passwd = ""
    room = ""
    host = ""
    port = 5222
    shoutbox = None

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

    def ready(self, client):
        self.client = client

    def send_message(self, jid, text):
        m = E(u"message", attributes={u'from': unicode(self.client.jid), u'to': unicode(jid), u'type': u'chat', u'id': generate_unique()}, namespace=XMPP_CLIENT_NS)
        E(u'body', content=text, namespace=XMPP_CLIENT_NS, parent=m)

        self.client.send_stanza(m)

    @headstock.xmpphandler('item', XMPP_ROSTER_NS)
    def roster(self, e):
        try:
            usr = self.sbox.getUserByLogin(e.get_attribute_value('jid', ''))
        except:
            name = e.get_attribute_value('name', '')
            if name:
                name = 'Anonym - ' + name
            else:
                name = 'Anonym'
            usr = User(1, name, '', '')
        self.sbox.sendShout(usr, e.get_attribute_value(''))
        print "Contact '%s' %s with subscription: %s" % (e.get_attribute_value('name', ''),
                                                         e.get_attribute_value('jid', ''),
                                                         e.get_attribute_value('subscription', ''))

    @headstock.xmpphandler('presence', XMPP_CLIENT_NS)
    def presence(self, e):
        print "Received '%s' presence from: %s" % (e.get_attribute_value('type', 'available'),
                                                   e.get_attribute_value('from'))

    def listen(self):
        """
        Start listening on XMPP and Shoutbox, relaying messages.
        """
        print "Creating AsyncClient..."
        c = AsyncClient(self.login, self.passwd, hostname=self.host, port=self.port)
        print "Registering xmppbridge with client..."
        c.register(self)
        print "Running client..."
        c.run()

