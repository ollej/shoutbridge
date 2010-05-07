# -*- coding: utf-8 -*-

from plugins.Plugin import *

class HalibotPlugin(Plugin):
    name = "HalibotPlugin"
    author = "Olle Johansson"
    description = "A generic HALiBot plugin for miscellaneous support features."
    passwd = "abcd1234"
    commands = [
        dict(
            command = ['!version'],
            handler = 'show_version',
            onevents = ['Message'],
        ),
        dict(
            command = ['!say'],
            handler = 'echo_message',
            onevents = ['XmppPrivateMessage'],
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
            onevents = ['XmppPrivateMessage'],
        ),
    ]

    def show_version(self, shout, command, comobj):
        """
        Print version and system information.
        """
        text = "%s %s (%s)" % (self.bridge.client_name, self.bridge.client_version,
                               self.bridge.get_os_info())
        self.bridge.send_and_shout(text, self.nick)

    def echo_message(self, shout, command, comobj):
        """
        Echos text given.
        """
        text = shout.text.replace(command, '', 1).strip()
        (passwd, room) = text.split(' ', 1)
        if passwd != self.passwd:
            return
        self.bridge.send_and_shout(shout.text, self.nick)

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
        if passwd != self.passwd:
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
        help = shout.text.replace(command, '', 1).strip()
        if help:
            try:
                self.logprint("Showing help for plugin:", help)
                plugin = self.bridge.plugins[help] 
            except KeyError:
                text = "Plugin not found: %s" % help
            else:
                text = plugin.description
        else:
            text = comobj['text']
        self.bridge.send_and_shout("%s: %s" % (shout.name, text), self.nick)

def main():
    import sys
    import string
    from time import time
    from utils.Conf import Conf
    import shoutbox.Shoutbox
    cfg = Conf('config.ini', 'LOCAL')
    args = sys.argv
    msg = unicode(' '.join(args[1:]), 'utf-8')
    shout = shoutbox.Shoutbox.Shout(1, 4711, 'Test', msg, time())
    bridge = FakeBridge()
    plug = HalibotPlugin([bridge])
    plug.setup()
    print "Returned:", plug.handleShoutMessage(shout)

# Call the main function.
if __name__ == '__main__':
    main()

