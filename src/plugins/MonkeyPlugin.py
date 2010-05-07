# -*- coding: utf-8 -*-

import random

from plugins.Plugin import *
from utils.utilities import *

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
            command = [u'!apa', u'!monkey'],
            handler = 'show_text',
            onevents=['Message'],
            text = [u'@({-_-})@'],
            nick = "Apa",
        ),
        dict(
            command = [u'!tits', u'!boobs', u'!boobies'],
            handler = 'show_text',
            onevents=['Message'],
            text = [u'( . )( . )', u'( . Y .)', u"(./\.)", u"( o Y o )", u"( + )( + )", u"(*)(*)", u"(@)(@)", u"{ O }{ O }", u"( ^ )( ^ )", u"(oYo)", u"\o/\o/"],
        ),
        dict(
            command = [u'!fallos', u'!snopp', '!kuk', u'!penis', u'!dick', u'!cock'],
            handler = 'show_cock',
            onevents=['Message'],
        ),
        dict(
            command = [u'!koala'],
            handler = 'show_text',
            onevents=['Message'],
            text = [u"@( * O * )@"],
        ),
        dict(
            command = [u'!fisk', u'!fish'],
            handler = 'show_text',
            onevents=['Message'],
            text = [u"<`)))><", u"><(((('>", u"><>"],
        ),
        dict(
            command = [u'!sheep', u'!får'],
            handler = 'show_text',
            onevents=['Message'],
            text = [u"°l°(,,,,);", u"/o\*"],
        ),
        dict(
            command = [u'!spindel', u'!spider'],
            handler = 'show_text',
            onevents=['Message'],
            text = [u"///\oo/\\\\\\"],
        ),
        dict(
            command = [u'!cat', u'!katt'],
            handler = 'show_text',
            onevents=['Message'],
            text = [u"<(^.^)>", u"=^..^=", u"(>'.'<)"],
        ),
        dict(
            command = [u'!rose', u'!ros'],
            handler = 'show_text',
            onevents=['Message'],
            text = [u"@->-->---", u"@->-", u"@--,--'---", u"--------{---(@", u"@}}>-----"],
        ),
        dict(
            command = [u'!mus', u'!mouse'],
            handler = 'show_text',
            onevents=['Message'],
            text = [u'----{,_,">', u'<^__)~~'],
        ),
        dict(
            command = [u'!sword', u'!svärd'],
            handler = 'show_text',
            onevents=['Message'],
            text = [u"O==I======>", u"o==}=======>>", u"(===||:::::::::::::::>"],
        ),
        dict(
            command = [u'!snigel', u'!snail'],
            handler = 'show_text',
            onevents=['Message'],
            text = [u"__@/"],
        ),
        dict(
            command = [u'!coffee', u'!cup', u'!kaffe', u'!kopp'],
            handler = 'show_text',
            onevents=['Message'],
            text = [u"[_]3"],
        ),
        dict(
            command = [u'!ass', u'!arse', u'!arsle'],
            handler = 'show_text',
            onevents=['Message'],
            text = [u"(  )x(  )", u"(  )O(  )", u"(_O_)", u"(_*_)", u"{_x_}", u"(_Y_)", u"(_!_)", u"(__!__)"],
        ),
        dict(
            command = [u'!duck', u'!anka'],
            handler = 'show_text',
            onevents=['Message'],
            text = [u"\__o-", u"o<", u".\\/", u"{:V", u"{:<>", u"(:<>"],
        ),
    ]

    def show_cock(self, shout, command=None, comobj=None):
        """
        Display text from command.
        """
        text = u'8' + ''.ljust(random.randint(1, 10), '=') + u"D"
        self.bridge.send_and_shout(text, self.nick)

    def show_text(self, shout, command=None, comobj=None):
        """
        Display text from command.
        """
        try:
            nick = comobj['nick']
        except KeyError:
            nick = self.nick
        self.bridge.send_and_shout(random.choice(comobj['text']), nick)

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
    plug = MonkeyPlugin([bridge])
    plug.setup()
    print "Returned:", plug.handleShoutMessage(shout)

# Call the main function.
if __name__ == '__main__':
    main()
