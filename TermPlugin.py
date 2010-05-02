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
    filename = "extras/definitions.dat"
    filename_newdefinitions = "extras/definitions_new.dat"
    separator = '%'
    commands = [
        dict(
            command=['!definiera', '!define', '!term add'],
            handler='add_term',
        ),
        dict(
            command=['!term', '!definition'],
            handler='define_term',
        ),
    ]
    definitions = dict()

    def setup(self):
        """
        Setup method which is called once before any triggers methods are called.
        """
        self.definitions = self.read_definitions(self.filename)

    def read_definitions(self, file):
        definitions = dict()
        lines = read_file(file)
        for line in lines:
            # TODO: Maybe send a function ref to read_file for handling each line.
            try:
                (term, definition) = line.split("=", 1)
            except ValueError:
                self.logprint("Couldn't add definition:", line)
                continue
            for t in term.split(','):
                definitions[t.lower()] = definition.strip()
        return definitions

    def handleXmppMessage(self, message):
        """
        Method called on every received XMPP message stanza.
        """
        body = getElStr(message.body)
        self.handle_shout(body, message['nick'])

    def handleShoutMessage(self, shout):
        """
        Method called on every new message from the Shoutbox.
        """
        self.handle_shout(shout.text, shout.name)

    def add_term(self, text, nick, command, cmd):
        newterm = text.replace(command, '', 1).strip()
        if newterm:
            try:
                (term, definition) = newterm.split('=', 1)
            except ValueError:
                self.bridge.send_and_shout("Couldn't add definition.", self.nick)
                return
            newdefinition = term.strip() + '=' + definition.strip()
            add_line_to_file(self.filename_newdefinitions, newdefinition, separator=self.separator)
            self.bridge.send_and_shout("New definition added for review.", self.nick)

    def define_term(self, text, nick, command, cmd):
        """
        Parse message body and send message with dice roll.
        """
        if not text:
            return
        #words = text.split()[1:]
        word = text.replace(command, '', 1).strip()
        if not word:
            word = [random.choice(self.definitions.keys())]
        answer = ""
        self.logprint('Handling term:', word)
        try:
            answer += "Definition av '" + word + "': " + self.definitions[word.lower()] + "\n"
        except KeyError:
            pass
        if not answer.strip():
            answer = "Hittade inga definitioner."
        self.bridge.send_and_shout(answer.strip(), self.nick)

def main():
    import sys
    import string
    from time import time
    from Conf import Conf
    import Shoutbox
    cfg = Conf('config.ini', 'LOCAL')
    args = sys.argv
    msg = unicode(' '.join(args[1:]), 'utf-8')
    shout = Shoutbox.Shout(1, 4711, 'Test', msg, time())
    bridge = FakeBridge()
    plug = TermPlugin([bridge])
    plug.setup()
    print "Returned:", plug.handleShoutMessage(shout)

# Call the main function.
if __name__ == '__main__':
    main()
