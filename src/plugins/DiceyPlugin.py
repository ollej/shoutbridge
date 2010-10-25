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
        self.d = Dicey()

    def dice_roller(self, shout, command, comobj):
        """
        Parse message body and send message with dice roll.
        """
        self.sender_nick = shout.name
        diestr = ''
        words = shout.text.split()
        try:
            rpg = words[1].lower()
        except IndexError:
            return
        if rpg in self.rpgs:
            diestr = self.roll_character(rpg)
            diestr = words[1] + " - " + diestr
            diestr = shout.name + ': ' + diestr
            self.bridge.send_and_shout(diestr, self.nick)
        else:
            diestr = self.d.replaceDieStrings(shout.text, self.replace_roll, self.max_responses)

    def roll_character(self, rpg):
        """
        Roll character for rpg.
        Currenty always rolls for DoD.
        """
        diestr = ''
        for name, roll in self.rpgs[rpg]:
            die = Die(roll)
            die.roll(True)
            diestr += name + ": " + str(die.result) + ' '
        return diestr

    def replace_roll(self, m):
        """
        Replace die rolls in text, and sends message/shout with result for each roll.
        """
        die = Die(int(m.group('die')), m.group('rolls'), m.group('op'), m.group('val'), m.group('rolltype'), m.group('seltype'), m.group('nrofresults'))
        die.roll()
        newstr = die.getResultString()
        if not m.group('rolls'):
            rolls = 1
        else:
            rolls = int(m.group('rolls'))
        if rolls > 1 and rolls <= self.max_printed_rolls:
            newstr += " " + repr(die.list)
            if die.op and die.val > 0:
                newstr += " " + die.op + " " + str(die.val)
        newstr = self.prepend_sender(newstr)
        self.bridge.send_and_shout(newstr, self.nick)
        return newstr


