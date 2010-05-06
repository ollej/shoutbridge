# -*- coding: utf-8 -*-

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
        tmpl = string.Template(random.choice(self.slapitems))
        if slapee and slapee.lower() != self.nick.lower():
            slap = tmpl.substitute(dict(slapper=shout.name, slapee=slapee))
            self.bridge.send_and_shout(slap, self.nick)

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
    plug = SlapPlugin([bridge])
    plug.setup()
    print "Returned:", plug.handleShoutMessage(shout)

# Call the main function.
if __name__ == '__main__':
    main()
