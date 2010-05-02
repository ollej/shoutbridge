# -*- coding: utf-8 -*-

from Plugin import *
from utilities import *

class KraetyzPlugin(Plugin):
    """
    If Kraetyz writes an opinion, he will be fake insta-banned.
    """
    priority = 0
    name = "KraetyzPlugin"
    author = "Olle Johansson <Olle@Johansson.com>"
    description = "If Kraetyz writes an opinion, he will be fake insta-banned."
    commands = [
        dict(
            command=[''],
            handler='send_warning',
        ),
    ]

    def send_warning(self, text, nick, command, cmd):
        """
        Parse message body and send message with dice roll.
        """
        if nick == "Kraetyz" and text.lower().find("jag tycker") >= 0:
            self.bridge.send_and_shout(u"/me bannar Kraetyz för uttryckande av åsikt.", self.nick)

def main():
    import sys
    import string
    from time import time
    from Conf import Conf
    import Shoutbox
    cfg = Conf('config.ini', 'LOCAL')
    args = sys.argv
    msg = unicode(' '.join(args[1:]), 'utf-8')
    shout = Shoutbox.Shout(1, 4711, 'Kraetyz', msg, time())
    bridge = FakeBridge()
    plug = KraetyzPlugin([bridge])
    plug.setup()
    print "Returned:", plug.handleShoutMessage(shout)

# Call the main function.
if __name__ == '__main__':
    main()
