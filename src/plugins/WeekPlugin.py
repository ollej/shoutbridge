# -*- coding: utf-8 -*-

from datetime import date

from plugins.Plugin import *
from utils.utilities import *

class WeekPlugin(Plugin):
    """
    Returns the ISO week number.
    """
    priority = 0
    name = "WeekPlugin"
    author = "Olle Johansson <Olle@Johansson.com>"
    description = "Simple plugin to display current ISO week number."
    commands = [
        dict(
            command=['!week', '!vecka'],
            handler='send_weeknr',
        ),
    ]

    def send_weeknr(self, text, nick, command, cmd):
        """
        Return the current ISO week number.
        """
        (isoyear, isoweek, isoweekday) = date.today().isocalendar()
        self.bridge.send_and_shout("Vecka: " + str(isoweek), self.nick)

def main():
    import sys
    import string
    from time import time
    from Conf import Conf
    import Shoutbox
    cfg = Conf('config.ini', 'LOCAL')
    args = sys.argv
    msg = unicode(' '.join(args[1:]), 'utf-8')
    shout = Shoutbox.Shout(1, 4711, 'Test', msg, time())
    bridge = FakeBridge()
    plug = WeekPlugin([bridge])
    plug.setup()
    print "Returned:", plug.handleShoutMessage(shout)

# Call the main function.
if __name__ == '__main__':
    main()
