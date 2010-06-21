# -*- coding: utf-8 -*-

import os
import glob
import random
import linecache

from plugins.Plugin import *
from utils.utilities import *

class TermPlugin(Plugin):
    """
    Term bot can print definitions of terms, or print a random definition. 
    """
    priority = 0
    name = "TermPlugin"
    author = "Olle Johansson <Olle@Johansson.com>"
    description = "Term bot can print definitions of terms, or print a random definition."
    filename = "extras/definitions.dat"
    filename_newdefinitions = "extras/definitions_new.dat"
    separator = '%'
    commands = [
        dict(
            command=['!definiera', '!define', '!term add'],
            handler='add_term',
            onevents=['Message'],
        ),
        dict(
            command=['!term', '!definition'],
            handler='define_term',
            onevents=['Message'],
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

    def add_term(self, shout, command, comobj):
        newterm = shout.text.replace(command, '', 1).strip()
        if newterm:
            try:
                if string.find(newterm, '=') >= 0:
                    (term, definition) = newterm.split('=', 1)
                else:
                    (term, definition) = newterm.split(' ', 1)
            except ValueError:
                self.bridge.send_and_shout("Couldn't add definition.", self.nick)
                return
            newdefinition = term.strip() + '=' + definition.strip()
            add_line_to_file(self.filename_newdefinitions, newdefinition, separator=self.separator)
            self.bridge.send_and_shout("New definition added for review.", self.nick)

    def define_term(self, shout, command, comobj):
        """
        Parse message body and send message with dice roll.
        """
        if not shout.text:
            return
        #words = text.split()[1:]
        word = shout.text.replace(command, '', 1).strip()
        if not word:
            word = random.choice(self.definitions.keys())
        answer = ""
        #self.logprint('Handling term:', word)
        try:
            answer += u"Definition av '%s': %s" % (word, self.definitions[word.lower()])
        except KeyError:
            pass
        if not answer.strip():
            answer = "Hittade inga definitioner."
        self.bridge.send_and_shout(answer.strip(), self.nick)

