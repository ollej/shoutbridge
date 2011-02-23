#!python
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
    #sbox.setConfig(cfg)

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

