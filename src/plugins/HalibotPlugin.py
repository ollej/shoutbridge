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

class HalibotPlugin(Plugin):
    name = "HalibotPlugin"
    author = "Olle Johansson"
    description = "A generic HALiBot plugin for miscellaneous support features."
    commands = [
        dict(
            command = ['!version'],
            handler = 'show_version',
            onevents = ['Message'],
        ),
        dict(
            command = ['!say'],
            handler = 'echo_message',
            onevents = ['XmppDirectMessage'],
        ),
        dict(
            command = ['!help me'],
            handler = 'show_text',
            onevents = ['Message'],
            text = ["I can't help you."],
        ),
        dict(
            command = ['!help'],
            handler = 'show_help',
            onevents = ['Message'],
            text = u"Write !help followed by the information you need help on. Use !listcommands to list all available commands.",
        ),
        dict(
            command = ['!listcommands', '!commands'],
            handler = 'list_commands',
            onevents = ['Message'],
        ),
        dict(
            command = ['!listplugins', '!plugins'],
            handler = 'list_plugins',
            onevents = ['Message'],
        ),
        dict(
            command = ['!jump'],
            handler = 'jump_room',
            onevents = ['XmppDirectMessage'],
        ),
        dict(
            command = ['!flipcoin', '!coinflip', '!coin', '!flip', '!toss'],
            handler = 'show_text',
            onevents = ['Message'],
            text = ['Heads', 'Tails'],
        ),
    ]

    def show_version(self, shout, command, comobj):
        """
        Print version and system information.
        """
        text = "%s %s (%s)" % (self.bridge.client_name, self.bridge.client_version,
                               self.bridge.get_os_info())
        self.bridge.send_and_shout(text, self.nick)

    def list_commands(self, shout, command, comobj):
        """
        List all available commands in all loaded Plugins.
        """
        commandlist = []
        for plugin_name, plugin in self.bridge.plugins.items():
            for com in plugin.commands:
                commandlist.extend(com['command'])
        self.bridge.send_and_shout("Available commands: %s" % ' '.join(commandlist), self.nick)

    def jump_room(self, shout, command, comobj):
        """
        Make bot jump to another jabber conference room.
        """
        text = shout.text.replace(command, '', 1).strip()
        (passwd, room) = text.split(' ', 1)
        if passwd != self.bridge.cfg.get('halibot_password'):
            return
        self.bridge.leave_room("Jumping to another room.")
        self.bridge.room = room
        self.bridge.join_room(room)

    def list_plugins(self, shout, command, comobj):
        """
        List all loaded Plugins.
        """
        self.bridge.send_and_shout("Loaded plugins: %s" % ' '.join(self.bridge.plugins.keys()), self.nick)

    def show_help(self, shout, command, comobj):
        """
        Show Plugin description on given plugin name.
        TODO: Shouldn't be case-sensitive.
        """
        help = shout.text.replace(command, '', 1).strip().lower()
        if help:
            self.logprint("Showing help for plugin:", help)
            for pname, p in self.bridge.plugins.items():
                if pname.lower() == help:
                    text = p.description
                    break
            if not text:
                text = "Plugin not found: %s" % help
        else:
            text = comobj['text']
        self.bridge.send_and_shout("%s: %s" % (shout.name, text), self.nick)

    def echo_message(self, shout, command, comobj):
        """
        Echos the message back out to the chat.
        """
        text = shout.text.replace(command, '', 1).strip()
        (passwd, text) = text.split(' ', 1)
        if passwd != self.bridge.cfg.get('halibot_password'):
            return
        self.bridge.send_and_shout(text, self.nick)
        

