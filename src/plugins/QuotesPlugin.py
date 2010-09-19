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
            onevents = ['Message'],
            quotefile = 'extras/quotes_new.dat',
        ),
        dict(
            command = ['!kimjongil', '!kim'],
            handler = 'random_quote',
            onevents = ['Message'],
            quotefile = 'extras/kimjongil_quotes.dat',
        ),
        dict(
            command = ['!jeff', '!coupling'],
            handler = 'random_quote',
            onevents = ['Message'],
            quotefile = 'extras/jeff_quotes.dat',
            nick = 'Jeff'
        ),
        dict(
            command = ['!citat', '!quote'],
            handler = 'random_quote',
            onevents = ['Message'],
            #quotefile = 'extras/quotes.dat',
            quotefile = 'http://www.rollspel.nu/forum/ubbthreads.php?ubb=listquotes',
        ),
        dict(
            command = ['!kjell'],
            handler = 'random_quote',
            onevents = ['Message'],
            quotefile = 'extras/kjell_quotes.dat',
        ),
        dict(
            command = ['!murphy', '!law'],
            handler = 'random_quote',
            onevents = ['Message'],
            quotefile = 'extras/murphy.dat',
        ),
        dict(
            command = ['!evaemma'],
            handler = 'random_quote',
            onevents = ['Message'],
            quotefile = 'extras/evaemma.dat',
        ),
        dict(
            command = ['!storuggla'],
            handler = 'random_quote',
            onevents = ['Message'],
            quotefile = 'extras/storuggla.dat',
        ),
        dict(
            command = ['!hoahoa'],
            handler = 'random_quote',
            onevents = ['Message'],
            quotefile = 'extras/hoahoa.dat',
        ),
        dict(
            command = ['!icebreaker', '!conversation', '!isbrytare', '!konversation'],
            handler = 'random_quote',
            onevents = ['Message'],
            quotefile = 'extras/conversation_starters.dat',
        ),
        dict(
            command = ['!8ball', '!magic', '!oracle', '!orakel'],
            handler = 'random_quote',
            onevents = ['Message'],
            quotefile = 'extras/8ball.dat',
        ),
    ]

    def setup(self):
        """
        Setup method which is called once before any triggers methods are called.
        """
        for c in self.commands:
            c['quotes'] = read_file(c['quotefile'], self.separator)

    def add_quote(self, shout, command, comobj):
        newquote = shout.text.replace(command, '', 1).strip()
        if newquote:
            add_line_to_file(comobj['quotefile'], newquote, separator=self.separator)
            self.bridge.send_and_shout("Quote added for review.", self.nick)

    def random_quote(self, shout, command, comobj):
        try:
            nick = comobj['nick']
        except KeyError:
            nick = self.nick
        self.bridge.send_and_shout(random.choice(comobj['quotes']).strip(), nick)

