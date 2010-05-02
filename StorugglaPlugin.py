# -*- coding: utf-8 -*-

import random
from Plugin import *
from utilities import *

class StorugglaPlugin(Plugin):
    """
    Storuggla bot prints a random quote from Storuggla's sign-out messages.
    """
    priority = 0
    name = "StorugglaPlugin"
    author = "Olle Johansson <Olle@Johansson.com>"
    description = "Storuggla bot prints a random quote from Storuggla's sign-out messages."
    commands = [
        dict(
            command = '!storuggla',
            handler = 'send_quote',
        ),
    ]

    def setup(self):
        """
        Setup method which is called once before any triggers methods are called.
        """
        self.quotes = read_file("extras/storuggla.dat", "%")

    def send_quote(self, text, nick, command, cmd):
        """
        Parse message body and send message with dice roll.
        """
        if self.quotes:
            self.bridge.send_and_shout(random.choice(self.quotes), self.nick)

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
    plug = StorugglaPlugin([bridge])
    plug.setup()
    print "Returned:", plug.handleShoutMessage(shout)

# Call the main function.
if __name__ == '__main__':
    main()
