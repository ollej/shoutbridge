# -*- coding: utf-8 -*-
#! /usr/bin/python

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

import re
import random

class Die(object):
    """
    Defines the information for a die roll.
    TODO: 4d6h3 for rolling 4 d6 dice and choosing the three highest.
    """
    #: List of allowed dice by default
    die_list = (2, 4, 6, 8, 10, 12, 20, 100)
    #: Maximum number of rolls allowed.
    max_rolls = 1000
    die = 0
    rolls = 0
    op = ''
    val = 0
    rolltype = ''
    success = ''
    threshold = None
    seltype = None
    nrofresults = None
    result = 0
    list = []
    successes = 0
    failures = 0
    sorf = 0

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
        (
            (?P<success>[<>])           # > counts successes, < failures
            (?P<threshold>\d+)          # Threshold for success/failure
        )?
        (                               # Start of operation
            (?P<op>\+|\-)               # Add or subtract?
            (?P<val>\d+)                # Value to add/subtract 
        )?                              # Operation not necessary
        )
        """, re.VERBOSE | re.IGNORECASE)

    def __init__(self, die, rolls=1, op='', val=0, rolltype='', 
                 seltype=None, nrofresults=None, die_list=None, max_rolls=None,
                 success='', threshold=0):
        """
        Initialize the Die to roll.
        param string die String containing the die roll to make, either just the number of sides to roll, or more complex: 3D6h2+4
        param integer rolls (Optional) Number of rolls to make, unless overridden by die
        param string op (Optional) Add or subtract val, unless overridden by die
        param integer val (Optional) Value to add or subtract to the roll, unless overridden by die
        param string rolltype (Optional) "Ob" to make an unlimited die roll, "Open" to make an open-ended die roll. Can be overridden by die.
        param string seltype (Optional) "h" to select highest results, "l" to select lowest results. Can be overridden by die.
        param integer nrofresults (Optional) If selecting highest or lowest results, select this many results. Can be overridden by die.
        param list die_list (Optional) List of integers. Only allow dice with as many sides as the numbers listed in this list. Empty list to allow all. None to use default: (2, 4, 6, 8, 10, 12, 20, 100)
        param integer max_rolls (Optional) If rolls is higher than this number, only one roll will be made. Defaults to 1000.
        param string success (Optional) '>' to count successs (rolls above threshold), '<' for failures.
        param integer threshold (Optional) Threshold for success or failure count.
        """
        # If die is a string, parse it to get all values.
        if type(die).__name__ == 'str':
            (die, rolls, op, val, rolltype, seltype, nrofresults, success, threshold) = self.parseDice(die)
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
        self.val = int(val) if val else None
        self.rolltype = rolltype if rolltype and rolltype in ('Ob', 'Open') else ''
        self.success = success if success in ('<', '>') else ''
        if self.success:
            self.threshold = int(threshold)

        # Build up self.dieroll based on parsed values
        if self.rolls > 1:
            self.dieroll = self.rolltype + str(self.rolls) + 'd' + str(self.die)
        else:
            self.dieroll = self.rolltype + 'd' + str(self.die)
        if seltype and nrofresults > 0:
            self.dieroll += seltype + str(nrofresults)
        if self.success:
            self.dieroll += self.success + str(self.threshold)
        if op and val > 0:
            self.dieroll += self.op + str(self.val)

        # Reset roll values
        self.result = 0
        self.list = []

    def parseDice(self, die):
        """
        Parses the string die for die rolls and returns a regexp match object if found, otherwise it returns die converted to an integer.
        param String die String containing die roll to make, or a number defining the number of sides of the die to roll.
        returns list|integer If a die roll was found in the string, a list of parsed values is returned, in the following order: die, rolls, op, val, rolltype, seltype, nrofresults
        """
        m = re.search(self.dice_pattern, die)
        if m:
            return (m.group('die'), m.group('rolls'), m.group('op'), m.group('val'), m.group('rolltype'), m.group('seltype'), m.group('nrofresults'), m.group('success'), m.group('threshold'))
        else:
            return int(die)

    def roll(self, reset=None):
        """
        Rolls the die according to the set values, sets self.roll and returns it.
        param boolean reset If set, the previous values rolled will be reset before the new roll is made.
        """
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

        # Count successes or failures
        if self.success == '>':
            self.successes = self.countSuccesses(self.list, self.threshold)
        elif self.success == '<':
            self.failures = self.countFailures(self.list, self.threshold)
        self.sorf = self.successes + self.failures

        return self.result

    def countSuccesses(self, list, threshold):
        count = 0
        for i in list:
            if i >= threshold:
                count = count + 1
        return count

    def countFailures(self, list, threshold):
        count = 0
        for i in list:
            if i <= threshold:
                count = count + 1
        return count

    def randomize(self):
        """
        Makes a die roll based on the values set in the object.
        Calls self.rollObDie, self.rollOpenDie or self.rollDie depending on configured self.rolltype
        """
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
        """
        Based on seltype, selects a number of highest or lowest results from the rolled dice.
        param string seltype 'h' to select the highest values, 'l' to select the lowest values.
        param integer nrofresults Number of die rolls to select from the list if seltype is set.
        """
        nrofresults = int(nrofresults)
        if seltype == 'h':
            results = self.getHighest(self.list, nrofresults)
        elif seltype == 'l':
            results = self.getLowest(self.list, nrofresults)
        return results

    def getHighest(self, lst, count):
        """
        Return the count highest items from lst.
        param list lst List of rolled dice results.
        param integer count The number of highest values to return from lst
        """
        lst.sort()
        highest = lst[-count:]
        highest.reverse()
        return highest

    def getLowest(self, lst, count):
        """
        Return the count lowest items from lst.
        param list lst List of rolled dice results.
        param integer count The number of lowest values to return from lst
        """
        lst.sort()
        lst.reverse()
        lowest = lst[-count:]
        lowest.reverse()
        return lowest

    def rollOpenDie(self, sides):
        """
        Roll an open die. If the roll is the highest value, roll again and add the result.
        param integer sides Number of sides on the die to roll.
        """
        result = self.rollDie(sides)
        if result == sides:
            return result + self.rollOpenDie(sides)
        else:
            return result

    def rollObDie(self, sides):
        """
        An unlimited die roll. If the roll is the maximum value, replace it with two new dice.
        param integer sides Number of sides on the die to roll.
        """
        result = self.rollDie(sides)
        if result == sides:
            self.list.pop()
            return self.rollObDie(sides) + self.rollObDie(sides)
        else:
            return result

    def rollDie(self, sides):
        """
        Make a die roll. Result is appended to self.list and returned.
        param integer sides Number of sides on die to roll.
        returns integer The number rolled
        """
        result = random.randint(1, sides) 
        self.list.append(result)
        return result

    def resetResult(self):
        """
        Resets the list of rolled dice and the total result.
        """
        self.result = 0
        self.list = []

    def getResultString(self):
        """
        Returns a formatted string with the result.
        """
        return unicode("Resultatet av tärningsslaget " + str(self.dieroll) + " blev: " + str(self.result), 'utf-8')
        #return "You rolled " + str(self.dieroll) + " and got: " + str(self.result)

class Dicey(object):
    """
    Dicey can replace die roll text in strings with results of the rolls.

    roll_string is a formatting string used as template when returning the die rolls as a string.
    It is used with the standard python interpolation, and the following mapping keys are available:
     * die - Number of sides of the rolled die
     * dieroll - The string used for the die roll, e.g. 3D6h2
     * result - The result of the roll
     * list - The list of all rolled dice
     * op - Operator parsed from the dieroll, e.g. + or -
     * val - Value for operator parsed from the dieroll, e.g. 3
     * rolls - Number of dice to roll
     * rolltype - Type of dieroll, Ob for unlimited and Open for open-ended roll. Empty for normal roll.
     * seltype - Roll selector, h for selecting highest result, l for selecting lowest result
     * nrofresults - Number of results to select (used for highest or lowest)
     * success - Count successes ('>') or failures ('<')
     * threshold - Threshold value for successes or failures.
     * resultstring - The result of the roll as a pre-formatted string from Die.getResultString()
    """
    die_list = None
    roll_string = "%(dieroll)s (%(result)s %(list)s)"

    def __init__(self, die_list=None, roll_string=None):
        """
        Initialize Dicey with default attributes.
        param list die_list Only allow dice with the number of sides in list, empty list to allow all. Defaults to same as in Die(): (2, 4, 6, 8, 10, 12, 20, 100)
        param string roll_string String template to use for replaceDieRoll, default: %(dieroll)s (%(result)s %(list)s)
        """
        if die_list is not None:
            self.die_list = die_list
        if roll_string is not None:
            self.roll_string = roll_string

    def makeDieRoll(self, m):
        """
        Reads group values from the regular expression match object and makes a die roll based on
        the values.
        param m Regexp Match Object with values for a die roll.
        returns Die Die instance already rolled.
        """
        die = Die(die=int(m.group('die')), rolls=m.group('rolls'), op=m.group('op'), val=m.group('val'), 
                  rolltype=m.group('rolltype'), seltype=m.group('seltype'), nrofresults=m.group('nrofresults'),
                  success=m.group('success'), threshold=m.group('threshold'), die_list=self.die_list)
        die.roll()
        return die

    def replaceDieRollAsHtml(self, m):
        """
        Replaces die rolls with html and the result of the roll.
        param m Regexp Match Object with values for a die roll.
        Returns string String with html representing the Die roll in m
        """
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
        """
        Replaces die rolls with the result of the roll.
        param m Regexp Match Object with values for a die roll.
        returns string Text string with information about the die roll based on m, using self.roll_string as a template.
        """
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
                'success': die.success,
                'threshold': die.threshold,
                'successes': die.successes,
                'failures': die.failures,
                'sorf': die.sorf,
                'resultstring': die.getResultString(),
            }
        else:
            return die.dieroll

    def replaceDieStrings(self, diestring, roll_call=None, max_responses=0, die_list=None, roll_string=None):
        """
        Finds all die roll texts in string and replaces them with result information.
        param string diestring String to replace die rolls in.
        param function roll_call (Optional) Function reference to use on replacements in the regexp, defaults to Dicey.replaceDieRoll which returns a string based on Dicey.roll_string. Dicey.replaceDieRollAsHtml can be used here.
        param integer max_repsonses (Optional) Maximum number of die rolls to replace.
        param list die_list (Optional) List of allowed dice (list of integers), use empty string () to allow all or None to allow only the default list: (2, 4, 6, 8, 10, 12, 20, 100)
        param string roll_string (Optional) Set self.roll_string to this string and use it for the string replacemnt in Dice.replaceDieRoll()
        """
        if not roll_call:
            roll_call = self.replaceDieRoll
        if die_list is not None:
            self.die_list = die_list
        if roll_string is not None:
            self.roll_string = roll_string
        newstring = re.sub(Die.dice_pattern, roll_call, diestring, max_responses)
        return newstring

if __name__ == '__main__':
    string = "asdf 4d6h3 qwer d20+100 asdfasf d12-100 asdf OpenD20 D8 d3 Ob3T6 d4 t10 d100 d12 d55 t78 5d6>4 5d10h2>9 3t4<1"
    #string = "asdf 4d6h3 qwer d20+100 asdfasf d12-100 asdf OpenD20 D8 d3 Ob3T6 d4 t10 d100 d12"
    print "Original string: " + string
    d = Dicey(die_list=None, roll_string=None)
    #newstring = d.replaceDieStrings(string, die_list=())
    newstring = d.replaceDieStrings(string, roll_string="%(dieroll)s (%(result)s %(list)s %(sorf)s Successes)")
    print "Result string: " + newstring

