# -*- coding: utf-8 -*-

import random

from utils.BridgeClass import *
from utils.utilities import *

class PluginError(Exception):
    """
    Default Plugin exception.
    """

class FakeBridge:
    """
    Fake bridge used for running plugins from command line.
    """
    def send_and_shout(self, text, nick=None):
        print "Message: ", nick, text

class Plugin(BridgeClass):
    """
    Superclass for Shoutbridge plugins.
    Methods should be implemented by sub-classes.
    All configured plugins will be setup by the Shoutbridge software on
    startup. Then the handle* methods will be triggered on specific events.
    """
    priority = 0
    name = "Plugin"
    author = "Olle Johansson"
    description = "Default Shoutbridge plugin interface."
    nick = 'HALiBot'
    bridge = None
    commands = []

    def __init__(self, args):
        try:
            self.bridge = args[0]
        except AttributeError:
            self.logprint("No bridge object given.")
            raise PluginError

    def setup(self):
        """
        Setup method which is called once before any triggers methods are called.
        """
        pass

    def prepend_sender(self, text, sep=': '):
        """
        Prepends name of sender of message if available.
        """
        try:
            if self.sender_nick:
                text = "%s%s%s" % (self.sender_nick, sep, text)
        except AttributeError:
            pass
        return text

    def show_text(self, shout, command=None, comobj=None):
        """
        Display text from command.
        """
        try:
            nick = comobj['nick']
        except KeyError:
            nick = self.nick
        self.bridge.send_and_shout(random.choice(comobj['text']), nick)


def main():
    import sys
    import string
    from time import time
    from Conf import Conf
    import Shoutbox
    cfg = Conf('config.ini', 'LOCAL')
    shout = Shoutbox.Shout(1, 4711, 'Test', 'A quick brown fox...', time())
    bridge = FakeBridge()
    plug = Plugin([bridge])
    plug.setup()
    print plug.handleShoutMessage(shout)

# Call the main function.
if __name__ == '__main__':
    main()
