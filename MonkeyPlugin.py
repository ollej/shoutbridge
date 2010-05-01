# -*- coding: utf-8 -*-

import random

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
    nick = "HALiBot"
    commands = [
        dict(
            command = ['!apa', '!monkey'],
            handler = 'show_text',
            text = [u'@({-_-})@'],
            nick = "Apa",
        ),
        dict(
            command = ['!tits', '!boobs', '!boobies'],
            handler = 'show_text',
            text = [u'( . )( . )', u'( . Y .)'],
        ),
        dict(
            command = ['!fallos', '!snopp', '!penis'],
            handler = 'show_text',
            text = [u"8========D"],
        ),
        dict(
            command = ['!koala'],
            handler = 'show_text',
            text = [u"@( * O * )@"],
        ),
        dict(
            command = ['!fisk', '!fish'],
            handler = 'show_text',
            text = [u"<`)))><", u"><(((('>", u"><>"],
        ),
        dict(
            command = ['!sheep', '!får'],
            handler = 'show_text',
            text = [u"°l°(,,,,);", u"/o\*"],
        ),
        dict(
            command = ['!spindel', '!spider'],
            handler = 'show_text',
            text = [u"///\oo/\\\\\\"],
        ),
        dict(
            command = ['!cat', '!katt'],
            handler = 'show_text',
            text = [u"<(^.^)>", u"=^..^="],
        ),
        dict(
            command = ['!rose', '!ros'],
            handler = 'show_text',
            text = [u"@->-->---", u"@->-", u"@--,--'---", u"--------{---(@", u"@}}>-----"],
        ),
        dict(
            command = ['!mus', '!mouse'],
            handler = 'show_text',
            text = [u'----{,_,">', u'<^__)~~'],
        ),
        dict(
            command = ['!sword', '!svärd'],
            handler = 'show_text',
            text = [u"o==}=======>>", u"(===||:::::::::::::::>"],
        ),
        dict(
            command = ['!snigel', '!snail'],
            handler = 'show_text',
            text = [u"__@/"],
        ),
    ]

    def show_text(self, text, nick, command=None, cmd=None):
        """
        Display text from command.
        """
        try:
            nick = cmd['nick']
        except KeyError:
            nick = self.nick
        self.bridge.send_and_shout(random.choice(cmd['text']), nick)

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
