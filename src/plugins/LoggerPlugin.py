# -*- coding: utf-8 -*-

from plugins.Plugin import *

class LoggerPlugin(Plugin):
    """
    Logs all messages to file.
    """
    priority = 0
    name = "LoggerPlugin"
    author = "Olle Johansson"
    description = "Message logger plugin."

    def setup(self):
        """
        Setup method which is called once before any triggers methods are called.
        """
        # FileLogger object not created yet.
        self.log = FileLogger("./message.log")

    def handleXmppMessage(self, message):
        """
        Method called on every received XMPP message stanza.
        Message can be modified and must be returned.
        """
        self.log.logprint(message.__str__())
        return message

    def handleShoutMessage(self, shout):
        """
        Method called on every new message from the Shoutbox.
        Shout message can be modified, and must be returned.
        """
        self.log.logprint(shout.__str__())
        return shout

