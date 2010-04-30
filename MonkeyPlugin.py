# -*- coding: utf-8 -*-

from Plugin import *
from utilities import *

class MonkeyPlugin(Plugin):
    """
    Displays a monkey.
    """
    priority = 0
    name = "MonkeyPlugin"
    author = "Olle Johansson <Olle@Johansson.com>"
    description = "Simple plugin to display a monkey."
    nick = "HALiBot"
    commands = [
        dict(
            command = ['!apa', '!monkey'],
            handler = 'show_monkey',
        ),
        dict(
            command = ['!tits', '!boobs', '!boobies'],
            handler = 'show_tits',
        ),
        dict(
            command = ['!fallos', '!snopp', '!penis'],
            handler = 'show_fallos',
        ),
    ]

    def setup(self):
        """
        Setup method which is called once before any triggers methods are called.
        """
        pass

    def show_monkey(self, text, nick, command=None):
        """
        Send a message with a cute monkey.
        """
        self.bridge.send_and_shout("@({-_-})@", "Apa")

    def show_tits(self, text, nick, command=None):
        """
        Show tits!
        """
        self.bridge.send_and_shout("( . )( . )", self.nick)

    def show_fallos(self, text, nick, command=None):
        """
        Show tits!
        """
        self.bridge.send_and_shout("8========D", self.nick)

def main():
    import sys
    import string
    from time import time
    from Conf import Conf
    import Shoutbox
    cfg = Conf('config.ini', 'LOCAL')
    args = sys.argv
    msg = ' '.join(args[1:])
    shout = Shoutbox.Shout(1, 4711, 'Test', msg, time())
    bridge = FakeBridge()
    plug = MonkeyPlugin([bridge])
    plug.setup()
    print "Returned:", plug.handleShoutMessage(shout)

# Call the main function.
if __name__ == '__main__':
    main()
