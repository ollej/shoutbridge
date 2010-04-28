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
    command = ''
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
        self.send_warning(body, message['nick'])

    def handleShoutMessage(self, shout):
        """
        Method called on every new message from the Shoutbox.
        """
        self.send_warning(shout.text, shout.name)

    def send_warning(self, text, nick):
        """
        Parse message body and send message with dice roll.
        """
        self.logprint("KraetyzPlugin: Handling message:")
        if nick == "Kraetyz" and text.lower().find("jag tycker") >= 0:
            self.bridge.send_and_shout("/me bannar Kraetyz för uttryckande av åsikt.", self.nick)

def main():
    import sys
    import string
    from time import time
    from Conf import Conf
    import Shoutbox
    cfg = Conf('config.ini', 'LOCAL')
    args = sys.argv
    msg = ' '.join(args[1:])
    shout = Shoutbox.Shout(1, 4711, 'Kraetyz', msg, time())
    bridge = FakeBridge()
    plug = KraetyzPlugin([bridge])
    plug.setup()
    print "Returned:", plug.handleShoutMessage(shout)

# Call the main function.
if __name__ == '__main__':
    main()
