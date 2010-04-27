# -*- coding: utf-8 -*-

from Plugin import *
from utilities import *

class MonkeyPlugin(Plugin):
    """
    Displays a monkey.
    """
    priority = 0
    name = "MonkeyPlugin"
    author = "Olle Johansson <Olle@Johansson.com>"
    description = "Simple plugin to display a monkey."
    command = '!apa'
    nick = "Apa"

    def setup(self):
        """
        Setup method which is called once before any triggers methods are called.
        """
        pass

    def handleXmppMessage(self, message):
        """
        Method called on every received XMPP message stanza.
        """
        body = getElStr(message.body)
        self.monkey(body)

    def handleShoutMessage(self, shout):
        """
        Method called on every new message from the Shoutbox.
        """
        self.monkey(shout.text)

    def monkey(self, text):
        """
        Parse message body and send message with dice roll.
        """
        self.logprint("MonkeyPlugin: Handling message:")
        if self.command == '' or text.startswith(self.command):
            self.bridge.send_and_shout("@({-_-})@", self.nick)

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
    plug = MonkeyPlugin([bridge])
    plug.setup()
    print "Returned:", plug.handleShoutMessage(shout)

# Call the main function.
if __name__ == '__main__':
    main()
