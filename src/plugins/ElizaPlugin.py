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

from plugins.Plugin import *
from utils.utilities import *
import eliza

class ElizaPlugin(Plugin):
    """
    Eliza, the famous non-professional psychatrist.
    If someone writes a message like:
    Eliza, what is the meaning of life?
    This plugin will answer as Eliza, with some ingenious answer.

    Requires eliza.py from:
        http://www.jezuk.co.uk/cgi-bin/view/software/eliza
    """
    priority = 0
    name = "ElizaPlugin"
    author = "Olle Johansson"
    description = "Eliza, the psychatrist"
    nick = "Eliza"
    commands = [
        dict(
            command=['Eliza,', 'Eliza:', '!eliza'],
            handler='ask_eliza',
            onevents=['Message'],
        ),
    ]

    def setup(self):
        """
        Setup method which is called once before any triggers methods are called.
        """
        self.eliza = eliza.eliza()

    def ask_eliza(self, shout, cmd, comobj):
        """
        Parse message body and send message with dice roll.
        """
        text = shout.text[len(cmd):].strip()
        response = self.eliza.respond(text)
        if response:
            self.bridge.send_and_shout(shout.name + ': ' + response, self.nick)

