# -*- coding: utf-8 -*-

import random

from plugins.Plugin import *
from utils.utilities import *

class QuotesPlugin(Plugin):
    """
    Quotes bot prints a random quote.
    """
    priority = 0
    name = "QuotesPlugin"
    author = "Olle Johansson <Olle@Johansson.com>"
    description = "Quotes bot prints a random quote."
    separator = '%'
    commands = [
        dict(
            command = ['!citera', '!citat add', '!quote add'],
            handler = 'add_quote',
            quotefile = 'extras/quotes_new.dat',
        ),
        dict(
            command = ['!kimjongil', '!kim'],
            handler = 'random_quote',
            quotefile = 'extras/kimjongil_quotes.dat',
        ),
        dict(
            command = ['!jeff', '!coupling'],
            handler = 'random_quote',
            quotefile = 'extras/jeff_quotes.dat',
        ),
        dict(
            command = ['!citat', '!quote'],
            handler = 'random_quote',
            quotefile = 'extras/quotes.dat',
        ),
        dict(
            command = ['!kjell'],
            handler = 'random_quote',
            quotefile = 'extras/kjell_quotes.dat',
        ),
        dict(
            command = ['!murphy', '!law'],
            handler = 'random_quote',
            quotefile = 'extras/murphy.dat',
        ),
        dict(
            command = ['!evaemma'],
            handler = 'random_quote',
            quotefile = 'extras/evaemma.dat',
        ),
        dict(
            command = ['!storuggla'],
            handler = 'random_quote',
            quotefile = 'extras/storuggla.dat',
        ),
        dict(
            command = ['!hoahoa'],
            handler = 'random_quote',
            quotefile = 'extras/hoahoa.dat',
        ),
    ]

    def setup(self):
        """
        Setup method which is called once before any triggers methods are called.
        """
        for c in self.commands:
            c['quotes'] = read_file(c['quotefile'], self.separator)

    def add_quote(self, text, nick, command, cmd):
        newquote = text.replace(command, '', 1).strip()
        if newquote:
            add_line_to_file(cmd['quotefile'], newquote, separator=self.separator)
            self.bridge.send_and_shout("Quote added for review.", self.nick)

    def random_quote(self, text, nick, command, cmd):
        self.bridge.send_and_shout(random.choice(cmd['quotes']).strip(), self.nick)

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
