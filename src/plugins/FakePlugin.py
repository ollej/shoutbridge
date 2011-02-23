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

class FakePlugin(Plugin):
    """
    Simple plugin for some fake commands.
    """
    priority = 0
    name = "FakePlugin"
    author = "Olle Johansson <Olle@Johansson.com>"
    description = "Simple plugin for some fake commands."
    nick = 'HALiBot'
    commands = [
        dict(
            command = [u'!kickban'],
            handler = 'fake_command',
            func    = 'kickban',
            onevents=['Message'],
        ),
        dict(
            command = [u'!kick'],
            handler = 'fake_command',
            func    = 'kick',
            onevents=['Message'],
        ),
        dict(
            command = [u'!ban'],
            handler = 'fake_command',
            func    = 'ban',
            onevents=['Message'],
        ),
    ]

    def fake_command(self, shout, command=None, comobj=None):
        text = self.strip_command(shout.text, command)
        try:
            (user, reason) = self.get_name(text)
            if user.lower() == self.nick.lower():
                user = shout.name
            func = getattr(self, "cmd_" + comobj['func'])
            if func:
                func(user, reason)
            else:
                self.send_message(u"Error: no command found: %s" % command)
        except ValueError:
            self.send_message(u"Please specify user.")

    def cmd_kickban(self, user, reason):
        """
        A fake kickban message.
        """
        self.send_kick(user, reason)
        self.send_ban(user)

    def cmd_kick(self, user, reason):
        """
        A fake kick message.
        """
        self.send_kick(user, reason)

    def cmd_ban(self, user, reason):
        """
        A fake ban message.
        """
        self.send_ban(user, reason)

    def send_ban(self, user, reason=""):
        if reason:
            message = "%s is banned with the reason: %s" % (user, reason)
        else:
            message = "%s is banned" % user
        self.bridge.send_and_shout(message, self.nick)

    def send_kick(self, user, reason=""):
        if reason:
            message = "%s is kicked out of the channel with the reason: %s" % (user, reason)
        else:
            message = "%s is kicked out of the channel" % user
        self.bridge.send_and_shout(message, self.nick)

