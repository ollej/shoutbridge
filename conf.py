# -*- coding: utf-8 -*-

import sys
import ConfigParser

class ConfSectionNotFound(Exception):
    "Couldn't find configuration section."

class Conf(object):
    _RAW = 1
    _SAFE = 2
    _DEFAULT = 3
    _cfg = None
    _items = None

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
        self._items = self._cfg.items(section)
        for k, v in self._items:
            setattr(self, k, v)

    def get(self, name):
        #return self._items[name]
        return self._cfg.get(self._section, name)

    def get_items(self):
        return self._items

# Call the main function.
if __name__ == '__main__':
    C = Conf('config.ini', 'LOCAL') 
    print C.get_items()
