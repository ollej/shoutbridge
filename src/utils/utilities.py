# -*- coding: utf-8 -*-

import urllib2
import urllib
import socket
import re
import htmlentitydefs
from twisted.words.xish import domish
import codecs
from optparse import OptionParser

from utils.decorators import *

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

        s = re.sub(r"\<\?xml.*\?\>\n", '', s, 1)
        s = s.encode('ascii', 'xmlcharrefreplace')
        parser = domish.elementStream()
        parser.DocumentStartEvent = onStart
        parser.ElementEvent = onElement
        parser.DocumentEndEvent = onEnd
        tmp = domish.Element(("", "s"))
        try:
            tmp.addRawXml(s)
            parser.parse(tmp.toXml())
        except domish.ParserError:
            return None
        return self.result.firstChildElement()

def loadUrl(url, params=None, method="GET", timeout=10.0, as_object=None):
    """
    Loads url with added params urlencoded.
    If method is empty or "GET", params are added to the url after a '?'.
    If params is set and method isn't GET, the method will be POST.
    An optional timeout on the request can be set.
    """
    if params:
        params = urllib.urlencode(params)
        if method == "GET":
            url = url + "?" + params
            params = None
    try:
        print "Loading URL:", url, params
        print "-----------------------------------------------------------"
        f = urllib2.urlopen(url, params, timeout)
        response_info = f.info()
        if as_object:
            return f
        s = f.read()
        f.close()
        s = unicode(s, 'utf-8')
    except socket.timeout as sock:
        print "Socket timed out.", sock
        print "-----------------------------------------------------------"
        return ""
    except urllib2.HTTPError as he:
        # Request casued a non 200 OK status response.
        print "An error occured when loading URL."
        print "URL:", url
        if params:
            print "Params:", params
        print "HTTP Error:", he
        print "-----------------------------------------------------------"
        return ""
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
    external = False
    if filename.find('://') >= 0:
        f = loadUrl(filename, as_object=True)
        external = True
    else:
        f = codecs.open(filename, "r", "utf-8")
    for line in f.readlines():
        if external:
            line = unicode(line, "utf-8")
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
    #f.write(unicode(text, 'utf-8') + newline)
    f.write(text + newline)

def get_options():
    parser = OptionParser(version="%prog 1.0")
    parser.add_option("-c", "--config", dest="config", default="config.ini",
                      help="Read configuration from FILE", metavar="FILE")
    parser.add_option("-S", "--section", dest="section", default="LOCAL",
                      help="Read configuration from SECTION", metavar="SECTION")
    parser.add_option("-D", "--debug",
                      action="store_true", dest="debug", default=False,
                      help="Print RAW data sent and received on the stream.")
    parser.add_option("-q", "--quiet",
                      action="store_true", dest="quiet", default=False,
                      help="Don't print status messages to stdout")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="make lots of noise [default]")
    parser.add_option("-s", "--start", dest="latest_shout",
                      help="Start reading shouts from START", metavar="START")
    parser.add_option("-l", "--login", dest="xmpp_login",
                      help="XMPP login JID.", metavar="JID")
    parser.add_option("-p", "--pass", dest="xmpp_pass",
                      help="XMPP password.", metavar="PASSWD")
    parser.add_option("-r", "--room", dest="xmpp_room",
                      help="Join this XMPP room.", metavar="ROOM")
    parser.add_option("-d", "--host", dest="xmpp_host",
                      help="Set XMPP host.", metavar="HOST")
    parser.add_option("-o", "--port", dest="xmpp_port",
                      help="Set XMPP port.", metavar="PORT")
    parser.add_option("-A", "--status", dest="xmpp_status",
                      help="Set default XMPP away status message.", metavar="STATUS")
    parser.add_option("-R", "--resource", dest="xmpp_resource",
                      help="Set XMPP resource for this client instance.", metavar="RESOURCE")
    parser.add_option("-L", "--loop", dest="loop_time",
                      help="Read shoutbox messages every SECS.", metavar="SECS")
    parser.add_option("-X", "--plugins", dest="plugins",
                      help="Load comma separated extensions/plugins.", metavar="PLUGINS")
    parser.add_option("-u", "--url", dest="base_url",
                      help="Read shoutbox messages from this URL.", metavar="URL")
    parser.add_option("-t", "--show-time", dest="show_time",
                      help="Prepend time to each message.")
    parser.add_option("-n", "--show-nick", dest="show_nick",
                      help="Prepend originating nick to each message.")
    parser.add_option("-b", "--bridge", dest="bridge_type",
                      help="Use this XMPP bridge class.", metavar="BRIDGE")
    parser.add_option("-B", "--shoutbox", dest="shoutbox_type",
                      help="Use this shoutbox connector class.", metavar="SHOUTBOX")
    parser.add_option("-H", "--db-host", dest="db_host",
                      help="Host for DB connector.", metavar="HOST")
    parser.add_option("-N", "--db-name", dest="db_name",
                      help="Name for DB connector.", metavar="NAME")
    parser.add_option("-U", "--db-user", dest="db_user",
                      help="User for DB connector.", metavar="USER")
    parser.add_option("-f", "--jid-field", dest="ubb_jid_field",
                      help="UBB.threads profile table field containing user JID.", metavar="FIELD")
    parser.add_option("-C", "--secret", dest="secret", metavar="SECRET",
                      help="Use this secret word to connect to MessageShoutbox server script.")
    parser.add_option("-F", "--date-format", dest="log_date_format",
                      help="Use this date format when logging.", metavar="FORMAT")
    return parser.parse_args()

if __name__ == '__main__':
    xml = loadUrl('http://www.rollspel.nu/forum/ubbthreads.php?ubb=listshouts')
    parser = ElementParser()
    dom = parser(xml)

