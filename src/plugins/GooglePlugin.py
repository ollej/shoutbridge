#!/usr/bin/python
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

import urllib
import simplejson

class GooglePlugin(Plugin):
    name = "GooglePlugin"
    author = "Olle Johansson"
    description = "Makes a google search for the given terms and returns the first hit."
    commands = [
        dict(
            command = ['!google', '!lmgtfy'],
            handler = 'google',
            onevents = ['Message'],
        )
    ]

    def google(self, shout, command, comobj):
        terms = self.strip_command(shout.text, command)
        query = urllib.urlencode({'q' : terms})
        url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % (query)
        search_results = urllib.urlopen(url)
        json = simplejson.loads(search_results.read())
        results = json['responseData']['results']
        if results:
            url = results[0]['url']
            title = results[0]['title']
            msg = 'Google says: <a href="%s" target="_blank">%s</a>' % (url, title)
            self.send_message(msg)

