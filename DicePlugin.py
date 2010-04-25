# -*- coding: utf-8 -*-

class DicePlugin:
    """
    Makes die rolls requested by users.
    If someone writes a message like:
    /dice 3d6 
    This plugin will send a message of its own with the result:
    Rolled 3 d6 dice, with result: 12 (4 + 3 + 5)
    """
    priority = 0
    name = "DicePlugin"
    author = "Olle Johansson"
    description = "Dice roller plugin."

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

def main():
    import sys
    import string
    from time import time
    from conf import Conf
    import shoutbox
    cfg = Conf('config.ini', 'LOCAL')
    shout = shoutbox.Shout(1, 4711, 'Test', 'A quick brown fox...', time())
    plug = Plugin()
    plug.setup()
    print plug.handleShoutMessage(shout)

# Call the main function.
if __name__ == '__main__':
    main()
