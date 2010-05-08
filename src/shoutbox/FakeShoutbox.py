# -*- coding: utf-8 -*-

from utils.BridgeClass import *
from shoutbox.Shoutbox import *

class FakeShoutbox(Shoutbox):
    @parameterTypes( selfType, 'User', str )
    def sendShout(self, user, message):
        """
        Send a shoutbox message from a user.
        """
        pass

    @parameterTypes( selfType, int )
    @returnType( list )
    def readShouts(self, start=-1):
        """
        Read shoutbox messages, all or newer than "start".
        """
        return []

def main():
    import sys
    import string
    from Conf import Conf
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
