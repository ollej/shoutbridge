#!python
# -*- coding: utf-8 -*-

import sys
from utils.Conf import Conf
from utils.ObjectFactory import *
from utils.decorators import *
from utils.utilities import get_options

def start_shoutbridge():
    # Read command line options.
    (options, args) = get_options()

    # Read configuration.
    configfile = options.config or 'config.ini'
    configsection = options.section or 'LOCAL'
    cfg = Conf(configfile, configsection)
    cfg.set_items(vars(options))

    if cfg.get_bool('verbose'):
        print "Shoutbridge started..."

    # Setup Shoutbox
    of = ObjectFactory()
    sbox = of.create(cfg.shoutbox_type, mod='shoutbox', inst="Shoutbox")
    sbox.setConfig(cfg)

    # Setup xmpp bridge
    bridge = of.create(cfg.bridge_type, mod='bridges', inst="XmppBridge")
    bridge.setup(sbox, cfg)

    # Start bridge
    bridge.listen()
    if cfg.get_bool('verbose'):
        print "Shoutbridge ended."

# Call the main function.
if __name__ == '__main__':
    start_shoutbridge()

