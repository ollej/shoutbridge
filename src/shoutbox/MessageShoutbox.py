# -*- coding: utf-8 -*-

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
            "start": str(start),
        })
        shoutxml = loadUrl(self.cfg.base_url, params)
        #self.logprint(shoutxml)
        return shoutxml

    def parseShout(self, s):
        return Shout(s['id'], s['from_id'], s['from'], getElStr(s.body), s['time'])

    def sendShout(self, user, message):
        params = dict({
            "ubb": "listshouts",
            "action": "send",
            "secret": self.cfg.secret,
            "user_id": str(user.id),
            "user_name": user.name,
            "message": message #.encode('utf-8', 'xmlcharrefreplace'),
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
        oldershouts = self.latest_shout
        for e in dom.elements():
            if e.name == "message":
                shout = self.parseShout(e)
                #self.logprint("Parsed shout", shout.id, shout.userid, shout.name, shout.time, shout.text)
                #self.logprint("oldershouts", oldershouts, "latest_shout", self.latest_shout)
                if shout.id > oldershouts and shout.userid is not 1:
                    #self.logprint("Adding shout", shout.__str__())
                    shouts.append(shout)
                    if shout.id > self.latest_shout:
                        #self.logprint("Updating latest latest_shout to:", shout.id)
                        self.latest_shout = int(shout.id)
        return shouts


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

