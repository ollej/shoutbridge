# -*- coding: utf-8 -*-

from plugins.Plugin import *
from utils.utilities import *
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
    nick = "Eliza"
    commands = [
        dict(
            command=['Eliza,'],
            handler='ask_eliza',
            onevents=['Message'],
        ),
    ]

    def setup(self):
        """
        Setup method which is called once before any triggers methods are called.
        """
        self.eliza = eliza.eliza()

    def ask_eliza(self, shout, cmd, comobj):
        """
        Parse message body and send message with dice roll.
        """
        text = shout.text[len(cmd):].strip()
        response = self.eliza.respond(text)
        if response:
            self.bridge.send_and_shout(shout.name + ': ' + response, self.nick)

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
    plug = ElizaPlugin([bridge])
    plug.setup()
    print plug.handleShoutMessage(shout)

# Call the main function.
if __name__ == '__main__':
    main()
