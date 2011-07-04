# -*- coding: utf-8 -*-

"""
The MIT License

Copyright (c) 2011 Olle Johansson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from twisted.protocols import basic
from twisted.internet import protocol
from twisted.application import service, internet

import unicodedata

from plugins.GoldQuest import *

class GoldQuestServer(basic.LineReceiver):
    prompt_text = "GoldQuest> "
    lastcmd = None

    def connectionMade(self):
        print "Got new client!"
        self.sendLine("Welcome to Gold Quest!")
        self.showHelp()
        self.factory.clients.append(self)

    def connectionLost(self, reason):
        print "Lost a client!"
        self.factory.clients.remove(self)

    def lineReceived(self, line):
        print "received", repr(line)
        if line.lower() == "quit":
            self.sendLine("Thanks for playing Gold Quest.")
            self.stopProducing()
            return
        elif line.lower() == "help":
            self.showHelp()
            return
        if not line and self.lastcmd:
            line = self.lastcmd
        self.lastcmd = line
        msg = game.play(line)
        if msg:
            print "msg:", msg
            for c in self.factory.clients:
                if c == self:
                    c.message(msg)
                else:
                    c.message("\n" + msg)
        else:
            self.message("Unknown command: %s" % line)

    def message(self, message):
        if isinstance(message, unicode):
            message = unicodedata.normalize('NFKD', message).encode('ascii', 'ignore')
        #self.transport.write(message)
        self.sendLine(message)
        self.prompt()

    def showHelp(self):
        self.sendLine("Available commands: fight, loot, deeper, rest, charsheet, quit")
        self.prompt()

    def prompt(self):
        self.transport.write(self.prompt_text)


factory = protocol.ServerFactory()
factory.protocol = GoldQuestServer
factory.clients = []

cfg = Conf('../config.ini', 'LOCAL')
cfg.set('debug', True)
game = GoldQuest(cfg)

application = service.Application("GoldQuest")
internet.TCPServer(1025, factory).setServiceParent(application)

