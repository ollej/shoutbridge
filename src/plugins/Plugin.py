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
        print "Message:", nick, text

class Plugin(BridgeClass):
    """
    Superclass for Shoutbridge plugins.

    All configured plugins will be setup by the Shoutbridge software on
    startup. The C{commands} attribute should contain a list of command
    objects. These will be read by Shoutbridge to determine which
    methods to call on different events.

    >>> p = Plugin([FakeBridge()])
    >>> p.strip_command("!hi there", "!hi")
    'there'
    >>> p.strip_command("!hi there", "!hello")
    '!hi there'
    >>> p.send_message("Hello World!")
    Message: HALiBot Hello World!
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
        Returns C{text} with name of sender prepended, separated by C{sep}.
        """
        try:
            if self.sender_nick:
                text = "%s%s%s" % (self.sender_nick, sep, text)
        except AttributeError:
            pass
        return text

    @parameterTypes( selfType, str, str )
    @returnType( str )
    def strip_command(self, text, command):
        """
        Returns C{text} with C{command} stripped away from the beginning.
        """
        return text.replace(command, '', 1).strip()

    @parameterTypes( selfType, str )
    def send_message(self, text):
        """
        Send text as message to both Shoutbox and Jabber conference.
        Prepends name of sender to message.
        """
        text = self.prepend_sender(text.strip())
        self.bridge.send_and_shout(text, self.nick)

    @parameterTypes( selfType, Shout, str, dict )
    def show_text(self, shout, command=None, comobj=None):
        """
        A command handler that sends a message with a random string from the 
        list in the C{text} element of the command object.
        If the command object has a C{nick} attribute, this will be used
        as the nick when sending the text, otherwise the default plugin
        nick will be used.
        """
        try:
            nick = comobj['nick']
        except KeyError:
            nick = self.nick
        self.bridge.send_and_shout(random.choice(comobj['text']), nick)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
