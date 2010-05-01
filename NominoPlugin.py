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
    nick = "HALiBot"
    path = "extras/nomino/"
    firstnames = dict()
    surnames = dict()
    commands = [
        dict(
            command=['!nomino', '!namn', '!name'],
            handler='randomize_name',
        ),
    ]

    def setup(self):
        """
        Setup method which is called once before any triggers methods are called.
        """
        self.firstnames = self.read_list_files("_names.txt")
        self.surnames = self.read_list_files("_surnames.txt")

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
        return namelist

    def randomize_name(self, text, nick, command, cmd):
        """
        Parse message body and send message with dice roll.
        """
        words = text.lower().split()
        fnlist = '*'
        if len(words) > 1:
            fnlist = words[1] 
        snlist = fnlist
        if len(words) > 2:
            snlist = words[2] 
        firstname = self.get_random_line(self.firstnames, fnlist).strip()
        surname = self.get_random_line(self.surnames, snlist).strip()
        name = "Slumpat namn: " + firstname + ' ' + surname
        self.bridge.send_and_shout(name, self.nick)

    def get_random_line(self, lists, listname='*'):
        if listname == '*':
            file = lists[random.choice(lists.keys())]
        else:
            try:
                file = lists[listname]
            except KeyError:
                return self.get_random_line(lists, '*')
        if not file:
            return None
        lineno = random.randint(0, file['linecount']-1)
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
