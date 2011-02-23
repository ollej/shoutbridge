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
            command = [u'!slap', u'!bitchslap', u'!örfil', u'!örfila'],
            handler = 'message_handler',
            method = 'get_slap',
            datfile = 'extras/slaps.dat',
            onevents = ['Message'],
        ),
        dict(
            command = [u'!hug', u'!krama', u'!kram'],
            handler = 'message_handler',
            method = 'get_hug',
            datfile = 'extras/hugs.dat',
            onevents = ['Message'],
        ),
    ]

    def setup(self):
        """
        Setup method which is called once before any triggers methods are called.
        """
        pass

    def get_hug(self, giver, taker, comobj):
        """
        Returns a random hug.
        """
        if giver.lower() == taker.lower():
            msg = u"hugs himself fondly."
        else:
            msg = self.select_and_replace(dict(hugger=giver, hugee=taker), comobj)
        return msg

    def get_slap(self, slapper, slapee, comobj):
        """
        Returns a random slap.
        """
        if slapee.lower() == self.nick.lower():
            slap = u"I'm sorry, %s. I'm afraid I can't do that." % shout.name
        elif slapee == 'Endyamon':
            slap = u"No, he likes it too much."
        else:
            slap = self.select_and_replace(dict(slapper=slapper, slapee=slapee), comobj)
        return slap

    def message_handler(self, shout, command, comobj):
        """
        Handles all incoming messages.
        """
        text = self.strip_command(shout.text, command)
        (slapee, text) = self.get_name(text)
        if slapee:
            get_msg = getattr(self, comobj['method'])
            msg = get_msg(shout.name, slapee, comobj)
            self.send_message(msg, False)

    def select_and_replace(self, tmpl, comobj):
        """
        Selects a random item from items list and uses tmpl dictionary for replacements.
        """
        if 'data' not in comobj:
            comobj['data'] = read_file(comobj['datfile'])
        msg = string.Template(random.choice(comobj['data']).strip())
        slap = msg.substitute(tmpl)
        return slap


