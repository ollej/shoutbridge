# -*- coding: utf-8 -*-

from Dice import *
from Plugin import *
from utilities import *

class DicePlugin(Plugin):
    """
    Makes die rolls requested by users.
    If someone writes a message like:
    !dice 3d6 
    This plugin will send a message of its own with the result:
    You rolled '3d6' and got: 9 [1, 3, 5]
    """
    priority = 0
    name = "DicePlugin"
    author = "Olle Johansson"
    description = "Dice roller plugin."
    command = '!dice'
    max_printed_rolls = 10
    nick = "Dicey"
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
    #('', []),


    def setup(self):
        """
        Setup method which is called once before any triggers methods are called.
        """
        self.d = Dicey()

    def handleXmppMessage(self, message):
        """
        Method called on every received XMPP message stanza.
        """
        body = getElStr(message.body)
        self.sender_nick = message['nick']
        self.dice_roller(body, message['nick'])

    def handleShoutMessage(self, shout):
        """
        Method called on every new message from the Shoutbox.
        """
        self.sender_nick = shout.name
        self.dice_roller(shout.text, shout.name)

    def dice_roller(self, text, nick):
        """
        Parse message body and send message with dice roll.
        """
        self.logprint("DicePlugin: Handling message:", text)
        if self.command == '' or text.startswith(self.command):
            diestr = ''
            words = text.split()
            rpg = words[1].lower()
            if rpg in self.rpgs:
                diestr = self.roll_character(rpg)
                diestr = words[1] + " - " + diestr
                diestr = self.prepend_sender(diestr)
                self.bridge.send_and_shout(diestr, self.nick)
            else:
                diestr = self.d.replaceDieStrings(text, self.replace_roll)

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
    plug = DicePlugin([bridge])
    plug.setup()
    print "Returned:", plug.handleShoutMessage(shout)

# Call the main function.
if __name__ == '__main__':
    main()
