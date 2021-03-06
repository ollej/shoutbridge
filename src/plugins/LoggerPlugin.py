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

import logging

from plugins.Plugin import *

class LoggerPlugin(Plugin):
    """
    Logs all messages to file.
    """
    priority = 0
    name = "LoggerPlugin"
    author = "Olle Johansson"
    description = "Message logger plugin."
    commands = [
        dict(
            command = [''],
            handler = 'handle_message',
            onevents = ['SentMessage', 'Message'],
        )
    ]

    def setup(self):
        """
        Setup method which is called once before any triggers methods are called.
        """
        self.log = logging.getLogger('message_logger')
        self.log.setLevel(logging.INFO)
        ch = logging.FileHandler('extras/messages.log', encoding='UTF-8')
        formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        ch.setFormatter(formatter)
        self.log.addHandler(ch)

    def handle_message(self, shout, command, comobj):
        """
        Method called on every new message received.
        """
        msg = "%s: %s" % (shout.name, shout.text)
        print "Message:", msg
        self.log.info(msg)
        return shout

