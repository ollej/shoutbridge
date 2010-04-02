# -*- coding: utf-8 -*-
"""
Bridge using headstock library.
Unfortunately, it doesn't work. Connection is dropped immediately.
"""

from headstock.lib.utils import generate_unique
from bridge import Element as E
from bridge.common import XMPP_CLIENT_NS, XMPP_ROSTER_NS
from headstock.client import AsyncClient
import headstock

class HeadstockBridge(object):
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

