# -*- coding: utf-8 -*-

from plugins.Plugin import *
from utils.utilities import *

class KraetyzPlugin(Plugin):
    """
    Match texts from a list of users and returns a message.
    If any of the nicks in onsender writes a message that contains the text
    in textmatch, then the bot will send the text as a message, substituting
    %s for the nick of the sender.
    """
    priority = 0
    name = "KraetyzPlugin"
    author = "Olle Johansson <Olle@Johansson.com>"
    description = "Match texts from a list of users and returns a message."
    commands = [
        dict(
            command=[''],
            handler='send_warning',
            onevents=['Message'],
            onsender = ['Kraetyz'],
            textmatch = 'jag tycker',
            text = u"/me bannar %s för uttryckande av åsikt.",
        ),
    ]

    def send_warning(self, shout, command, comobj):
        """
        Parse message body and send message with dice roll.
        """
        if shout.name in comobj['onsender'] and shout.text.lower().find(comobj['textmatch']) >= 0:
            self.bridge.send_and_shout(comobj['text'] % (shout.name), self.nick)


