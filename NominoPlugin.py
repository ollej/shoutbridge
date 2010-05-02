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
            command=['!nomino list', '!namn list', '!name list', '!nomino help', '!namn help', '!name help'],
            handler='list_lists',
        ),
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

    def list_lists(self, text, nick, command, cmd):
        info = u"Förnamnslistor: "
        info += ' '.join(self.firstnames.keys())
        info += u"\nEfternamnslistor: "
        info += ' '.join(self.surnames.keys())
        self.bridge.send_and_shout(info, self.nick)

    def randomize_name(self, text, nick, command, cmd):
        """
        Parse message body and send message with dice roll.
        """
        words = text.lower().split()
        count = 1
        gender = None
        remove = []
        for w in words:
            if w in ('woman', 'women', 'female', 'females', 'kvinna', 'kvinnor'):
                gender = 'F'
                remove.append(w)
            elif w in ('male', 'males', 'men', 'man', u'män'):
                gender = 'M'
                remove.append(w)
            elif w.isdigit():
                count = int(w)
                remove.append(w)
        for r in remove:
            words.remove(r)
        fnlist = '*'
        if len(words) > 1:
            fnlist = words[1] 
        snlist = fnlist
        if len(words) > 2:
            snlist = words[2] 
        if count > 10:
            count = 10
        name = "Namn:" 
        for c in range(count):
            name += " " + self.get_random_name(fnlist, snlist, gender)
        self.bridge.send_and_shout(name, self.nick)

    def get_random_name(self, fnlist, snlist, onlygender=None):
        firstname = self.get_random_line(self.firstnames, fnlist).strip()
        try:
            (gender, firstname) = firstname.split(' ', 1)
        except ValueError:
            gender = u"Unknown"
        if onlygender and onlygender in ('M', 'F') and onlygender != gender:
            # Inefficient way to make sure a correct gender is returned.
            return self.get_random_name(fnlist, snlist, onlygender)
        if gender == 'M':
            gender = u'Male'
        else:
            gender = u'Female'
        surname = self.get_random_line(self.surnames, snlist).strip()
        name = u"%s %s (%s)" % (firstname, surname, gender)
        return name

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
        return unicode(linecache.getline(file['filename'], lineno), "utf-8")


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
