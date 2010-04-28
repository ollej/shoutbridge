# -*- coding: utf-8 -*-

import random
from Plugin import *
from utilities import *

class EvaEmmaPlugin(Plugin):
    """
    EvaEmma bot prints a random quote from EvaEmma Andersson.
    """
    priority = 0
    name = "EvaEmmaPlugin"
    author = "Olle Johansson <Olle@Johansson.com>"
    description = "EvaEmma bot prints a random quote from EvaEmma Andersson."
    command = '!evaemma'
    nick = "EvaEmma"

    def setup(self):
        """
        Setup method which is called once before any triggers methods are called.
        """
        self.quotes = read_file("extras/evaemma.dat", "%")

    def handleXmppMessage(self, message):
        """
        Method called on every received XMPP message stanza.
        """
        body = getElStr(message.body)
        self.send_quote(body, message['nick'])

    def handleShoutMessage(self, shout):
        """
        Method called on every new message from the Shoutbox.
        """
        self.send_quote(shout.text, shout.name)

    def send_quote(self, text, nick):
        """
        Parse message body and send message with dice roll.
        """
        self.logprint("EvaEmmaPlugin: Handling message:", nick, text)
        if not self.quotes:
            return
        if self.command == '' or text.startswith(self.command):
            self.bridge.send_and_shout(random.choice(self.quotes), self.nick)

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
    plug = EvaEmmaPlugin([bridge])
    plug.setup()
    print "Returned:", plug.handleShoutMessage(shout)

# Call the main function.
if __name__ == '__main__':
    main()
