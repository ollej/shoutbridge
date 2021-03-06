# -*- coding: utf-8 -*-

"""
The MIT License

Copyright (c) 2010 Olle Johansson

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

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Sequence, create_engine
from sqlalchemy.orm import mapper, sessionmaker
import time
import string

from plugins.Plugin import *
from shoutbox.Shoutbox import *

class Tell(object):
    id = 0
    user = ""
    teller = ""
    message = ""
    time_told = 0

    def __init__(self, user, teller, message, time_told=None):
        self.user = user
        self.teller = teller
        self.message = message
        if time_told:
            self.time_told = time_told
        else:
            self.time_told = time.time()

class SeenTellPlugin(Plugin):
    name = "SeenTellPlugin"
    author = "Olle Johansson"
    description = "Keeps tracks of users and can tell when they were last online. It's also possible to leave messages for users."
    date_format = "%Y-%m-%d %H:%M:%S"
    commands = [
        dict(
            command = ['!tell', '!till'],
            handler = 'tell_user',
            onevents = ['Message'],
            defaultmessage = "Use '!tell Username Message' to tell a user something when they next join the chat.",
        ),
        dict(
            command = ['!seen', '!sett'],
            handler = 'seen_user',
            onevents = ['Message'],
        ),
        dict(
            command = [''],
            handler = 'handle_message',
            onevents = ['Message'],
        ),
    ]

    def setup(self):
        """
        Setup Sqlite SQL tables and start a db session.

        The database will be saved in C{extras/halibot.db}

        Calls L{setup_tables} to setup table metadata and L{setup_session}
        to instantiate the db session.
        """
        try:
            debug = self.bridge.cfg.get_bool('debug')
        except AttributeError:
            debug = False
        self.engine = create_engine('sqlite:///extras/halibot.db', echo=debug)
        self.setup_tables()
        self.setup_session()

    def setup_session(self):
        """
        Start a SQLAlchemy db session.

        Saves the session instance in C{self.session}
        """
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def setup_tables(self):
        """
        Defines the tables to use for L{User} and L{Tell}.

        The Metadata instance is saved to C{self.metadata}
        """
        self.metadata = MetaData()
        users_table = Table('users', self.metadata,
            Column('id', Integer, Sequence('user_id_seq'), primary_key=True),
            Column('name', String(50)),
            Column('jid', String(50)),
            Column('last_seen', Integer),
        )
        mapper(User, users_table)
        tell_table = Table('tell', self.metadata,
            Column('id', Integer, Sequence('user_id_seq'), primary_key=True),
            Column('user', String(50)),
            Column('teller', String(50)),
            Column('message', String(255)),
            Column('time_told', Integer),
        )
        mapper(Tell, tell_table)
        self.metadata.create_all(self.engine)

    def add_user(self, user):
        """
        Add a L{User} object to the database.
        """
        self.session.add(user)

    def get_user(self, name):
        """
        Returns first L{Üser} object from database with the name C{name}.
        """
        return self.session.query(User).filter(User.name.like(name)).first() 

    def add_tell(self, tell):
        """
        Add a L{Tell} object to the database.
        """
        self.session.add(tell)

    def get_tells(self, name):
        """
        Returns a list of all L{Tell} objects made by user with name C{name}.
        """
        return self.session.query(Tell).filter(Tell.user.like(name)).all()

    def delete_tell(self, tell):
        """
        Remove L{Tell} object from database.
        """
        self.session.delete(tell)

    def handle_message(self, shout, command, comobj):
        """
        Called on every message. Saves last seen time for user. If someone has
        left messages for the user, these will be printed.
        """
        #self.logprint("handle_message:", shout.name)
        user = self.update_user(shout.name)
        tells = self.get_tells(user.name)
        for tell in tells:
            response = u"The user %s wanted me to tell you: %s" % (tell.teller, tell.message)
            self.send_message(response)
            self.delete_tell(tell)
        self.session.commit()

    def update_user(self, name):
        """
        Update last seen time of user, or create new user if not found.
        """
        #self.logprint("update_user:", name)
        user = self.get_user(name)
        if not user:
            user = User(None, name, '', time.time())
            self.add_user(user)
        else:
            user.last_seen = time.time()
        return user

    def tell_user(self, shout, command, comobj):
        """
        Leave message for a user.
        """
        self.update_user(shout.name)
        text = self.strip_command(shout.text, command)
        #self.logprint("tell_user:", text)
        (name, message) = self.get_name(text)
        self.logprint("name", name, "message", message)
        if not message:
            response = comobj['defaultmessage']
        elif name == shout.name:
            response = u"Only crazy people talk to themselves."
        elif name.lower() == self.nick.lower():
            response = u"I'm sorry, %s. I'm afraid I can't do that." % shout.name
        else:
            tell = Tell(name, shout.name, message, time.time())
            self.session.add(tell)
            response = u"Ok, I will tell %s that next time I see that user." % name
        self.send_message(response)
        self.session.commit()

    def seen_user(self, shout, command, comobj):
        """
        Print information on when a user was last seen in the room.
        """
        name = self.strip_command(shout.text, command)
        if not name:
            response = "Use '!seen Username' to see when a user of that name was last seen in the chat."
        else:
            user = self.get_user(name)
            #self.logprint("seen_user:", name, user)
            if not user:
                response = "I have not seen the user '%s'" % name
            else:
                last_seen = datetime.fromtimestamp(user.last_seen).strftime(self.date_format)
                response = "I last saw user '%s': %s" % (user.name, last_seen)
        self.send_message(response)
        self.update_user(shout.name)
        self.session.commit()


