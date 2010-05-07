# -*- coding: utf-8 -*-

import platform
import time
from datetime import datetime, date

from utils.ObjectFactory import *
from utils.BridgeClass import *
from shoutbox.Shoutbox import *
from utils.utilities import *

class BridgeError(Exception):
    "Unknown Bridge Error"

class BridgeConnectionError(BridgeError):
    "Could not connect to XMPP."

class BridgeAuthenticationError(BridgeError):
    "Could not authenticate."

class BridgeWrongTypeError(BridgeError):
    "Incorrect type."

class BridgeMissingAttributeError(BridgeError):
    "A required attribute is missing."

class BridgeNoXmlStream(BridgeError):
    "No active xml stream available."

class XmppBridge(BridgeClass):
    client_name = "Shoutbridge"
    client_version = "1.0"
    shoutbox = None
    roster = dict()
    cfg = None
    last_time = 0
    plugins = dict()
    of = None

    def __init__(self, sbox=None, cfg=None):
        """
        Instantiate an XMPP bridge using XMPP login details and a shoutbox object.
        """
        # cfg.xmpp_login, cfg.xmpp_pass, cfg.xmpp_host, cfg.xmpp_port, cfg.xmpp_room
        if sbox:
            self.shoutbox = sbox
        if cfg:
            self.setConfig(cfg)

        # Update last active time.
        self.update_last_time()


    def setConfig(self, cfg):
        """
        Sets the config object and some default class attributes from config.
        """
        self.cfg = cfg
        self.login = self.cfg.xmpp_login
        self.passwd = self.cfg.xmpp_pass
        self.host = self.cfg.xmpp_host
        self.port = self.cfg.xmpp_port
        (self.room, foo, self.resource) = self.cfg.xmpp_room.rpartition('/')
        self.roomjid = self.cfg.xmpp_room
        self.current_nick = self.resource

    def setShoutbox(self, sbox):
        """
        Sets the shoutbox instance object for shoutbox communication.
        """
        self.shoutbox = sbox

    def setup(self, sbox=None, cfg=None):
        if sbox:
            self.setShoutbox(sbox)
        if cfg:
            self.setConfig(cfg)

        # Load list of plugins
        self.load_plugins(self.cfg.plugins)

        # Make an XMPP connection
        self.make_connection()

    def load_plugins(self, plugs):
        if not plugs:
            return
        if not self.of:
            self.of = ObjectFactory()
        pluginlist = plugs.split(',')
        for p in pluginlist:
            try:
                plug = self.of.create(p + "Plugin", mod='plugins', inst='Plugin', args=[self])
            except ImportError:
                self.logprint("Couldn't load plugin:", p)
                continue
            plug.setup()
            self.logprint("Loaded plugin:", plug.name, "\n", plug.description)
            self.plugins[p] = plug

    def trigger_plugin_event(self, event, obj):
        """
        Triggers given event on all loaded plugins with obj as argument.
        """
        if not obj or not event:
            return
        for plugin_name, plugin in self.plugins.items():
            try:
                text = obj.text
                nick = obj.name
            except AttributeError:
                text = obj
                nick = ""
            try:
                (cmd, comobj, func) = self.get_plugin_handler(plugin, event, text)
            except AttributeError:
                self.logprint("Attribute Error encountered in plugin:", plugin_name)
                continue
            try:
                if func:
                    self.logprint("Calling plugin:", plugin_name, event, cmd)
                    plugin.sender_nick = nick
                    func(obj, cmd, comobj)
            except Exception as e:
                self.logprint("Plugin raised exception:", plugin_name, "\n", e)

    def get_plugin_handler(self, plugin, event, text):
        text = text.lower()
        for comobj in plugin.commands:
            if event in comobj['onevents']:
                for cmd in comobj['command']:
                    if cmd == '' or text.startswith(cmd.lower()):
                        return [cmd, comobj, getattr(plugin, comobj['handler'])]
        return [None, None, None]

    def is_type(self, obj, cls):
        if type(obj).__name__ == 'instance':
            if obj.__class__.__name__ == cls:
                return True
        return False

    def make_connection(self):
        """
        Make an XMPP connection and authorize the user.
        """
        pass

    def close_connection(self):
        pass

    def rawDataIn(self, buf):
        print "RECV: %s" % unicode(buf, 'utf-8')

    def rawDataOut(self, buf):
        print "SEND: %s" % unicode(buf, 'utf-8')

    def connected(self, xs):
        pass

    def disconnected(self, xs):
        pass

    def authenticated(self, xs):
        print "Authenticated."
        # Connect to conference room
        self.join_room(self.roomjid)

    def leave_room(self, reason=None):
        if not reason:
            reason = "Leaving room."
        self.send_presence(
            to=room,
            ptype="unavailable",
            children=dict(
                status=dict(
                    defaultUri=None,
                    content=reason,
                ),
            ),
        )

    def join_room(self, room):
        #frm=self.login + '/' + self.cfg.xmpp_resource,
        self.send_presence(
            to=room,
            children=dict(
                x=dict(
                    defaultUri=u'http://jabber.org/protocol/muc',
                    content='',
                ),
                status=dict(
                    defaultUri=None,
                    content="I'm not here right now.",
                ),
                priority=dict(
                    defaultUri=None,
                    content='1',
                ),
            ),
        )
        # TODO: Answer room configuration request.
        # TODO: Wait until server responds on room join before continuing.

    def add_to_roster(self, nick, jid):
        if nick in self.roster:
            return self.roster[nick]
        try:
            user = self.shoutbox.getUserByJid(jid)
        except ShoutboxUserNotFoundError:
            # Default to anonymous user with JID as username
            user = User(1, jid, '')
        self.roster[nick] = user
        self.logprint("Adding to roster:", nick)
        return user

    def delete_from_roster(self, nick):
        if nick in self.roster:
            del self.roster[nick]
            self.logprint("Removing from roster:", nick)
            return True
        return False

    def get_from_roster(self, nick, jid):
        if not nick in self.roster:
            self.add_to_roster(nick, jid)
        return self.roster[nick]

    def remove_jid_from_roster(self, jid, nick=None):
        self.logprint("Removing self from roster:", jid, nick)
        if nick and nick in self.roster:
            usr = self.roster[nick]
            list = dict(nick=usr)
        else:
            list = self.roster
        if list:
            for k, u in list.items(): 
                if u.jid == jid:
                    self.delete_from_roster(k)

    def get_os_info(self):
        return str(platform.platform())

    def strip_tags(self, s):
        """
        Strip html tags from s
        """
        # this list is neccesarry because chk() would otherwise not know
        # that intag in strip_tags() is ment, and not a new intag variable in chk().
        intag = [False]

        def chk(c):
            if intag[0]:
                intag[0] = (c != '>')
                return False
            elif c == '<':
                intag[0] = True
                return False
            return True

        return ''.join(c for c in s if chk(c))

    def clean_message(self, text):
        """
        Clean text of unwanted content.
        """
        text = self.strip_tags(text)
        return text

    def update_last_time(self):
        self.last_time = time.time()

    def get_last_activity(self):
        return str(int(time.time() - self.last_time))

    def change_nick(self, nick):
        if self.cfg.show_nick == "True":
            return
        # If nick is unavailable, append "_" and try again.
        if nick and nick != self.current_nick:
            # If nick is already in roster, but with shoutbridge jid, remove it.
            self.remove_jid_from_roster(self.login, nick)
            if nick in self.roster:
                return self.change_nick(nick + '_')
            self.current_nick = nick
            self.send_presence(
                to=self.room + '/' + nick
            )
            return nick

    def send_stanza(self, stanza):
        pass

    def handle_iq(self, iq):
        """
        Handles incoming IQ stanzas and dispatches to specific handle methods.
        """
        pass

    def lookup_iq_method(self, command):
        return getattr(self, 'handle_iq_' + command.upper(), None) or self.handle_iq_DEFAULT

    def handle_iq_DEFAULT(self, frm=None, to=None, id=None, query=None):
        self.logprint("Unknown incoming IQ stanza:", frm, to, id, query)

    def handle_iq_GET(self, frm=None, to=None, id=None, query=None):
        """
        Handle IQ get stanzas.
        """
        # Default to sending back error for unknown get iq.
        self.send_iq_error(to=frm, id=id, query=query)

    def handle_iq_RESULT(self, frm=None, to=None, id=None, query=None):
        """
        IQ result is ignored.
        """
        pass

    def handle_iq_SET(self, frm=None, to=None, id=None, query=None):
        """
        IQ set not yet implemented, return error.
        """
        self.send_iq_error(to=frm, id=id, query=query)

    def handle_iq_ERROR(self, frm=None, to=None, id=None, query=None):
        """
        IQ error stanza is just logged.
        """
        self.logprint("Received IQ error stanza:", frm, id, query.toXml())

    def send_iq_version(self, frm=None, to=None, id=None):
        """
        Returns iq stanza with client and system information.
        """
        pass

    def send_iq_last(self, to=None, id=None):
        """
        Return IQ stanza with information on seconds since last client usage.
        """
        pass

    def send_iq_disco(self, frm=None, to=None, id=None, query=None):
        """
        Send IQ stanza with discovery information.
        """
        pass

    def send_iq_error(self, to=None, id=None, iqtype=None, query=None, condition=None):
        """
        Build and send IQ error stanza.
        """
        pass

    def send_iq(self, iqtype, id, frm=None, to=None, children=None, querytype=None):
        """
        Sends an IQ stanza on the xml stream.
        """
        pass

    def handle_presence(self, pres):
        """
        Handle presence stanzas.
        """
        pass

    def lookup_presence_method(self, command):
        return getattr(self, 'handle_presence_' + command.upper(), None) or self.handle_presence_DEFAULT

    def handle_presence_DEFAULT(self, pres, fromjid=None, **kwargs):
        pass

    def handle_presence_ERROR(self, pres, fromjid=None, **kwargs):
        pass

    def handle_presence_UNAVAILABLE(self, pres, nick=None, **kwargs):
        self.delete_from_roster(nick)

    def handle_presence_AVAILABLE(self, pres, fromstr=None, nick=None, **kwargs):
        user = self.add_to_roster(nick, fromstr)

    def handle_presence_UNSUBSCRIBE(self, pres, fromjid=None, **kwargs):
        self.send_presence(
            ptype="unsubscribed",
            to=fromjid,
        )

    def handle_presence_SUBSCRIBE(self, pres, fromjid=None, **kwargs):
        self.send_presence(
            ptype="subscribed",
            to=fromjid,
        )

    def send_presence_status(self, show=None, status=None):
        """
        Convenience method to send status information.
        """
        if status:
            self.cfg.xmpp_status = status
        else:
            status = self.cfg.xmpp_status
        if not show:
            show = "chat"
        self.send_presence(xmlns='jabber:client', show=show, status=status)

    def send_presence(self, xmlns=None, ptype=None, status=None, show=None,
                     frm=None, to=None, children=None):
        """
        Build and send presence stanza.
        """
        pass

    def handle_message(self, mess):
        """
        Handle an XMPP message.
        """
        pass

    def send_message(self, tojid, text, nick=None):
        """
        Send an text as XMPP message to tojid
        """
        pass

    def ping(self):
        """
        Emulate user being active by sending presence status to server and
        updating last active time.
        """
        self.update_last_time()
        pingnode = domish.Element(('urn:xmpp:ping', 'ping'))
        self.logprint("Sending ping and updating last active time.", pingnode)
        self.send_iq('get', children=[pingnode])

    def send_and_shout(self, text, nick=None):
        """
        Sends text to both xmpp room and shoutbox,
        using self.resource as nick if it isn't set.
        """
        if not nick:
            nick = self.resource
        user = User(1, nick, self.login)
        self.send_message(self.room, text, nick)
        #text = text.replace("\n", "<br />\n")
        self.shoutbox.sendShout(user, text)

    def process_shoutbox_messages(self):
        if not self.xmlstream:
            return False

        # Read shoutbox messages.
        # TODO: Should possibly use E-tag and options to see if anything has changed.
        msgs = self.shoutbox.readShouts()
        #self.logprint("Number of messages received:", len(msgs))
        if not msgs:
            return False
        for m in msgs:
            text = self.clean_message(m.text)
            if self.cfg.show_time == "True" and self.cfg.show_nick == "True":
                text = "%s <%s> %s" % (m.time, m.name, text)
            elif self.cfg.show_time == "True":
                text = "%s %s" % (m.time, text)
            elif self.cfg.show_nick == "True":
                text = "<%s> %s" % (m.name, text)
            self.send_message(self.room, text, nick=m.name)

            # Trigger handleShoutMessage event
            self.trigger_plugin_event('Message', m)
            self.trigger_plugin_event('ShoutMessage', m)

    def listen(self):
        """
        Start listening on XMPP and Shoutbox, relaying messages.
        """
        pass

