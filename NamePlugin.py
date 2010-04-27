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
    command = '!namn'
    nick = "Bot"
    names = []

    def setup(self):
        """
        Setup method which is called once before any triggers methods are called.
        """
        self.names = read_file("extras/names.dat")

    def handleXmppMessage(self, message):
        """
        Method called on every received XMPP message stanza.
        """
        body = getElStr(message.body)
        self.send_names(body)

    def handleShoutMessage(self, shout):
        """
        Method called on every new message from the Shoutbox.
        """
        self.send_names(shout.text)

    def send_names(self, text):
        """
        Parse message body and send message with dice roll.
        """
        self.logprint("NamePlugin: Handling message.")
        if self.command == '' or text.startswith(self.command):
            d = date.today()
            day = int(d.strftime("%j")) - 1
            names = self.names[day]
            self.bridge.send_and_shout(names)

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