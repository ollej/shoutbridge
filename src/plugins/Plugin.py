# -*- coding: utf-8 -*-

import random

from utils.pyanno import raises, abstractMethod, returnType, parameterTypes, deprecatedMethod, \
                          privateMethod, protectedMethod, selfType, ignoreType, callableType

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
    #: Priority of the Plugin. Use this to control order of plugin calling.
    priority = 0
    #: Name of the Plugin
    name = "Plugin"
    #: Author of the Plugin.
    author = "Olle Johansson"
    #: Short description of the Plugin. Shown by !help command.
    description = "Default Shoutbridge plugin interface."
    #: Default nick to use when sending messages from this Plugin.
    nick = 'HALiBot'
    #: Contains a reference to the XmppBridge that has loaded this plugin.
    bridge = None
    #: List of command objects describing commands and respective handler methods.
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

    @protectedMethod
    @parameterTypes( selfType, str, str )
    @returnType( str )
    def prepend_sender(self, text, sep=': '):
        """
        Returns I{text} with name of sender prepended, separated by I{sep}.
        """
        try:
            if self.sender_nick:
                text = "%s%s%s" % (self.sender_nick, sep, text)
        except AttributeError:
            pass
        return text

    @protectedMethod
    @parameterTypes( selfType, str, str )
    @returnType( str )
    def strip_command(self, text, command):
        """
        Returns I{text} with I{command} stripped away from the beginning.
        """
        return text.replace(command, '', 1).strip()

    @protectedMethod
    @parameterTypes( selfType, str )
    def send_message(self, text):
        """
        Send text as message to both Shoutbox and Jabber conference.
        Prepends name of sender to message.
        """
        text = self.prepend_sender(text)
        self.bridge.send_and_shout(text, self.nick)

    @parameterTypes( selfType, Shout, str, dict )
    def show_text(self, shout, command=None, comobj=None):
        """
        A command handler that sends a message with a random string from the 
        list in the I{text} element of the command object.
        If the command object has a I{nick} attribute, this will be used
        as the nick when sending the text, otherwise the default plugin
        nick will be used.
        """
        try:
            nick = comobj['nick']
        except KeyError:
            nick = self.nick
        self.bridge.send_and_shout(random.choice(comobj['text']), nick)


