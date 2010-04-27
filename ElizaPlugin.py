# -*- coding: utf-8 -*-

from Plugin import *
from utilities import *
import eliza

class ElizaPlugin(Plugin):
    """
    Eliza, the famous non-professional psychatrist.
    If someone writes a message like:
    Eliza, what is the meaning of life?
    This plugin will answer as Eliza, with some ingenious answer.

    Requires eliza.py from:
        http://www.jezuk.co.uk/cgi-bin/view/software/eliza
    """
    priority = 0
    name = "ElizaPlugin"
    author = "Olle Johansson"
    description = "Eliza, the psychatrist"
    command = "Eliza,"

    def setup(self):
        """
        Setup method which is called once before any triggers methods are called.
        """
        self.eliza = eliza.eliza()

    def handleXmppMessage(self, message):
        """
        Method called on every received XMPP message stanza.
        Message can be modified and must be returned.
        """
        body = getElStr(message.body)
        self.ask_eliza(body)
        return message

    def handleShoutMessage(self, shout):
        """
        Method called on every new message from the Shoutbox.
        Shout message can be modified, and must be returned.
        """
        self.ask_eliza(shout.text)
        return shout

    def ask_eliza(self, text):
        """
        Parse message body and send message with dice roll.
        """
        self.logprint("ElizaPlugin: Handling message:", text)
        if text.startswith(self.command):
            text = text[len(self.command):].strip()
            response = self.eliza.respond(text)
            if response:
                self.bridge.send_and_shout(response, "Eliza")

def main():
    import sys
    import string
    from time import time
    from Conf import Conf
    import Shoutbox
    cfg = Conf('config.ini', 'LOCAL')
    shout = Shoutbox.Shout(1, 4711, 'Test', 'Eliza, A quick brown fox...', time())
    plug = Plugin()
    plug.setup()
    print plug.handleShoutMessage(shout)

# Call the main function.
if __name__ == '__main__':
    main()
