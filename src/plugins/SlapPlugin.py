# -*- coding: utf-8 -*-

import random

from plugins.Plugin import *
from utils.utilities import *

class SlapPlugin(Plugin):
    """
    Lets uses slap each other with hilarious items.
    """
    priority = 0
    name = "SlapPlugin"
    author = "Olle Johansson <Olle@Johansson.com>"
    description = "Slap bot lets users slap each other with hilarious items."
    commands = [
        dict(
            command = ['!slap'],
            handler = 'slap',
            onevents = ['Message'],
        ),
    ]

    def setup(self):
        """
        Setup method which is called once before any triggers methods are called.
        """
        self.slapitems = read_file("extras/slaps.dat")

    def slap(self, shout, command, comobj):
        """
        Parse message body and send message with dice roll.
        """
        words = shout.text.split()
        slapee = words[1]
        tmpl = string.Template(random.choice(self.slapitems).strip())
        if slapee and slapee.lower() != self.nick.lower():
            if slapee == 'Endyamon':
                slap = u"No, he likes it too much."
            else:
                slap = tmpl.substitute(dict(slapper=shout.name, slapee=slapee))
            self.bridge.send_and_shout(slap, self.nick)

