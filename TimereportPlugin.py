# -*- coding: utf-8 -*-

import os
import glob
import linecache

from Plugin import *
from utilities import *

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

def main():
    import sys
    import string
    from time import time
    from Conf import Conf
    import Shoutbox
    cfg = Conf('config.ini', 'LOCAL')
    args = sys.argv
    msg = unicode(' '.join(args[1:]), 'utf-8')
    shout = Shoutbox.Shout(1, 4711, 'Test', msg, time())
    bridge = FakeBridge()
    plug = TimereportPlugin([bridge])
    plug.setup()
    print "Returned:", plug.handleShoutMessage(shout)

# Call the main function.
if __name__ == '__main__':
    main()
