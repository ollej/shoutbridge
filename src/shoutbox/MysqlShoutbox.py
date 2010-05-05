# -*- coding: utf-8 -*-

import MySQLdb
from datetime import date
from datetime import datetime

from shoutbox.Shoutbox import *
from utils.utilities import *
from bridge.XmppBridge import *

class MysqlShoutbox(XmppBridge):
    db_host = ""
    db_name = ""
    db_user = ""
    db_pass = ""
    db_tbl_shoutbox = "ubbt_SHOUT_BOX"
    db_tbl_user = "ubbt_USERS"
    db_tbl_profile = "ubbt_USER_PROFILE"
    db_fld_profile = "USER_EXTRA_FIELD_1"
    db_tbl_graemlins = "ubbt_GRAEMLINS"
    latest_shout = 0
    db = None
    graemlins = None

    def __init__(self, cfg):
        self.cfg = cfg
        self.db_name = cfg.db_name
        self.db_user = cfg.db_user
        self.db_pass = cfg.db_pass
        self.db_host = cfg.db_host
        if cfg.latest_shout:
            self.latest_shout = cfg.latest_shout
        if cfg.ubb_jid_field:
            self.db_fld_profile = cfg.ubb_jid_field
        self.connectDb()

    def __del__(self):
        self.db.close()
        self.conn.close()

    def connectDb(self):
        """
        Connects to a MySQL database.

        CREATE TABLE  `ubbt_USER_XMPP` (
        `XMPP_USER_ID` INT NOT NULL ,
        `XMPP_LOGIN` VARCHAR( 255 ) NOT NULL ,
        `XMPP_PASSWD` VARCHAR( 255 ) NOT NULL ,
        PRIMARY KEY (  `XMPP_USER_ID` )
        ) ENGINE = MYISAM
        """
        self.conn = MySQLdb.connect (host = self.db_host,
                               user = self.db_user,
                               passwd = self.db_pass,
                               db = self.db_name)
        self.db = self.conn.cursor()
        self.graemlins = self.read_graemlin_list()

    def read_graemlin_list(self):
        """
        GRAEMLIN_MARKUP_CODE    GRAEMLIN_SMILEY_CODE    GRAEMLIN_IMAGE  GRAEMLIN_IS_ACTIVE  GRAEMLIN_WIDTH  GRAEMLIN_HEIGHT 
        """
        sql = "SELECT GRAEMLIN_MARKUP_CODE, GRAEMLIN_SMILEY_CODE, GRAEMLIN_IMAGE, GRAEMLIN_WIDTH, GRAEMLIN_HEIGHT FROM " + self.db_tbl_graemlins
        self.db.execute(sql)
        rows = self.db.fetchall()
        graemlins = []
        for g in rows:
            graemlins.append(Graemlin(g[0], g[1], g[2], g[3], g[4]))
        return graemlins

    def _getUserByField(self, field, id):
        """
        Retrieves User information based on a db field and value.
        """
        if not id:
            return User(1, 'Anonymous', '')
        sql = "SELECT u.USER_ID, u.USER_DISPLAY_NAME, " + self.db_fld_profile + " AS JIDLOGIN FROM " + self.db_tbl_user + " u LEFT OUTER JOIN " + self.db_tbl_profile + " x ON u.USER_ID = x.USER_ID WHERE " + field + " = %s"
        print "SQL: " + sql
        print "ID: " + id
        self.db.execute(sql, id)
        row = self.db.fetchone()
        if row:
            usr = User(row[0], row[1], row[2])
        else:
            raise ShoutboxUserNotFoundError
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

    def getXmppDetails(self, userid):
        """
        Retrieves XMPP login details based on a userid.
        """
        sql = "SELECT XMPP_LOGIN, XMPP_PASSWD FROM " + self.db_tbl_xmpp + " WHERE XMPP_USER_ID = %s"
        self.db.execute(sql, userid)
        row = self.db.fetchone()
        return row

    def sendShout(self, user, message):
        """
        Send a shoutbox message from a user.
        """
        sql = "INSERT INTO " + self.db_tbl_shoutbox + " (USER_ID, SHOUT_DISPLAY_NAME, SHOUT_TEXT, SHOUT_TIME, USER_IP) VALUES ( %s, %s, %s, UNIX_TIMESTAMP(), %s)"
        data = (user.id, user.name, unicode(message), '127.0.0.1')
        self.db.execute(sql, data)

    def readShouts(self, start=-1):
        """
        Read shoutbox messages, all or newer than "start".
        """
        if start < 0:
            start = self.latest_shout
        sql = "SELECT SHOUT_ID, USER_ID, SHOUT_DISPLAY_NAME, SHOUT_TEXT, SHOUT_TIME FROM " + self.db_tbl_shoutbox + " WHERE SHOUT_ID > %s AND USER_IP<>'127.0.0.1' ORDER BY SHOUT_ID ASC"
        self.db.execute(sql, start)
        rows = self.db.fetchall()
        # Keep track of the latest shout
        if len(rows) > 0:
            latest = rows[-1]
            self.latest_shout = latest[0]
        shouts = []
        for s in rows:
            text = self.replace_graemlins(s[3])
            shouts.append(Shout(s[0], s[1], s[2], text, s[4]))
        return shouts

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
