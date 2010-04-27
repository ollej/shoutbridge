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

    def setup(self):
        """
        Setup method which is called once before any triggers methods are called.
        """
        self.d = Dicey()

    def handleXmppMessage(self, message):
        """
        Method called on every received XMPP message stanza.
        Message can be modified and must be returned.
        """
        body = getElStr(message.body)
        self.dice_roller(body)
        return message

    def handleShoutMessage(self, shout):
        """
        Method called on every new message from the Shoutbox.
        Shout message can be modified, and must be returned.
        """
        self.dice_roller(shout.text)
        return shout

    def dice_roller(self, text):
        """
        Parse message body and send message with dice roll.
        """
        self.logprint("DicePlugin: Handling message:", text)
        if self.command == '' or text.startswith(self.command):
            diestr = ''
            if text.find('DoD') >= 0:
                diestr = self.roll_character('DoD')
                self.bridge.send_and_shout(diestr, self.nick)
            else:
                diestr = self.d.replaceDieStrings(text, self.replace_roll)

    def roll_character(self, rpg):
        """
        Roll character for rpg.
        Currenty always rolls for DoD.
        """
        diestr = ''
        die = Die(6, 3)
        for roll in ['STY', 'KRO', 'STO', 'INT', 'KRA', 'SKI', 'KAR']:
            die.resetResult()
            die.roll()
            diestr += roll + ": " + str(die.result) + ' '
        return diestr

    def replace_roll(self, m):
        """
        Replace die rolls in text, and sends message/shout with result for each roll.
        """
        die = Die(m.group('die'), m.group('rolls'), m.group('op'), m.group('val'), m.group('type'))
        die.roll()
        str = die.getResultString()
        if int(m.group('rolls')) <= self.max_printed_rolls:
            str += " " + repr(die.list)
        self.bridge.send_and_shout(str, self.nick)
        return str

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
    plug = DicePlugin([shout])
    plug.setup()
    print "Returned:", plug.handleShoutMessage(shout)

# Call the main function.
if __name__ == '__main__':
    main()
