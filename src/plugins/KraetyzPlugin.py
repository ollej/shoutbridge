# -*- coding: utf-8 -*-

from plugins.Plugin import *
from utils.utilities import *

class KraetyzPlugin(Plugin):
    """
    Match texts from a list of users and returns a message.
    If any of the nicks in onsender writes a message that contains the text
    in textmatch, then the bot will send the text as a message, substituting
    %s for the nick of the sender.
    """
    priority = 0
    name = "KraetyzPlugin"
    author = "Olle Johansson <Olle@Johansson.com>"
    description = "Match texts from a list of users and returns a message."
    commands = [
        dict(
            command=[''],
            handler='send_warning',
            onsender = ['Kraetyz'],
            textmatch = 'jag tycker',
            text = u"/me bannar %s för uttryckande av åsikt.",
        ),
    ]

    def send_warning(self, text, nick, command, cmd):
        """
        Parse message body and send message with dice roll.
        """
        if nick in cmd['onsender'] and text.lower().find(cmd['textmatch']) >= 0:
            self.bridge.send_and_shout(cmd['text'] % (nick), self.nick)

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
