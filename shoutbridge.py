# -*- coding: utf-8 -*-

import sys
from shoutbox import *
#from xmppbridge import *
from twistedbridge import *
from conf import Conf

def start_shoutbridge():
    print "Shoutbridge started..."
    cfg = Conf('config.ini', 'LOCAL')
    sbox = Shoutbox(cfg.db_name, cfg.db_user, cfg.db_pass)
    bridge = TwistedBridge(sbox, cfg.xmpp_login, cfg.xmpp_pass, cfg.xmpp_host, cfg.xmpp_port, cfg.xmpp_room)
    bridge.listen()
    #row = sbox.getUser(xmpp_login)
    #usr = User(row[0], row[1])
    #print "User = " + str(usr)
    #xmppdetails = sbox.getXmppDetails(2)
    #print "XMPP Details = " + str(xmppdetails)
    #sbox.sendShout(usr, "asdf asdf asdf ")
    #msgs = sbox.readShouts()
    #for m in msgs:
    #    print m
    print "Shoutbridge ended."

# Call the main function.
if __name__ == '__main__':
    start_shoutbridge()

