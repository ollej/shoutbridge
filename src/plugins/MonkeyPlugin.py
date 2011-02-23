# -*- coding: utf-8 -*-

"""
The MIT License

Copyright (c) 2010 Olle Johansson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

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
            text = [u"///\oo/\\\\\\", u"///\·::·/\\\\\\", u"///\oııo/\\\\\\"],
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
        dict(
            command = [u'!cthulhu'],
            handler = 'show_text',
            onevents=['Message'],
            text = [u'\(;,;)/)'],
        ),
    ]

