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

import re

from plugins.Plugin import *
from utils.utilities import *

class ScraperPlugin(Plugin):
    name = "ScraperPlugin"
    author = "Olle Johansson"
    description = "A simple scraper plugin."
    commands = [
        dict(
            command = ['!scrape'],
            handler = 'scrape',
            onevents = ['Message'],
            url = 'http://example.com/index.html',
            search = [
                '<font color="red"><b><tt>ERROR',
                '<font color="red"><b><tt>FAILURE',
            ]
        )
    ]

    def scrape(self, shout, command, comobj):
        if comobj['url']:
            lines = read_file(comobj['url'])
        matches = []
        if lines:
            for s in comobj['search']:
                matches.extend(grep(s, lines))
        if matches:
            for m in matches:
                # TODO: This is a quite specific use case.
                m = strip_tags(m)
                m = re.sub("(&nbsp;)+", " ", m)
                m = re.sub("^(ERROR|FAILURE)", "\\1:", m)
                if m.startswith('ERROR') or m.startswith('FAILURE'):
                    self.send_message(m)

