# -*- coding: utf-8 -*-

"""
The MIT License

Copyright (c) 2010 Olle Johansson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import string
import types
from datetime import date
from datetime import datetime

from utils.pyanno import raises, abstractMethod, returnType, parameterTypes, deprecatedMethod, \
                         privateMethod, protectedMethod, selfType, ignoreType, callableType, \
                         ClassName

from utils.BridgeClass import *
from utils.Conf import Conf

class ShoutboxError(Exception):
    "Unknown Shoutbox error"

class ShoutboxUserNotFoundError(ShoutboxError):
    "Found no such user."

class User(BridgeClass):
    id = 0
    name = ""
    jid = ""
    last_seen = 0

    def __init__(self, id, name, jid, last_seen=None):
        if id:
            self.id = int(id)
        else:
            self.id = None
        self.name = name
        self.jid = jid
        self.last_seen = last_seen

    def __repr__(self):
        return "<User(%s, '%s','%s', '%s')>" % (self.id, self.name, self.jid, self.last_seen)

class Shout(BridgeClass):
    """
    SHOUT_ID, USER_ID, SHOUT_DISPLAY_NAME, SHOUT_TEXT, SHOUT_TIME
    """
    def __init__(self, id, userid, name, text, time):
        self.id = int(id)
        self.userid = int(userid)
        self.name = name
        self.text = text
        d = datetime.fromtimestamp(int(time))
        if date.today() == datetime.date(d):
            self.time = d.strftime('%H:%M')
        else:
            self.time = d.strftime('%Y-%m-%d %H:%M')


class Graemlin(BridgeClass):
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

class Shoutbox(BridgeClass):
    latest_shout = 0
    graemlins = None

    def __init__(self, cfg=None):
        if cfg:
            self.setConfig(cfg)

    def __del__(self):
        pass

    @parameterTypes( selfType, 'Conf' )
    def setConfig(self, config):
        """
        Updates the configuration.
        """
        self.cfg = config
        if self.cfg.latest_shout:
            self.latest_shout = int(self.cfg.latest_shout)

    @abstractMethod
    @parameterTypes( selfType )
    def read_graemlin_list(self):
        """
        Returns a list of Graemlin objects.
        """
        pass

    @privateMethod
    @parameterTypes( selfType, str, str )
    @returnType( User )
    def _getUserByField(self, field, id):
        """
        Retrieves User information based on a db field and value.
        """
        if not id:
            return User(1, 'Anonymous', '')
        usr = User(1, id, '')
        return usr

    @parameterTypes( selfType, str )
    @returnType( User )
    def getUserByUsername(self, username):
        """
        Retrieves User information based on a username
        """
        return self._getUserByField("u.USER_DISPLAY_NAME", username)

    @parameterTypes( selfType, str )
    @returnType( User )
    def getUserById(self, id):
        """
        Retrieves User information based on an id.
        """
        return self._getUserByField("u.USER_ID", id)

    @parameterTypes( selfType, str )
    @returnType( User )
    def getUserByJid(self, jid):
        """
        Retrieves User information based on an XMPP login.
        """
        return self._getUserByField('', jid)

    @abstractMethod
    @parameterTypes( selfType, 'User', str )
    def sendShout(self, user, message):
        """
        Send a shoutbox message from a user.
        """
        pass

    @abstractMethod
    @parameterTypes( selfType, int )
    @returnType( list )
    def readShouts(self, start=-1):
        """
        Read shoutbox messages, all or newer than "start".
        """
        return []

    @parameterTypes( selfType, str )
    @returnType( str )
    def replace_graemlins(self, text):
        if text.find('<<GRAEMLIN_URL>>') < 0:
            return text
        for s in self.graemlins:
            text = text.replace(s.get_html(), s.get_code())
        return text


def main():
    import sys
    import string
    from Conf import Conf
    cfg = Conf('config.ini', 'LOCAL')
    sbox = Shoutbox(cfg)
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
