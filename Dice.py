# -*- coding: utf-8 -*-

#! /usr/bin/python

import re
import random

class Die:
    """Defines the information for a die roll."""
    dice_pattern = re.compile(r"""
        (?P<dieroll>
        (?P<rolltype>Ob|Open)?              # Type of dieroll
        (?P<rolls>\d+)?                 # Number of dice to roll
        [d|D|t|T]                       # Start of diename
        (?P<die>100|20|4|6|8|10|12|2)   # How many sides on the die
        (                               # Start of operation
            (?P<op>\+|\-)               # Add or subtract?
            (?P<val>\d+)                # Value to add/subtract 
        )?                              # Operation not necessary
        )
        """, re.VERBOSE)

    def __init__(self, die, rolls=1, op='', val=0, rolltype=''):
        # If die is a string, parse it to get all values.
        if type(die).__name__ == 'str':
            (die, rolls, op, val, rolltype) = self.parseDice(die)
        self.die = int(die) if die else 0
        self.rolls = int(rolls) if rolls else 1

        # Don't allow more than 1000 rolls.
        if self.rolls > 1000:
            self.rolls = 1
        self.op = op if op in ('+', '-') else ''
        self.val = int(val) if val else 0
        self.rolltype = rolltype if rolltype and rolltype in ('Ob', 'Open') else ''
        if self.rolls > 1:
            self.dieroll = self.rolltype + str(self.rolls) + 'd' + str(self.die)
        else:
            self.dieroll = self.rolltype + 'd' + str(self.die)
        if op != '' and val > 0:
            self.dieroll += self.op + str(self.val)
        self.result = 0
        self.list = []

    def parseDice(self, die):
        m = re.search(self.dice_pattern, die)
        if m:
            return (m.group('die'), m.group('rolls'), m.group('op'), m.group('val'), m.group('rolltype'))
        else:
            return int(die)

    def roll(self, reset=None):
        """Rolls the die according to the set values, sets self.roll and returns it."""
        if reset:
            self.resetResult()
        if not self.die in (2, 4, 6, 8, 10, 12, 20, 100): return False
        if self.op and self.op not in ('+', '-'): return False
        if self.rolltype and self.rolltype not in ('Ob', 'Open'): return False
        for i in range(self.rolls):
            self.result += self.randomize()
        if self.op == '+':
            self.result += self.val
        elif self.op == '-':
            self.result -= self.val
        return self.result

    def randomize(self):
        if self.rolltype == 'Ob':
            return self.rollObDie(self.die)
        elif self.rolltype == 'Open':
            return self.rollOpenDie(self.die)
        else:
            return self.rollDie(self.die)

    def rollOpenDie(self, sides):
        result = self.rollDie(sides)
        if result == sides:
            return result + self.rollOpenDie(sides)
        else:
            return result

    def rollObDie(self, sides):
        result = self.rollDie(sides)
        if result == sides:
            self.list.pop()
            return self.rollObDie(sides) + self.rollObDie(sides)
        else:
            return result

    def rollDie(self, sides):
        result = random.randint(1, sides) 
        self.list.append(result)
        return result

    def resetResult(self):
        self.result = 0

    def getResultString(self):
        return unicode("Resultatet av tärningsslaget " + str(self.dieroll) + " blev: " + str(self.result), 'utf-8')
        #return "You rolled " + str(self.dieroll) + " and got: " + str(self.result)
        
class Dicey:
    """Dicey can replace die roll text in strings with results of the rolls."""

    def replaceDieRoll(self, m):
        """Replaces die rolls with html and the result of the roll."""
        die = Die(int(m.group('die')), m.group('rolls'), m.group('op'), m.group('val'), m.group('rolltype'))
        die.roll()
        html = "<div class='dieroll'>"
        html += die.dieroll
        html += "<img src='http://www.rollspel.nu/forum/images/graemlins/wrnu/t" + str(die.die) + ".gif' alt=" + str(die.dieroll) + " title=" + str(die.dieroll) + ">"
        html += "<br />" + die.getResultString()
        html += "<br />: All die rolls: " + str(die.list)
        html += "</div>"
        return html

    def replaceDieStrings(self, diestring, roll_call=None):
        """Finds all die roll texts in string and replaces them with result information."""
        if not roll_call:
            roll_call = self.replaceDieRoll
        newstring = re.sub(Die.dice_pattern, roll_call, diestring)
        return newstring

if __name__ == '__main__':
    string = "asdf d20+100 asdfasf d12-100 asdf OpenD20 D8 d3 Ob3T6 d4 t10 d100 d12"
    print "Original string: " + string
    d = Dicey()
    newstring = d.replaceDieStrings(string)
    print "Result string: " + newstring

