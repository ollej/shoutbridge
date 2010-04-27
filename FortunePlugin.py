# -*- coding: utf-8 -*-

import commands
from Plugin import *
from utilities import *

class FortunePlugin(Plugin):
    """
    Displays a short fortune message.
    Requires the fortune command line program.
    """
    priority = 0
    name = "FortunePlugin"
    author = "Olle Johansson <Olle@Johansson.com>"
    description = "Fortune cookie plugin."
    command = '!fortune'
    nick = "Fortune"
    max_length = 60

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
        self.tell_fortune(body)
        return message

    def handleShoutMessage(self, shout):
        """
        Method called on every new message from the Shoutbox.
        """
        self.tell_fortune(shout.text)
        return shout

    def tell_fortune(self, text):
        """
        Parse message body and send message with dice roll.
        """
        self.logprint("FortunePlugin: Handling message:", text)
        if self.command == '' or text.startswith(self.command):
            newstr = commands.getoutput('fortune -s -n ' + str(self.max_length))
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
