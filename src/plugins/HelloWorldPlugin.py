# -*- coding: utf-8 -*-

from plugins.Plugin import *

class HelloWorldPlugin(Plugin):
    name = "HelloWorldPlugin"
    author = "Your Name"
    description = "A simple Hello World plugin."
    commands = [
        dict(
            command = ['!hello'],
            handler = 'hello_world',
            onevents = ['Message'],
        )
    ]

    def hello_world(self, shout, command, comobj):
        self.send_message("Hello World!")

