# -*- coding: utf-8 -*-

#! /usr/bin/python

import re
import random

class Die(object):
    """
    Defines the information for a die roll.
    TODO: 4d6h3 for rolling 4 d6 dice and choosing the three highest.
    """
    die = 0
    rolls = 0
    op = ''
    val = 0
    rolltype = ''
    seltype = None
    nrofresults = None
    result = 0
    die_list = (2, 4, 6, 8, 10, 12, 20, 100)
    max_rolls = 1000
    list = []

    dice_pattern = re.compile(r"""
        (?P<dieroll>
        (?P<rolltype>Ob|Open)?          # Type of dieroll
        (?P<rolls>\d+)?                 # Number of dice to roll
        [d|D|t|T]                       # Start of diename
        (?P<die>\d+)                    # How many sides on the die
        (
            (?P<seltype>[hHlL])         # Roll selector, h = highest
            (?P<nrofresults>\d+)        # Nr of results
        )?
        (                               # Start of operation
            (?P<op>\+|\-)               # Add or subtract?
            (?P<val>\d+)                # Value to add/subtract 
        )?                              # Operation not necessary
        )
        """, re.VERBOSE | re.IGNORECASE)

    def __init__(self, die, rolls=1, op='', val=0, rolltype='', 
                 seltype=None, nrofresults=None, die_list=None, max_rolls=None):
        # If die is a string, parse it to get all values.
        if type(die).__name__ == 'str':
            (die, rolls, op, val, rolltype, seltype, nrofresults) = self.parseDice(die)
        self.die = int(die) if die else 0
        self.rolls = int(rolls) if rolls else 1
        if seltype:
            self.seltype = seltype.lower()
        if nrofresults:
            self.nrofresults = int(nrofresults)
        if die_list is not None:
            self.die_list = die_list
        if max_rolls:
            self.max_rolls = max_rolls

        # Don't allow more than 1000 rolls.
        if self.rolls > self.max_rolls:
            self.rolls = 1
        self.op = op if op in ('+', '-') else ''
        self.val = int(val) if val else 0
        self.rolltype = rolltype if rolltype and rolltype in ('Ob', 'Open') else ''
        if self.rolls > 1:
            self.dieroll = self.rolltype + str(self.rolls) + 'd' + str(self.die)
        else:
            self.dieroll = self.rolltype + 'd' + str(self.die)
        if seltype and nrofresults > 0:
            self.dieroll += seltype + str(nrofresults)
        if op and val > 0:
            self.dieroll += self.op + str(self.val)
        self.result = 0
        self.list = []

    def parseDice(self, die):
        m = re.search(self.dice_pattern, die)
        if m:
            return (m.group('die'), m.group('rolls'), m.group('op'), m.group('val'), m.group('rolltype'), m.group('seltype'), m.group('nrofresults'))
        else:
            return int(die)

    def roll(self, reset=None):
        """Rolls the die according to the set values, sets self.roll and returns it."""
        if reset:
            self.resetResult()
        print "die_list", self.die_list, "die", self.die
        if self.die_list and self.die not in self.die_list: return False
        if self.op and self.op not in ('+', '-'): return False
        if self.rolltype and self.rolltype not in ('Ob', 'Open'): return False

        # Roll dice
        for i in range(self.rolls):
            self.result += self.randomize()

        # Add modifiers.
        if self.op == '+':
            self.result += self.val
        elif self.op == '-':
            self.result -= self.val

        # Select results
        if self.seltype and self.nrofresults > 0:
            self.list = self.selectResults(self.seltype, self.nrofresults)
            self.calculateResult()

        return self.result

    def randomize(self):
        if self.rolltype == 'Ob':
            return self.rollObDie(self.die)
        elif self.rolltype == 'Open':
            return self.rollOpenDie(self.die)
        else:
            return self.rollDie(self.die)

    def calculateResult(self):
        # Recalculate result
        self.result = 0
        for v in self.list:
            self.result += v

    def selectResults(self, seltype, nrofresults):
        nrofresults = int(nrofresults)
        if seltype == 'h':
            results = self.getHighest(self.list, nrofresults)
        elif seltype == 'l':
            results = self.getLowest(self.list, nrofresults)
        return results

    def getHighest(self, lst, count):
        """
        Return the count highest items from lst.
        """
        lst.sort()
        highest = lst[-count:]
        highest.reverse()
        return highest

    def getLowest(self, lst, count):
        """
        Return the count lowest items from lst.
        """
        lst.sort()
        lst.reverse()
        lowest = lst[-count:]
        lowest.reverse()
        return lowest

    def rollOpenDie(self, sides):
        """
        Roll an open die. If the roll is the highest value, roll again and add the result.
        """
        result = self.rollDie(sides)
        if result == sides:
            return result + self.rollOpenDie(sides)
        else:
            return result

    def rollObDie(self, sides):
        """
        An unlimited die roll. If the roll is the maximum value, replace it with two new dice.
        """
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
        self.list = []

    def getResultString(self):
        return unicode("Resultatet av tärningsslaget " + str(self.dieroll) + " blev: " + str(self.result), 'utf-8')
        #return "You rolled " + str(self.dieroll) + " and got: " + str(self.result)
        
class Dicey(object):
    """Dicey can replace die roll text in strings with results of the rolls."""
    die_list = None
    roll_string = "%(dieroll)s (%(result)s %(list)s)"

    def makeDieRoll(self, m):
        die = Die(int(m.group('die')), m.group('rolls'), m.group('op'), m.group('val'), 
                   m.group('rolltype'), m.group('seltype'), m.group('nrofresults'), die_list=self.die_list)
        die.roll()
        return die

    def replaceDieRollAsHtml(self, m):
        """Replaces die rolls with html and the result of the roll."""
        die = self.makeDieRoll(m)
        html = "<div class='dieroll'>"
        html += die.dieroll
        html += "<img src='http://www.rollspel.nu/forum/images/graemlins/wrnu/t" + str(die.die) + ".gif' alt='" + str(die.dieroll) + "' title='" + str(die.dieroll) + "' />"
        html += "<br />" + die.getResultString()
        html += "<br />: All die rolls: " + str(die.list)
        html += "</div>"
        if die.list:
            return html
        else:
            return die.dieroll

    def replaceDieRoll(self, m):
        """Replaces die rolls with the result of the roll."""
        die = self.makeDieRoll(m)
        if die.list:
            return self.roll_string % {
                'die': die.die,
                'dieroll': die.dieroll,
                'result': die.result,
                'list': die.list,
                'op': die.op,
                'val': die.val,
                'seltype': die.seltype,
                'rolls': die.rolls,
                'rolltype': die.rolltype,
                'nrofresults': die.nrofresults,
                'resultstring': die.getResultString(),
            }
        else:
            return die.dieroll

    def replaceDieStrings(self, diestring, roll_call=None, max_responses=0, die_list=None, roll_string=None):
        """Finds all die roll texts in string and replaces them with result information."""
        if not roll_call:
            roll_call = self.replaceDieRoll
        if die_list is not None:
            self.die_list = die_list
        if roll_string is not None:
            self.roll_string = roll_string
        newstring = re.sub(Die.dice_pattern, roll_call, diestring, max_responses)
        return newstring

if __name__ == '__main__':
    string = "asdf 4d6h3 qwer d20+100 asdfasf d12-100 asdf OpenD20 D8 d3 Ob3T6 d4 t10 d100 d12 d55 t78"
    #string = "asdf 4d6h3 qwer d20+100 asdfasf d12-100 asdf OpenD20 D8 d3 Ob3T6 d4 t10 d100 d12"
    print "Original string: " + string
    d = Dicey()
    #newstring = d.replaceDieStrings(string, die_list=())
    newstring = d.replaceDieStrings(string)
    print "Result string: " + newstring

