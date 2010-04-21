# -*- coding: utf-8 -*-

import urllib2
import re
import htmlentitydefs
from twisted.words.xish import domish

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

        xmldef = '<?xml version="1.0" encoding="utf-8"?>\n'
        if s.startswith(xmldef):
            s = s.replace(xmldef, '', 1)
        s = s.encode('ascii', 'xmlcharrefreplace')
        parser = domish.elementStream()
        parser.DocumentStartEvent = onStart
        parser.ElementEvent = onElement
        parser.DocumentEndEvent = onEnd
        tmp = domish.Element(("", "s"))
        tmp.addRawXml(s)
        parser.parse(tmp.toXml())
        return self.result.firstChildElement()

def loadUrl(url, params=None, method="GET"):
    if params and method == "GET":
        url = url + "?%s" % params
        params = None
    print "Loading URL:", url
    f = urllib2.urlopen(url, params)
    s = f.read()
    f.close()
    s = unicode(s, 'utf-8')
    return s

##
# Removes HTML or XML character references and entities from a text string.
#
# @author Fredrik Lundh
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.
def unescape(text):
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

if __name__ == '__main__':
    xml = loadUrl('http://www.rollspel.nu/forum/ubbthreads.php?ubb=listshouts')
    parser = ElementParser()
    dom = parser(xml)

