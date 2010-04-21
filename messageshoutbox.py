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

class MessageShoutbox(Shoutbox):
    latest_shout = 0
    first_shout = 0
    base_url = ""

    def __init__(self, config):
        self.parser = ElementParser()
        self.cfg = config
        self.base_url = config.base_url

    def __del__(self):
        pass

    def readShouts(self, start=-1):
        """
        Read shoutbox messages, all or newer than "start".
        """
        if start < 0:
            start = self.latest_shout
        print "Loading shouts, with start:", start
        shoutdata = self.loadShouts(start)
        shouts = self.parseShouts(shoutdata)
        return shouts

    def loadShouts(self, start):
        params = urlencode({
            "ubb": "listshouts",
            "shout": start,
        })
        shoutxml = loadUrl(self.base_url, params)
        return shoutxml

    def parseShout(self, s):
        return Shout(s['id'], s['from_id'], s['from'], self._getElStr(s.body), s['time'])

    def sendShout(self, user, message):
        params = urlencode({
            "ubb": "listshouts",
            "action": "send",
            "secret": self.cfg.secret,
            "user_id": user.id,
            "user_name": user.name,
            "message": message.encode('latin-1', 'xmlcharrefreplace'),
        })
        result = loadUrl(self.base_url, params)
        if result == "OK":
            return True
        return False

    def _getElStr(self, el):
        return unicode(unescape(el.__str__().strip()))

    def parseShouts(self, shoutxml):
        dom = self.parser(shoutxml)
        shouts = []
        oldershouts = self.latest_shout
        for e in dom.elements():
            if e.name == "message":
                shout = self.parseShout(e)
                if shout.id > oldershouts:
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

