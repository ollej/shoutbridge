# -*- coding: utf-8 -*-

"""
The MIT License

Copyright (c) 2010 Olle Johansson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

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
        dict(
            command = ['!gang', '!gäng'],
            handler = 'random_quote',
            onevents = ['Message'],
            separator = None,
            quotefile = 'extras/gangnames.dat',
        ),
    ]

    def setup(self):
        """
        Setup method which is called once before any triggers methods are called.
        """
        #for c in self.commands:
        pass

    def load_quotes(self, c):
        try:
            sep = c['separator']
        except KeyError:
            sep = self.separator
        c['quotes'] = read_file(c['quotefile'], sep)

    def add_quote(self, shout, command, comobj):
        newquote = shout.text.replace(command, '', 1).strip()
        if newquote:
            add_line_to_file(comobj['quotefile'], newquote, separator=self.separator)
            self.bridge.send_and_shout("Quote added for review.", self.nick)

    def get_nick(self, comobj):
        try:
            nick = comobj['nick']
        except KeyError:
            nick = self.nick
        return nick

    def get_quote(self, comobj):
        if 'quotes' not in comobj:
            self.load_quotes(comobj)
        return random.choice(comobj['quotes']).strip()

    def random_quote(self, shout, command, comobj):
        self.bridge.send_and_shout(self.get_quote(comobj), self.get_nick(comobj))

