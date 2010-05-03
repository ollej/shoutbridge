# -*- coding: utf-8 -*-

import random
from Plugin import *
from utilities import *

class MurphyPlugin(Plugin):
    """
    Murphy bot prints a random quote from Murphy's Rules.
    """
    priority = 0
    name = "MurphyPlugin"
    author = "Olle Johansson <Olle@Johansson.com>"
    description = "Murphy bot prints a random quote from Murphy's Rules."
    commands = [
        dict(
            command = ['!murphy'],
            handler = 'send_quote',
        ),
    ]

    def setup(self):
        """
        Setup method which is called once before any triggers methods are called.
        """
        self.quotes = read_file("extras/murphy.dat", "%")

    def send_quote(self, text, nick, command, cmd):
        """
        Parse message body and send message with dice roll.
        """
        if not self.quotes:
            return
        self.bridge.send_and_shout(random.choice(self.quotes), self.nick)

def main():
    import sys
    import string
    from time import time
    from Conf import Conf
    import Shoutbox
    cfg = Conf('config.ini', 'LOCAL')
    args = sys.argv
    msg = unicode(' '.join(args[1:]), 'utf-8')
    shout = Shoutbox.Shout(1, 4711, 'TestUser', msg, time())
    bridge = FakeBridge()
    plug = MurphyPlugin([bridge])
    plug.setup()
    print "Returned:", plug.handleShoutMessage(shout)

# Call the main function.
if __name__ == '__main__':
    main()
