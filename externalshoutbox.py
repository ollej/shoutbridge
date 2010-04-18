# -*- coding: utf-8 -*-

import re
import urllib2
from datetime import date
from datetime import datetime
from twisted.words.xish import domish
import htmlentitydefs

class ShoutboxError(Exception):
    "Unknown Shoutbox error"

class ShoutboxUserNotFoundError(ShoutboxError):
    "Found no such user."

class User:
    id = ""
    name = ""
    jid = ""

    def __init__(self, id, name, jid):
        self.id = id
        self.name = name
        self.jid = jid

class Shout:
    """
    SHOUT_ID, USER_ID, SHOUT_DISPLAY_NAME, SHOUT_TEXT, SHOUT_TIME
    """
    def __init__(self, id, userid, name, text, time):
        self.id = id
        self.userid = userid
        self.name = name
        self.text = text
        self.time = time
        
class Graemlin:
    """
    GRAEMLIN_MARKUP_CODE, GRAEMLIN_SMILEY_CODE, GRAEMLIN_IMAGE, GRAEMLIN_WIDTH, GRAEMLIN_HEIGHT
    """
    def __init__(self, code, smiley, image, width, height):
        self.code = code
        self.smiley = smiley
        self.image = image
        self.width = width
        self.height = height

    def get_html(self):
        vals = (self.image, self.code, self.code, self.width, self.height)
        return '<img src="<<GRAEMLIN_URL>>/%s" alt="%s" title="%s" height="%s" width="%s" />' % vals

    def get_code(self):
        return self.smiley or ':' + self.code + ':'

class ElementParser(object):
    "callable class to parse XML string into Element"

    def __call__(self, s):
        self.result = None
        def onStart(el):
            self.result = el
        def onEnd():
            pass
        def onElement(el):
            self.result.addChild(el)

        parser = domish.elementStream()
        parser.DocumentStartEvent = onStart
        parser.ElementEvent = onElement
        parser.DocumentEndEvent = onEnd
        tmp = domish.Element(("", "s"))
        tmp.addRawXml(s)
        parser.parse(tmp.toXml())
        return self.result.firstChildElement()

class ExternalShoutbox:
    latest_shout = 0
    first_shout = 0
    base_url = ""

    def __init__(self, config):
        self.parser = ElementParser()
        self.base_url = config.base_url
        self.shoutre = re.compile(
            r"""
            title="Skriven:\ (?P<time>[^"]*)" .*
            id="shout(?P<id>\d+)">\s
            <a\ href="/forum/ubbthreads.php/users/(?P<userid>\d*)/(?:.*).html">
            <span(?:[^>]*?)>(?P<username>[^<]+)</span></a>:&nbsp;
            (?P<content>.*)
            \s<\/div>
            """,
            re.X | re.M | re.S )

    def __del__(self):
        pass

    ##
    # Removes HTML or XML character references and entities from a text string.
    #
    # @author Fredrik Lundh
    # @param text The HTML (or XML) source text.
    # @return The plain text, as a Unicode string, if necessary.
    def unescape(self, text):
        def fixup(m):
            text = m.group(0)
            if text[:2] == "&#":
                # character reference
                try:
                    if text[:3] == "&#x":
                        return unichr(int(text[3:-1], 16))
                    else:
                        return unichr(int(text[2:-1]))
                except ValueError:
                    pass
            else:
                # named entity
                try:
                    text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
                except KeyError:
                    pass
            return text # leave as is
        return re.sub("&#?\w+;", fixup, text)

    def _getUserByField(self, field, id):
        """
        Retrieves User information based on a db field and value.
        """
        if not id:
            return User(1, 'Anonymous', '')
        usr = User(1, 'Anonymous', '')
        return usr

    def getUserByUsername(self, username):
        """
        Retrieves User information based on a username
        """
        return self._getUserByField("u.USER_DISPLAY_NAME", username)

    def getUserById(self, id):
        """
        Retrieves User information based on an id.
        """
        return self._getUserByField("u.USER_ID", id)

    def getUserByJid(self, jid):
        """
        Retrieves User information based on an XMPP login.
        """
        return self._getUserByField(self.db_fld_profile, jid)

    def sendShout(self, user, message):
        """
        Send a shoutbox message from a user.
        """
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

    def loadUrl(self, url, params=None, method="GET"):
        if params and method == "GET":
            url = url + "?%s" % params
            params = None
        print "Loading URL:", url
        f = urllib2.urlopen(url, params)
        s = f.read()
        f.close()
        return s

    def loadShouts(self, start):
        url = self.base_url + "?ubb=getshouts&shout=" + str(start)
        shoutxml = self.loadUrl(url)
        shoutxml = unicode(shoutxml, 'utf-8').encode('ascii', 'xmlcharrefreplace')
        shoutxml = shoutxml.replace('<?xml version="1.0" encoding="UTF-8" ?>\n', '')
        return self.parseShouts(shoutxml)

    def parseShout(self, shout):
        matches = re.search(self.shoutre, shout)
        if matches:
            s = matches.groupdict()
            for k, v in s.items():
                s[k] = self.unescape(s[k])
            return s

    def getElStr(self, el):
        return unicode(el.__str__().strip())

    def parseShouts(self, shoutxml):
        dom = self.parser(shoutxml)
        shouts = []
        oldershouts = self.latest_shout
        for e in dom.elements():
            if e.name == 'firstshout':
                self.first_shout = self.getElStr(e)
            elif e.name == "lastshout":
                self.latest_shout = self.getElStr(e)
            elif e.name == "shouts":
                for f in e.elements('', 'shoutdata'):
                    shout = self.parseShout(self.getElStr(f))
                    if shout and shout['id'] > oldershouts:
                        shouts.append(shout)
        return shouts

    def replace_graemlins(self, text):
        if text.find('<<GRAEMLIN_URL>>') < 0:
            return text
        for s in self.graemlins:
            text = text.replace(s.get_html(), s.get_code())
        return text


def main():
    import sys
    import string
    from conf import Conf
    cfg = Conf('config.ini', 'LOCAL')
    sbox = Shoutbox(cfg)
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

