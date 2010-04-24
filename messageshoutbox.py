# -*- coding: utf-8 -*-

import re
from urllib import urlencode
import urllib2
from datetime import date
from datetime import datetime
from twisted.words.xish import domish
import htmlentitydefs
from shoutbox import *
from utilities import *
import xml.parsers.expat
import time
from datetime import datetime, date

class MessageShoutbox(Shoutbox):
    latest_shout = 0
    first_shout = 0
    base_url = ""

    def __init__(self, config):
        self.parser = ElementParser()
        self.cfg = config
        self.base_url = config.base_url
        self.latest_shout = self.cfg.latest_shout

    def __del__(self):
        pass

    def logprint(self, *message):
        print "--------------------------------------------------------------"
        print datetime.now().strftime(self.cfg.log_date_format), '-',
        for m in message:
            print m,
        print "\n--------------------------------------------------------------"

    def readShouts(self, start=None):
        """
        Read shoutbox messages, all or newer than "start".
        """
        if start is None:
            start = self.latest_shout
        shoutdata = self.loadShouts(start)
        shouts = self.parseShouts(shoutdata)
        return shouts

    def loadShouts(self, start):
        params = urlencode({
            "ubb": "listshouts",
            "start": start,
        })
        self.logprint("Loading shouts:\n", self.base_url, params)
        shoutxml = loadUrl(self.base_url, params)
        return shoutxml

    def parseShout(self, s):
        return Shout(s['id'], s['from_id'], s['from'], getElStr(s.body), s['time'])

    def sendShout(self, user, message):
        params = urlencode({
            "ubb": "listshouts",
            "action": "send",
            "secret": self.cfg.secret,
            "user_id": user.id,
            "user_name": user.name,
            "message": message.encode('utf-8', 'xmlcharrefreplace'),
        })
        self.logprint("Sending shout:\n", self.base_url, params)
        result = loadUrl(self.base_url, params)
        if result == "OK":
            return True
        return False

    def parseShouts(self, shoutxml):
        dom = self.parser(shoutxml)
        shouts = []
        oldershouts = self.latest_shout
        for e in dom.elements():
            if e.name == "message":
                shout = self.parseShout(e)
                if shout.id > oldershouts and shout.userid is not 1:
                    shouts.append(shout)
                    if shout.id > self.latest_shout:
                        self.latest_shout = shout.id
        return shouts


def main():
    import sys
    import string
    from conf import Conf
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

