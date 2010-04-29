# -*- coding: utf-8 -*-

from datetime import date
from Plugin import *
from utilities import *

class WeekPlugin(Plugin):
    """
    Returns the ISO week number.
    """
    priority = 0
    name = "WeekPlugin"
    author = "Olle Johansson <Olle@Johansson.com>"
    description = "Simple plugin to display current ISO week number."
    command = '!vecka'
    nick = "HALiBot"

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
        self.send_weeknr(body)

    def handleShoutMessage(self, shout):
        """
        Method called on every new message from the Shoutbox.
        """
        self.send_weeknr(shout.text)

    def send_weeknr(self, text):
        """
        Parse message body and send message with dice roll.
        """
        self.logprint("WeekPlugin: Handling message.")
        if self.command == '' or text.startswith(self.command):
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
    msg = ' '.join(args[1:])
    shout = Shoutbox.Shout(1, 4711, 'Test', msg, time())
    bridge = FakeBridge()
    plug = WeekPlugin([bridge])
    plug.setup()
    print "Returned:", plug.handleShoutMessage(shout)

# Call the main function.
if __name__ == '__main__':
    main()
