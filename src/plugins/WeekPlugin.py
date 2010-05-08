# -*- coding: utf-8 -*-

from datetime import date

from plugins.Plugin import *
from utils.utilities import *

class WeekPlugin(Plugin):
    """
    Returns the ISO week number.
    """
    priority = 0
    name = "WeekPlugin"
    author = "Olle Johansson <Olle@Johansson.com>"
    description = "Simple plugin to display current ISO week number."
    commands = [
        dict(
            command = ['!week', '!vecka'],
            handler = 'send_weeknr',
            onevents = ['Message'],
        ),
    ]

    def send_weeknr(self, shout, command, comobj):
        """
        Return the current ISO week number.
        """
        (isoyear, isoweek, isoweekday) = date.today().isocalendar()
        self.bridge.send_and_shout("Vecka: " + str(isoweek), self.nick)

