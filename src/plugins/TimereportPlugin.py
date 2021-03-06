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

import os
import glob
import linecache

from plugins.Plugin import *
from utils.utilities import *

class TimereportPlugin(Plugin):
    """
    Timereport bot allows you to report time on projects.
    """
    priority = 0
    name = "TimereportPlugin"
    author = "Olle Johansson <Olle@Johansson.com>"
    description = "Timereport bot allows you to report time on projects."
    filename = "extras/timereports.dat"
    separator = '%'
    commands = [
        dict(
            command=['!timereport'],
            handler='timereport',
        ),
        dict(
            command=['!printreport'],
            handler='printreport',
        ),
    ]
    reports = dict()

    def setup(self):
        """
        Setup method which is called once before any triggers methods are called.
        """
        self.reports = self.read_reports(self.filename)

    def read_reports(self, file):
        """
        Read reported times.
        """
        reports = dict()
        lines = read_file(file)
        for line in lines:
            # TODO: Maybe send a function ref to read_file for handling each line.
            try:
                (term, definition) = line.split("=", 1)
            except ValueError:
                self.logprint("Couldn't load report line:", line)
                continue
            for t in term.split(','):
                reports[t.lower()] = definition.strip()
        return reports

    def timereport(self, text, nick, command, cmd):
        """
        Add new timereport.
        """
        newterm = text.replace(command, '', 1).strip()
        if newterm:
            try:
                (term, definition) = newterm.split('=', 1)
            except ValueError:
                self.bridge.send_and_shout("Couldn't add timereport.", self.nick)
                return
            newdefinition = term.strip() + '=' + definition.strip()
            add_line_to_file(self.filename, newdefinition, separator=self.separator)
            self.bridge.send_and_shout("Time reported", self.nick)

    def printreport(self, text, nick, command, cmd):
        """
        Print reported time.
        """
        if not text:
            return
        #words = text.split()[1:]
        word = text.replace(command, '', 1).strip()
        if not word:
            word = random.choice(self.reports.keys())
        answer = ""
        self.logprint('Handling term:', word)
        try:
            answer += u"Time report '%s': %s" % (word, self.reports[word.lower()])
        except KeyError:
            pass
        if not answer.strip():
            answer = "Found no timereport."
        self.bridge.send_and_shout(answer.strip(), self.nick)

