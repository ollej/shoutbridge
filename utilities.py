# -*- coding: utf-8 -*-

import urllib2
import re
import htmlentitydefs
from twisted.words.xish import domish
import codecs

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
    try:
        f = urllib2.urlopen(url, params)
        s = f.read()
        f.close()
        s = unicode(s, 'utf-8')
    except urllib2.URLError:
        # For now, just ignore URL errors and return empty string.
        return ""
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

def getElStr(el):
    return unicode(unescape(el.__str__().strip()))

def read_file(filename, separator=None):
    """
    Loads the lines in the file into an array.
    If separator is given, those characters by themselves on a line will separate
    each element in the array, otherwise each line will be an element.
    """
    lines = []
    text = ""
    #f = open (filename, "r", "utf-8")
    f = codecs.open(filename, "r", "utf-8")
    for line in f.readlines():
        if separator and line.strip() == separator:
            lines.append(text)
            text = ""
            continue
        if separator:
            text += line
        else:
            lines.append(line)
    if text:
        lines.append(text)
    return lines

def file_len(filename):
    """
    Returns the number of lines in the given file.
    """
    with open(filename) as f:
        for i, l in enumerate(f):
            pass
    return i

def add_line_to_file(filename, text, separator=None, newline="\n"):
    """
    Writes text to filename.
    Prepends a line with separator if given.
    """
    f = codecs.open(filename, "a+", "utf-8")
    f.seek(0, 2)
    if separator and f.tell() > 0:
        f.write(separator + newline)
    f.write(text + newline)

if __name__ == '__main__':
    xml = loadUrl('http://www.rollspel.nu/forum/ubbthreads.php?ubb=listshouts')
    parser = ElementParser()
    dom = parser(xml)

