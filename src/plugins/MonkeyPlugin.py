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
            text = [u"///\oo/\\\\\\", u"///\·::·/\\\\\\"],
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
        dict(
            command = [u'!wave', u'!vinka'],
            handler = 'show_text',
            onevents=['Message'],
            text = [u"o/"],
        ),
        dict(
            command = [u'!love', u'!heart', u'!hjärta', u'!kärlek', u'!älska'],
            handler = 'show_text',
            onevents=['Message'],
            text = [u"<3", u"♥"],
        ),
        dict(
            command = [u'!cartman', '!southpark'],
            handler = 'show_text',
            onevents=['Message'],
            text = [u"(>_<)", u"(>.<)"],
        ),
        dict(
            command = [u'!butterfly', u'!fjäril'],
            handler = 'show_text',
            onevents=['Message'],
            text = [u"Ƹ̵̡Ӝ̵̨̄Ʒ", u">;<", u">;"],
        ),
        dict(
            command = [u'!alligator', u"!crocodile", u"!krokodil"],
            handler = 'show_text',
            onevents=['Message'],
            text = [u"^^^^^U^^^U^=___"],
        ),
        dict(
            command = [u'!santa', u"!santaclaus", u"!rudolph", u"!christmas", u"!sleigh", u"!tomte", u"!tomten", u"!jultomten", u"!jul"],
            handler = 'show_text',
            onevents=['Message'],
            text = [u'"o"/#\ "o"/#\ "o"/#\ ._(##\--/)`'],
        ),
        dict(
            command = [u'!snowman', u"!snögubbe"],
            handler = 'show_text',
            onevents=['Message'],
            text = [u'☃'],
        ),
    ]

    def show_cock(self, shout, command=None, comobj=None):
        """
        Display text from command.
        """
        text = u'8' + ''.ljust(random.randint(1, 10), '=') + u"D"
        self.bridge.send_and_shout(text, self.nick)


