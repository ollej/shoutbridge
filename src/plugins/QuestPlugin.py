# -*- coding: utf-8 -*-

"""
The MIT License

Copyright (c) 2011 Olle Johansson

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

from GoldQuest import *
from plugins.Plugin import *

class QuestPlugin(Plugin):
    name = "QuestPlugin"
    author = "Olle Johansson"
    description = "A simple multi user quest game."
    commands = [
        dict(
            command = ['!quest'],
            handler = 'quest',
            onevents = ['Message'],
        )
    ]
    nick = 'GoldQuest'
    game = None

    def setup(self):
        """
        Sets up a new instance of the game class.
        """
        self.game = GoldQuest(self.bridge.cfg)

    def quest(self, shout, command, comobj):
        text = self.strip_command(shout.text, command)
        msg = self.game.play(text)
        return self.send_message(msg, False)


