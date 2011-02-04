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

from plugins.Plugin import *

class CryptoPlugin(Plugin):
    name = "CryptoPlugin"
    author = "Olle Johansson"
    description = "Adds some simple crypto commands."
    commands = [
        dict(
            command = ['!reverse'],
            handler = 'cmd_reverse',
            onevents = ['Message'],
        ),
        dict(
            command = ['!rot13'],
            handler = 'cmd_rot13',
            onevents = ['Message'],
        ),
    ]

    def cmd_reverse(self, shout, command, comobj):
        msg = self.strip_command(shout.text, command)
        msg = msg[::-1]
        self.send_message(msg)

    def cmd_rot13(self, shout, command, comobj):
        msg = self.strip_command(shout.text, command)
        msg = self.rot13(msg)
        self.send_message(msg)

    def rot13(self, s):
        return ''.join( self.rot13_char(ch) for ch in s )

    def rot13_char(self, ch):
        if ch.lower() <= 'm':
            dist = 13
        else:
            dist = -13
        return chr(ord(ch) + dist)

