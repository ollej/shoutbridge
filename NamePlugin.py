# -*- coding: utf-8 -*-

from datetime import date
from Plugin import *
from utilities import *

class NamePlugin(Plugin):
    """
    Returns the names of today in the Swedish calendar.
    """
    priority = 0
    name = "NamePlugin"
    author = "Olle Johansson <Olle@Johansson.com>"
    description = "Plugin that prints names from the Swedish calendar."
    commands = [
        dict(
            command=['!dagensnamn'],
            handler='send_names',
        ),
    ]
    names = []

    def setup(self):
        """
        Setup method which is called once before any triggers methods are called.
        """
        self.names = read_file("extras/names.dat")

    def send_names(self, text, nick, command, cmd):
        """
        Parse message body and send message with dice roll.
        """
        d = date.today()
        day = int(d.strftime("%j")) - 1
        names = self.names[day]
        self.bridge.send_and_shout(names, self.nick)

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
    plug = NamePlugin([bridge])
    plug.setup()
    print "Returned:", plug.handleShoutMessage(shout)

# Call the main function.
if __name__ == '__main__':
    main()
