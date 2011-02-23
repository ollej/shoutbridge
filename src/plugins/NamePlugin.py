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

class NamePlugin(Plugin):
    """
    Returns the names of today in the Swedish calendar.
    """
    priority = 0
    name = "NamePlugin"
    author = "Olle Johansson <Olle@Johansson.com>"
    description = "Plugin that prints names from the Swedish calendar."
    commands = [
        dict(
            command=['!dagensnamn'],
            handler='send_names',
            onevents=['Message'],
        ),
    ]
    names = []

    def setup(self):
        """
        Setup method which is called once before any triggers methods are called.
        """
        self.names = read_file("extras/names.dat")

    def send_names(self, shout, command, comobj):
        """
        Parse message body and send message with dice roll.
        """
        d = date.today()
        day = int(d.strftime("%j")) - 1
        names = self.names[day]
        self.send_message(names)

