# -*- coding: utf-8 -*-

from datetime import date

from plugins.Plugin import *
from utils.utilities import *

class NamePlugin(Plugin):
    """
    Returns the names of today in the Swedish calendar.
    """
    priority = 0
    name = "NamePlugin"
    author = "Olle Johansson <Olle@Johansson.com>"
    description = "Plugin that prints names from the Swedish calendar."
    commands = [
        dict(
            command=['!dagensnamn'],
            handler='send_names',
            onevents=['Message'],
        ),
    ]
    names = []

    def setup(self):
        """
        Setup method which is called once before any triggers methods are called.
        """
        self.names = read_file("extras/names.dat")

    def send_names(self, shout, command, comobj):
        """
        Parse message body and send message with dice roll.
        """
        d = date.today()
        day = int(d.strftime("%j")) - 1
        names = self.names[day]
        self.bridge.send_and_shout(names, self.nick)

