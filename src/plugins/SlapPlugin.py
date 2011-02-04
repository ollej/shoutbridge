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

class SlapPlugin(Plugin):
    """
    Lets uses slap each other with hilarious items.
    """
    priority = 0
    name = "SlapPlugin"
    author = "Olle Johansson <Olle@Johansson.com>"
    description = "Slap bot lets users slap each other with hilarious items."
    commands = [
        dict(
            command = ['!slap'],
            handler = 'slap',
            onevents = ['Message'],
        ),
    ]

    def setup(self):
        """
        Setup method which is called once before any triggers methods are called.
        """
        self.slapitems = read_file("extras/slaps.dat")

    def slap(self, shout, command, comobj):
        """
        Parse message body and send message with dice roll.
        """
        words = shout.text.split()
        slapee = words[1]
        tmpl = string.Template(random.choice(self.slapitems).strip())
        if slapee:
            if slapee.lower() == self.nick.lower():
                slap = u"I'm sorry, %s. I'm afraid I can't do that." % shout.name
            elif slapee == 'Endyamon':
                slap = u"No, he likes it too much."
            else:
                slap = tmpl.substitute(dict(slapper=shout.name, slapee=slapee))
            self.bridge.send_and_shout(slap, self.nick)

