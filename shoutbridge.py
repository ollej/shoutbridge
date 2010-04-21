# -*- coding: utf-8 -*-

import sys
from messageshoutbox import *
from twistedbridge import *
from conf import Conf

def start_shoutbridge():
    print "Shoutbridge started..."
    cfg = Conf('config.ini', 'LOCAL')

    # Setup Shoutbox
#    if cfg.shoutbox_type == "external_ubb":
#        from externalshoutbox import *
#    elif cfg.shoutbox_type == "ubb":
#        from shoutbox import *
#    else:
#        print "Configured shoutbox type not supported:", cfg.shoutbox_type
    sbox = MessageShoutbox(cfg)

    # Setup xmpp bridge
#    if cfg.bridge_type == "twisted":
#        from twistedbridge import *
#        bridge = TwistedBridge(sbox, cfg)
#    elif cfg.bridge_type == "xmpppy":
#        from xmppbridge import *
#        bridge = XmppBridge(sbox, cfg)
#    elif cfg.bridge_type == "headstock":
#        from headstockbridge import *
#        bridge = HeadstockBridge(sbox, cfg)
#    else:
#        print "Bridge type not supported:", cfg.bridge_type
    bridge = TwistedBridge(sbox, cfg)

    # Start bridge
    bridge.listen()
    print "Shoutbridge ended."

# Call the main function.
if __name__ == '__main__':
    start_shoutbridge()

