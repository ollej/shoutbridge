# -*- coding: utf-8 -*-

import sys
from conf import Conf
from ObjectFactory import *

def start_shoutbridge():
    print "Shoutbridge started..."
    cfg = Conf('config.ini', 'LOCAL')
    of = ObjectFactory()

    # Setup Shoutbox
    sbox = of.create(cfg.shoutbox_type, "Shoutbox")
    sbox.setConfig(cfg)

    # Setup xmpp bridge
    bridge = of.create(cfg.bridge_type, "XmppBridge")
    bridge.setup(sbox, cfg)

    # Start bridge
    bridge.listen()
    print "Shoutbridge ended."

# Call the main function.
if __name__ == '__main__':
    start_shoutbridge()

