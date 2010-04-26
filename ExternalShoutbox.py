# -*- coding: utf-8 -*-

import re
import urllib2
from datetime import date
from datetime import datetime
from twisted.words.xish import domish
import htmlentitydefs

from Shoutbox import *
from utilities import *

class ExternalShoutbox(Shoutbox):
    latest_shout = 0
    first_shout = 0
    base_url = ""
    shoutre = None

    def __init__(self, config):
        self.parser = ElementParser()
        self.cfg = config
        self.base_url = config.base_url
        self.shoutre = re.compile(
            r"""
                title="Skriven:\ (?P<time>[^"]*)" .*
                id="shout(?P<id>\d+)"> .*
                (?:<span class="standouttext">\*)?
                <a\ href="/forum/ubbthreads.php/users/(?P<userid>\d*)/(?:.*).html">
                <span(?:[^>]*?)>(?P<username>[^<]+)</span></a>:?&nbsp;
                (?P<content>.*?)
                \n(?:<\/span>)?<\/div>
            """,
            re.VERBOSE | re.MULTILINE | re.DOTALL )

    def __del__(self):
        pass

    def readShouts(self, start=-1):
        """
        Read shoutbox messages, all or newer than "start".
        """
        if start < 0:
            start = self.latest_shout
        print "Loading shouts, with start:", start
        rows = self.loadShouts(start)
        shouts = []
        for s in rows:
            #text = self.replace_graemlins(s[3])
            if s:
                shouts.append(Shout(s['id'], s['userid'], s['username'], s['content'], s['time']))
        return shouts

    def loadShouts(self, start):
        params = urlencode({
            "ubb": "getshouts",
            "start": start,
        })
        shoutxml = loadUrl(self.base_url, params)
        #shoutxml = unicode(shoutxml, 'utf-8').encode('ascii', 'xmlcharrefreplace')
        #shoutxml = shoutxml.replace('<?xml version="1.0" encoding="UTF-8" ?>\n', '')
        return self.parseShouts(shoutxml)

    def parseShout(self, shout):
        matches = re.search(self.shoutre, shout)
        if matches:
            s = matches.groupdict()
            for k, v in s.items():
                s[k] = unescape(s[k])
            return s

    def parseShouts(self, shoutxml):
        dom = self.parser(shoutxml)
        shouts = []
        oldershouts = self.latest_shout
        for e in dom.elements():
            if e.name == 'firstshout':
                self.first_shout = getElStr(e)
            elif e.name == "lastshout":
                self.latest_shout = getElStr(e)
            elif e.name == "shouts":
                for f in e.elements('', 'shoutdata'):
                    shout = self.parseShout(getElStr(f))
                    if shout and shout['id'] > oldershouts:
                        shouts.append(shout)
        return shouts


def main():
    import sys
    import string
    from Conf import Conf
    cfg = Conf('config.ini', 'LOCAL')
    sbox = ExternalShoutbox(cfg)
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

