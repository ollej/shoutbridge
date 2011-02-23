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

from Dice import *
from plugins.Plugin import *
from utils.utilities import *

class DiceyPlugin(Plugin):
    """
    Makes die rolls requested by users.
    If someone writes a message like:
    !dice 3d6 
    This plugin will send a message of its own with the result:
    You rolled '3d6' and got: 9 [1, 3, 5]
    """
    priority = 0
    name = "DiceyPlugin"
    author = "Olle Johansson"
    description = "Dice roller plugin."
    max_printed_rolls = 10
    max_responses = 5
    die_list = (2, 4, 6, 8, 10, 12, 20, 100)
    roll_string = "%(dieroll)s (%(result)s %(list)s) = %(sorf)s Successes"
    nick = "Dicey"
    commands = [
        dict(
            command=['!dicey', '!dice', '!roll', '!rulla', u'!tärning', '!kasta'],
            handler='dice_roller',
            onevents=['Message'],
        ),
    ]
    rpgs = dict([
        ('dod', [
            ('STY', '3d6'),
            ('KRO', '3d6'),
            ('STO', '3d6'),
            ('INT', '3d6'),
            ('KRA', '3d6'),
            ('SKI', '3d6'),
            ('KAR', '3d6'),
        ]),
        ('dnd', [
            ('STR', '4d6h3'),
            ('CON', '4d6h3'),
            ('DEX', '4d6h3'),
            ('INT', '4d6h3'),
            ('WIS', '4d6h3'),
            ('CHA', '4d6h3'),
        ]),
        ('eon', [
            (u'STY', '3d6'),
            (u'TÅL', '3d6'),
            (u'RÖR', '3d6'),
            (u'PER', '3d6'),
            (u'PSY', '3d6'),
            (u'VIL', '3d6'),
            (u'BIL', '3d6'),
            (u'SYN', '3d6'),
            (u'HÖR', '3d6'),
        ]),
        ('twerps', [
            ('Styrka', '1d10'),
        ]),
    ])

    def setup(self):
        """
        Setup method which is called once before any triggers methods are called.
        """
        self.d = Dicey(die_list=self.die_list, roll_string=self.roll_string)

    def dice_roller(self, shout, command, comobj):
        """
        Parse message body and send message with dice roll.
        """
        diestr = ''
        text = self.strip_command(shout.text, command)
        (rpg, rest) = self.get_name(text)
        #self.logprint("rpg:", rpg, "rest", rest)
        if rpg.lower() in self.rpgs:
            diestr = u"%s - %s" % (rpg, self.roll_character(rpg.lower()))
            self.send_message(diestr)
        else:
            diestr = self.d.replaceDieStrings(shout.text, roll_call=self.send_roll, die_list=self.die_list, max_responses=self.max_responses, roll_string=self.roll_string)
            #diestr = self.d.replaceDieStrings(shout.text, self.replace_roll, self.max_responses)

    def roll_character(self, rpg):
        """
        Roll character for rpg.
        Currenty always rolls for DoD.
        """
        diestr = ''
        for name, roll in self.rpgs[rpg]:
            die = Die(roll)
            die.roll(True)
            diestr += u"%s: %s " % (name, die.result)
        return diestr

    def send_roll(self, m):
        newstr = self.d.replaceDieRoll(m)
        # Ugly hack: If not using success, strip success info from string.
        if not m.group('success'):
            s = " = 0 Successes"
            if newstr.endswith(s):
                newstr = newstr[:-len(s)]
        self.send_message(newstr)
        return newstr

