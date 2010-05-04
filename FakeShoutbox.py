# -*- coding: utf-8 -*-

import string
import types
from datetime import date
from datetime import datetime

from BridgeClass import *
from Shoutbox import *

class FakeShoutbox(Shoutbox):
    pass

def main():
    import sys
    import string
    from Conf import Conf
    ## MixIn testing:
    #import time
    #from MixIn import MixIn
    #s.mixinClass(Graemlin)
    #MixIn(Shout, Graemlin)
    #s = Shout(12, 34, "adsf", u'adsfäöåääö', time.time())
    #print s.dumpall()
    #quit()
    cfg = Conf('config.ini', 'LOCAL')
    sbox = FakeShoutbox(cfg)
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
