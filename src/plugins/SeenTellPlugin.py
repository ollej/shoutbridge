# -*- coding: utf-8 -*-

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Sequence, create_engine
from sqlalchemy.orm import mapper, sessionmaker
import time

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
            command = [''],
            handler = 'handle_message',
            onevents = ['Message'],
        ),
        dict(
            command = ['!tell'],
            handler = 'tell_user',
            onevents = ['Message'],
        ),
        dict(
            command = ['!seen'],
            handler = 'seen_user',
            onevents = ['Message'],
        )
    ]

    def setup(self):
        self.engine = create_engine('sqlite:///extras/halibot.db', echo=True)
        self.create_tables()
        self.create_session()

    def create_session(self):
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create_tables(self):
        """
        users_table = Table('users', self.metadata,
            Column('id', Integer, Sequence('user_id_seq'), primary_key=True),
            Column('name', String(50)),
            Column('jid', String(50)),
            Column('last_seen', Integer),
        )
        mapper(User, users_table)
        """
        self.metadata = MetaData()
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
        self.session.add(user)

    def get_user(self, name):
        return self.session.query(User).filter_by(name=name).first() 

    def add_tell(self, tell):
        self.session.add(tell)

    def get_tells(self, name):
        return self.session.query(Tell).filter_by(user=name).all()

    def delete_tell(self, tell):
        self.session.delete(tell)

    def handle_message(self, shout, command, comobj):
        #user = self.update_user(shout.name)
        #tells = self.get_tells(user.name)
        tells = self.get_tells(shout.name)
        for tell in tells:
            response = "The user %s wanted me to tell you: %s" % (tell.teller, tell.message)
            self.send_message(response)
            self.delete_tell(tell)

    def update_user(self, name):
        user = self.get_user(name)
        if not user:
            user = User(0, name, '', time.time())
            self.add_user(user)
        else:
            user.last_seen = time.time()
        return user

    def tell_user(self, shout, command, comobj):
        text = self.strip_command(shout.text, command)
        try:
            (name, message) = text.split(' ', 1)
        except ValueError:
            response = "Use '!tell Username Message' to tell a user something when they next join the chat."
        else:
            tell = Tell(name, message, time.time())
            self.session.add(tell)
            response = "Ok, I will tell user '%s' that next time I see him." % name
        self.send_message(response)

    def seen_user(self, shout, command, comobj):
        name = self.strip_command(shout.text, command)
        user = self.get_user(name)
        if not user:
            response = "I have not seen the user '%s'" % name
        else:
            response = "I last saw user '%s': %s" % (user.name, d.strftime(self.date_format))
        self.send_message(response)


