# -*- coding: utf-8 -*-

from plugins.Plugin import *

class HelloWorldPlugin(Plugin):
    name = "HelloWorldPlugin"
    author = "Your Name"
    description = "A simple Hello World plugin."
    commands = [
        dict(
            command = ['!hello'],
            handler = 'hello_world',
        )
    ]

    def hello_world(self, text, nick, command, cmd):
        self.bridge.send_and_shout("Hello World!", self.nick)

def main():
    import sys
    import string
    from time import time
    from Conf import Conf
    import Shoutbox
    cfg = Conf('config.ini', 'LOCAL')
    args = sys.argv
    msg = unicode(' '.join(args[1:]), 'utf-8')
    shout = Shoutbox.Shout(1, 4711, 'Test', msg, time())
    bridge = FakeBridge()
    plug = HelloWorldPlugin([bridge])
    plug.setup()
    print "Returned:", plug.handleShoutMessage(shout)

# Call the main function.
if __name__ == '__main__':
    main()

