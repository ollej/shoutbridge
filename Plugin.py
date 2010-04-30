# -*- coding: utf-8 -*-

from BridgeClass import *

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
    nick = ''
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

    def prepend_sender(self, text):
        """
        Prepends name of sender of message if available.
        """
        if self.sender_nick:
            text = self.sender_nick + ': ' + text
        return text


    def handleXmppMessage(self, message):
        """
        Method called on every received XMPP message stanza.
        """
        pass

    def handleShoutMessage(self, shout):
        """
        Method called on every new message from the Shoutbox.
        """
        pass

    def handleXmppIq(self, iq):
        """
        Method called on every received XMPP iq stanza.
        """
        pass

    def handleXmppPresence(self, presence):
        """
        Method called on every received XMPP Presence stanza.
        """
        pass

    def handle_shout(self, text, nick):
        """
        Parses the text and matches against command handlers.
        """
        self.logprint(self.name + ": Handling message:", nick, text)
        #text = unicode(text, 'utf-8')
        for cmd in self.commands:
            if not cmd['command'] or text.startswith(cmd['command']):
                handler = getattr(self, cmd['handler'])
                handler(text, nick, cmd['command'])
                break

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
