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
from datetime import date
from datetime import datetime
from twisted.words.xish import domish
import htmlentitydefs
import xml.parsers.expat
import time
from datetime import datetime, date

from shoutbox.Shoutbox import *
from utils.utilities import *

class MessageShoutbox(Shoutbox):
    latest_shout = 0

    def __init__(self, config=None):
        self.parser = ElementParser()
        if config:
            self.setConfig(config)

    def __del__(self):
        pass

    def readShouts(self, start=None):
        """
        Read shoutbox messages, all or newer than "start".
        """
        if start is None:
            start = self.latest_shout
        shoutdata = self.loadShouts(start)
        if shoutdata:
            shouts = self.parseShouts(shoutdata)
            return shouts
        return []

    def loadShouts(self, start):
        params = dict({
            "ubb": "listshouts",
            "longpoll": "1",
            "start": str(start),
        })
        shoutxml = loadUrl(self.cfg.base_url, params)
        #self.logprint(shoutxml)
        return shoutxml

    def skipShouts(self):
        """
        Reads all shouts and ignores them.
        """
        xml = self.loadShouts(self.latest_shout)
        self.parseShouts(xml)

    def parseShout(self, s):
        return Shout(s['id'], s['from_id'], s['from'], getElStr(s.body), s['time'])

    def sendShout(self, user, message):
        params = dict({
            "ubb": "listshouts",
            "action": "send",
            "secret": self.cfg.secret,
            "user_id": str(user.id),
            "user_name": user.name,
            "message": message,
        })
        self.logprint("Sending shout:\n", self.cfg.base_url, params)
        result = loadUrl(self.cfg.base_url, params)
        if result == "OK":
            return True
        return False

    def parseShouts(self, shoutxml):
        if not shoutxml:
            return []
        dom = self.parser(shoutxml)
        if not dom:
            self.logprint("Empty dom object returned from parser for xml:\n", shoutxml)
            return [] 
        shouts = []
        for e in dom.elements():
            if e.name == "message":
                shout = self.handleShoutMessage(e)
                if shout:
                    shouts.append(shout)
        return shouts

    def handleShoutMessage(self, e):
        oldershouts = self.latest_shout
        shout = self.parseShout(e)
        if shout.id > oldershouts and shout.userid is not 1:
            if shout.id > self.latest_shout:
                self.latest_shout = int(shout.id)
                if self.db:
                    self.db.set_value('latest_shout_id', self.latest_shout)
            return shout

def main():
    import sys
    import string
    from Conf import Conf
    cfg = Conf('config.ini', 'LOCAL')
    sbox = MessageShoutbox(cfg)
    print sbox.readShouts()
    if len(sys.argv) > 1:
        args = sys.argv
        id = args[1]
        msg = ' '.join(args[2:])
        print "id = " + id + " msg: " + msg
        if id.isdigit():
            usr = sbox.getUserById(id)
        elif string.find(id, '@') >= 0:
            usr = sbox.getUserByJid(id)
        else:
            usr = sbox.getUserByUsername(id)
        sbox.sendShout(usr, msg)

# Call the main function.
if __name__ == '__main__':
    main()

