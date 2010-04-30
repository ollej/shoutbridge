# -*- coding: utf-8 -*-

import random
from Plugin import *
from utilities import *

class QuotesPlugin(Plugin):
    """
    Quotes bot prints a random quote.
    """
    priority = 0
    name = "QuotesPlugin"
    author = "Olle Johansson <Olle@Johansson.com>"
    description = "Quotes bot prints a random quote."
    nick = "HALiBot"
    filename = "extras/quotes.dat"
    filename_newquotes = "extras/quotes_new.dat"
    separator = '%'
    commands = [
        dict(
            command = ['!citat add', '!quote add'],
            handler = 'add_quote',
        ),
        dict(
            command = ['!citat', '!quote'],
            handler = 'random_quote',
        ),
    ]

    def setup(self):
        """
        Setup method which is called once before any triggers methods are called.
        """
        self.quotes = read_file(self.filename, self.separator)

    def add_quote(self, text, nick, command):
        newquote = text.replace(command, '', 1).strip()
        if newquote:
            add_line_to_file(self.filename_newquotes, newquote, separator=self.separator)
            self.bridge.send_and_shout("Quote added for review: " + newquote, self.nick)

    def random_quote(self, text, nick, command=None):
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
    plug = QuotesPlugin([bridge])
    plug.setup()
    print "Returned:", plug.handleShoutMessage(shout)

# Call the main function.
if __name__ == '__main__':
    main()
