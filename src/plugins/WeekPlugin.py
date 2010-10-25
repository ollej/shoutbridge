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

from datetime import date

from plugins.Plugin import *
from utils.utilities import *

class WeekPlugin(Plugin):
    """
    Returns the ISO week number.
    """
    priority = 0
    name = "WeekPlugin"
    author = "Olle Johansson <Olle@Johansson.com>"
    description = "Simple plugin to display current ISO week number."
    commands = [
        dict(
            command = ['!week', '!vecka'],
            handler = 'send_weeknr',
            onevents = ['Message'],
        ),
    ]

    def send_weeknr(self, shout, command, comobj):
        """
        Return the current ISO week number.
        """
        (isoyear, isoweek, isoweekday) = date.today().isocalendar()
        self.bridge.send_and_shout("Vecka: " + str(isoweek), self.nick)

