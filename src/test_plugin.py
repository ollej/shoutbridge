# -*- coding: utf-8 -*-

from bridges.XmppBridge import *
from plugins.Plugin import *
from shoutbox.Shoutbox import *
from utils.ObjectFactory import *

def main():
    import sys
    import string
    from time import time
    args = sys.argv
    try:
        plugin_name = args[1]
    except IndexError:
        print "Usage: %s <plugin_name> <message>" % args[0]
        quit()
    cfg = Conf('../config.ini', 'LOCAL')
    bridge = FakeBridge(cfg=cfg)
    try:
        of = ObjectFactory()
        plug = of.create(plugin_name, mod='plugins', inst="Plugin", args=[bridge])
    except ImportError as ie:
        print "Couldn't load plugin: %s" % plugin_name
	print "Args:", ie.args
        quit()
    msg = unicode(' '.join(args[2:]), 'utf-8')
    shout = Shout(1, 4711, 'PluginTestUser', msg, time())
    plug.setup()
    bridge.plugins[plugin_name] = plug
    bridge.trigger_plugin_event("Message", shout)

# Call the main function.
if __name__ == '__main__':
    main()

