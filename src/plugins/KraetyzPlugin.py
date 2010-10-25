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

class KraetyzPlugin(Plugin):
    """
    Match texts from a list of users and returns a message.
    If any of the nicks in onsender writes a message that contains the text
    in textmatch, then the bot will send the text as a message, substituting
    %s for the nick of the sender.
    """
    priority = 0
    name = "KraetyzPlugin"
    author = "Olle Johansson <Olle@Johansson.com>"
    description = "Match texts from a list of users and returns a message."
    commands = [
        dict(
            command=[''],
            handler='send_warning',
            onevents=['Message'],
            onsender = ['Kraetyz'],
            textmatch = 'jag tycker',
            text = u"/me bannar %s för uttryckande av åsikt.",
        ),
    ]

    def send_warning(self, shout, command, comobj):
        """
        Parse message body and send message with dice roll.
        """
        if shout.name in comobj['onsender'] and shout.text.lower().find(comobj['textmatch']) >= 0:
            self.bridge.send_and_shout(comobj['text'] % (shout.name), self.nick)


