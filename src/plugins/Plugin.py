# -*- coding: utf-8 -*-

import random

from bridges.XmppBridge import *
from utils.BridgeClass import *
from utils.utilities import *

class PluginError(Exception):
    """
    Default Plugin exception.
    """

class FakeBridge(XmppBridge):
    """
    Fake bridge used for running plugins from command line.
    """
    def send_and_shout(self, text, nick=None):
        print "Message: ", nick, text

class Plugin(BridgeClass):
    """
    Superclass for Shoutbridge plugins.
    Methods should be implemented by sub-classes.
    All configured plugins will be setup by the Shoutbridge software on
    startup. Then the handle* methods will be triggered on specific events.
    """
    priority = 0
    name = "Plugin"
    author = "Olle Johansson"
    description = "Default Shoutbridge plugin interface."
    nick = 'HALiBot'
    bridge = None
    commands = []

    def __init__(self, args):
        try:
            self.bridge = args[0]
        except AttributeError:
            self.logprint("No bridge object given.")
            raise PluginError

    def setup(self):
        """
        Setup method which is called once before any triggers methods are called.
        """
        pass

    def prepend_sender(self, text, sep=': '):
        """
        Prepends name of sender of message if available.
        """
        try:
            if self.sender_nick:
                text = "%s%s%s" % (self.sender_nick, sep, text)
        except AttributeError:
            pass
        return text

    def strip_command(self, text, command):
        return text.replace(command, '', 1).strip()

    def send_message(self, text):
        """
        Send text as message to both Shoutbox and Jabber conference.
        Prepends name of sender to message.
        """
        text = self.prepend_sender(text)
        self.bridge.send_and_shout(text, self.nick)

    def show_text(self, shout, command=None, comobj=None):
        """
        Display text from command.
        """
        try:
            nick = comobj['nick']
        except KeyError:
            nick = self.nick
        self.bridge.send_and_shout(random.choice(comobj['text']), nick)


