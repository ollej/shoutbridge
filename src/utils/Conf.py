# -*- coding: utf-8 -*-

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
