# -*- coding: utf-8 -*-

import commands
from plugins.Plugin import *
from utils.utilities import *

class FortunePlugin(Plugin):
    """
    Displays a short fortune message.
    Requires the fortune command line program.
    """
    priority = 0
    name = "FortunePlugin"
    author = "Olle Johansson <Olle@Johansson.com>"
    description = "Fortune cookie plugin."
    commands = [
        dict(
            command=['!fortune', '!kaka', '!sia'],
            handler='tell_fortune',
        ),
    ]
    max_length = 60

    def tell_fortune(self, text, nick, command, cmd):
        """
        Parse message body and send message with dice roll.
        """
        #newstr = commands.getoutput('fortune -a -s -n ' + str(self.max_length))
        newstr = commands.getoutput('fortune -a -s')
        if nick:
            newstr = nick + ': ' + newstr
        self.bridge.send_and_shout(newstr, self.nick)

def main():
    import sys
    import string
    from time import time
    from Conf import Conf
    import Shoutbox
    cfg = Conf('config.ini', 'LOCAL')
    args = sys.argv
    msg = ' '.join(args[1:])
    shout = Shoutbox.Shout(1, 4711, 'Test', msg, time())
    bridge = FakeBridge()
    plug = FortunePlugin([bridge])
    plug.setup()
    print "Returned:", plug.handleShoutMessage(shout)

# Call the main function.
if __name__ == '__main__':
    main()
