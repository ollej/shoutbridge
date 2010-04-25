# -*- coding: utf-8 -*-

class Plugin:
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
    bridge = None

    def __init__(self, bridge):
        self.bridge = bridge

    def setup(self):
        """
        Setup method which is called once before any triggers methods are called.
        """
        pass

    def handleXmppMessage(self, message):
        """
        Method called on every received XMPP message stanza.
        Message can be modified and must be returned.
        """
        return message

    def handleShoutMessage(self, shout):
        """
        Method called on every new message from the Shoutbox.
        Shout message can be modified, and must be returned.
        """
        return shout

    def handleXmppIq(self, iq):
        """
        Method called on every received XMPP iq stanza.
        IQ stanza can be modified and must be returned.
        """
        return iq

    def handleXmppPresence(self, presence):
        """
        Method called on every received XMPP Presence stanza.
        Presence stanza object can be modified and must be returned.
        """
        return presence

def main():
    import sys
    import string
    from time import time
    from conf import Conf
    import shoutbox
    cfg = Conf('config.ini', 'LOCAL')
    shout = shoutbox.Shout(1, 4711, 'Test', 'A quick brown fox...', time())
    plug = Plugin('')
    plug.setup()
    print plug.handleShoutMessage(shout)

# Call the main function.
if __name__ == '__main__':
    main()
