# -*- coding: utf-8 -*-

import os
import glob
import random
import linecache

from Plugin import *
from utilities import *

class TermPlugin(Plugin):
    """
    Term bot can print definitions of terms, or print a random definition. 
    """
    priority = 0
    name = "TermPlugin"
    author = "Olle Johansson <Olle@Johansson.com>"
    description = "Term bot can print definitions of terms, or print a random definition."
    command = '!term'
    nick = "HALiBot"
    path = "extras/definitions.dat"
    definitions = dict()

    def setup(self):
        """
        Setup method which is called once before any triggers methods are called.
        """
        self.definitions = self.read_definitions(self.path)

    def read_definitions(self, file):
        definitions = dict()
        lines = read_file(file)
        for line in lines:
            # TODO: Maybe send a function ref to read_file for handling each line.
            (term, definition) = line.split("=", 1)
            definitions[term.lower()] = definition.strip()
        return definitions

    def handleXmppMessage(self, message):
        """
        Method called on every received XMPP message stanza.
        """
        body = getElStr(message.body)
        self.randomize_name(body, message['nick'])

    def handleShoutMessage(self, shout):
        """
        Method called on every new message from the Shoutbox.
        """
        self.randomize_name(shout.text, shout.name)

    def randomize_name(self, text, nick):
        """
        Parse message body and send message with dice roll.
        """
        self.logprint("TermPlugin: Handling message:", nick, text)
        if self.command == '' or text.startswith(self.command):
            if not text:
                return
            words = text.split()[1:]
            if not words:
                words = [random.choice(self.definitions.keys())]
            answers = ""
            for w in words:
                self.logprint('Handling term:', w)
                try:
                    answers += "Definition av '" + w + "': " + self.definitions[w.lower()] + "\n"
                except KeyError:
                    pass
            self.bridge.send_and_shout(answers.strip(), self.nick)

def main():
    import sys
    import string
    from time import time
    from Conf import Conf
    import Shoutbox
    cfg = Conf('config.ini', 'LOCAL')
    args = sys.argv
    msg = ' '.join(args[1:])
    shout = Shoutbox.Shout(1, 4711, 'Test', msg, time())
    bridge = FakeBridge()
    plug = TermPlugin([bridge])
    plug.setup()
    print "Returned:", plug.handleShoutMessage(shout)

# Call the main function.
if __name__ == '__main__':
    main()
