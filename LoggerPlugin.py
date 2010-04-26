# -*- coding: utf-8 -*-

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

def main():
    import sys
    import string
    from time import time
    from Conf import Conf
    import shoutbox
    cfg = Conf('config.ini', 'LOCAL')
    shout = shoutbox.Shout(1, 4711, 'Test', 'A quick brown fox...', time())
    plug = Plugin()
    plug.setup()
    print plug.handleShoutMessage(shout)

# Call the main function.
if __name__ == '__main__':
    main()
