# -*- coding: utf-8 -*-

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

