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

import sys
import ConfigParser
from BridgeClass import BridgeClass

class ConfSectionNotFound(Exception):
    "Couldn't find configuration section."

class Conf(BridgeClass):
    _RAW = 1
    _SAFE = 2
    _DEFAULT = 3
    _cfg = None
    _items = dict()

    def __init__(self, file, section, type=1):
        self._file = file
        self._section = section
        self._type = type
        if type == self._RAW:
            self._cfg = ConfigParser.RawConfigParser()
        elif type == self._SAFE:
            self._cfg = ConfigParser.SafeConfigParser()
        else:
            self._cfg = ConfigParser.ConfigParser()
        try:
            self._cfg.read(file)
        except:
            print "Unexpected error:"
            print "Couldn't read configuration", sys.exc_info()[0]
            sys.exit()
        if not self._cfg.has_section(section):
            raise ConfSectionNotFound
        self.read_all(section)

    def read_all(self, section):
        if not self._cfg.has_section(section):
            raise ConfSectionNotFound
        self.set_items(dict(self._cfg.items(section)))

    def get(self, name):
        return self._items[name]

    def set(self, name, value):
        self._items[name] = value

    def get_bool(self, name):
        try:
            val = self._items[name]
        except KeyError:
            return None
        if val == True or val.lower() in ["true", "1", "on", "yes"]:
            return True
        return False

    def get_items(self):
        return self._items

    def set_items(self, items):
        for k, v in items.items():
            if v:
                self._items[k] = v
                setattr(self, k, v)

# Call the main function.
if __name__ == '__main__':
    C = Conf('config.ini', 'LOCAL') 
    print C.get_items()
