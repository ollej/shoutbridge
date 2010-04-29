# -*- coding: utf-8 -*-

import os
import glob
import random
import linecache

from Plugin import *
from utilities import *

class NominoPlugin(Plugin):
    """
    Nomino bot can generate random names from different lists.
    """
    priority = 0
    name = "NominoPlugin"
    author = "Olle Johansson <Olle@Johansson.com>"
    description = "Nomino bot can generate random names from different lists."
    command = '!nomino'
    nick = "HALiBot"
    path = "extras/nomino/"
    firstnames = dict()
    surnames = dict()

    def setup(self):
        """
        Setup method which is called once before any triggers methods are called.
        """
        self.firstnames = self.read_list_files("_names.txt")
        self.surnames = self.read_list_files("_surnames.txt")
        self.logprint("Firstnames:", self.firstnames)
        self.logprint("Surnames:", self.surnames)

    def read_list_files(self, listtype):
        namelist = dict()
        refn = re.compile(listtype + "$");
        for infile in glob.glob( os.path.join(self.path, '*' + listtype) ):
            listname = os.path.basename(infile).lower()
            listname = re.sub(refn, '', listname)
            listname = listname.replace(' ', '')
            linecount = file_len(infile)
            if linecount:
                namelist[listname] = dict(linecount=linecount, filename=infile)
            print "Namefile:", infile, listname, linecount
        return namelist

    def handleXmppMessage(self, message):
        """
        Method called on every received XMPP message stanza.
        """
        body = getElStr(message.body)
        self.randomize_name(body, message['nick'])

    def handleShoutMessage(self, shout):
        """
        Method called on every new message from the Shoutbox.
        """
        self.randomize_name(shout.text, shout.name)

    def randomize_name(self, text, nick):
        """
        Parse message body and send message with dice roll.
        """
        self.logprint("NominoPlugin: Handling message:", nick, text)
        if self.command == '' or text.startswith(self.command):
            words = text.lower().split()
            fnlist = '*'
            if len(words) > 1:
                fnlist = words[1] 
            snlist = fnlist
            if len(words) > 2:
                snlist = words[2] 
            self.logprint("Selections:", fnlist, snlist)
            firstname = self.get_random_line(self.firstnames, fnlist).strip()
            surname = self.get_random_line(self.surnames, snlist).strip()
            self.logprint("Namn:", firstname, surname)
            name = "Slumpat namn: " + firstname + ' ' + surname
            self.bridge.send_and_shout(name, self.nick)

    def get_random_line(self, lists, listname='*'):
        self.logprint("Lists:", lists)
        if listname == '*':
            file = lists[random.choice(lists.keys())]
        else:
            try:
                file = lists[listname]
            except KeyError:
                return self.get_random_line(lists, '*')
        if not file:
            return None
        self.logprint("File.", file)
        lineno = random.randint(0, file['linecount']-1)
        self.logprint("Selection:", file['filename'], lineno)
        return linecache.getline(file['filename'], lineno)


def main():
    import sys
    import string
    from time import time
    from Conf import Conf
    import Shoutbox
    cfg = Conf('config.ini', 'LOCAL')
    args = sys.argv
    msg = ' '.join(args[1:])
    shout = Shoutbox.Shout(1, 4711, 'Test', msg, time())
    bridge = FakeBridge()
    plug = NominoPlugin([bridge])
    plug.setup()
    print "Returned:", plug.handleShoutMessage(shout)

# Call the main function.
if __name__ == '__main__':
    main()
