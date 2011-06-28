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

from sqlalchemy import Table, Column, Integer, Boolean, String, MetaData, ForeignKey, Sequence, create_engine
from sqlalchemy.orm import mapper, sessionmaker
import random

from GoldQuest import *
from plugins.Plugin import *

class QuestPlugin(Plugin):
    name = "QuestPlugin"
    author = "Olle Johansson"
    description = "A simple multi user quest game."
    commands = [
        dict(
            command = ['!quest'],
            handler = 'quest',
            onevents = ['Message'],
        )
    ]
    hero = None

    def setup(self):
        """
        Setup Sqlite SQL tables and start a db session.

        The database will be saved in C{extras/goldquest.db}

        Calls L{setup_tables} to setup table metadata and L{setup_session}
        to instantiate the db session.
        """
        try:
            debug = self.bridge.cfg.get_bool('debug')
        except AttributeError:
            debug = False
        self.engine = create_engine('sqlite:///extras/quest.db', echo=debug)
        self.setup_tables()
        self.setup_session()
        self.hero = self.get_alive_hero()

    def setup_session(self):
        """
        Start a SQLAlchemy db session.

        Saves the session instance in C{self.session}
        """
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def setup_tables(self):
        """
        Defines the tables to use for L{Hero}
        The Metadata instance is saved to C{self.metadata}
        """
        self.metadata = MetaData()
        hero_table = Table('hero', self.metadata,
            Column('id', Integer, Sequence('hero_id_seq'), primary_key=True),
            Column('name', String(100)),
            Column('health', Integer),
            Column('strength', Integer),
            Column('hurt', Integer),
            Column('kills', Integer),
            Column('gold', Integer),
            Column('level', Integer),
            Column('alive', Boolean),
        )
        mapper(Hero, hero_table)
        self.metadata.create_all(self.engine)

    def quest(self, shout, command, comobj):
        text = self.strip_command(shout.text, command)
        if text in ['reroll', 'ny gubbe']:
            return self.reroll()
        if not self.hero or not self.hero.alive:
            msg = u"Your village doesn't have a champion! Use !quest reroll"
            return self.send_message(msg)
        if text in ['rest', 'vila']:
            msg = self.rest()
        elif text in ['fight', u'slåss']:
            msg = self.fight()
        elif text in ['deeper', 'vidare']:
            msg = self.go_deeper()
        elif text in ['loot', 'search', u'sök', 'finna dolda ting']:
            msg = self.search_treasure()
        elif text in ['charsheet', 'formulär']:
            msg = self.show_charsheet()
        self.save_hero()
        return self.send_message(msg)

    def save_hero(self):
        self.session.add(self.hero)
        self.session.commit()

    def get_alive_hero(self):
        hero = self.session.query(Hero).filter_by(alive=True).first()
        #hero = self.session.query(Hero).all()
        if hero:
            hero.write()
        return hero

    def reroll(self):
        if self.hero and self.hero.alive:
            msg = u'%s growls' % self.hero.name
            return self.send_message(msg)
        else:
            self.hero = Hero()
            self.hero.reroll()
            self.save_hero()
            msg = random.choice([
                u"There's a new hero in town: %(name)s",
                u"The valiant hero %(name) shows up to help the village.",
                u"%(name) comes forth to fight for the village.",
            ])
            msg = msg % dict(name=self.hero.name, strength=self.hero.strength, health=self.hero.health)
            return self.send_message(msg)

    def search_treasure(self):
        gold = self.hero.search_treasure()
        if gold:
            lootmsg = random.choice([
                u"%(name)s found loot: %(gold)d pieces of gold!",
                u"%(name)s opens a chest and finds %(gold)d gold coins!",
                u"%(gold)d gold nuggets are scattered on the ground, %(name)s picks them up.",
            ])
        else:
            lootmsg = "%(name)s can't find any gold."
        msg = lootmsg % dict(name=self.hero.name, gold=gold)
        return msg

    def rest(self):
        rested = self.hero.rest()
        if rested:
            if self.hero.hurt:
                restmsg = random.choice([
                    u"%(name)s rests and heals %(rested)s hurt.",
                    u"After a short rest, %(name)s heals %(rested)s points",
                ])
            else:
                restmsg = random.choice([
                    u"%(name) is fully healed.",
                    u"After some rest, %(name)s is healed.",
                ])
        else:
            restmsg = "%(name)s is already fully rested."
        msg = restmsg % dict(name=self.hero.name, rested=rested)
        return msg

    def go_deeper(self):
        level = self.hero.go_deeper()
        msg = random.choice([
            u"Your valiant hero, %(name)s, delves deeper into the dungeon.",
            u"%(name)s is now at level %(level)d of the dungeon.",
            u"With steady steps %(name)s heads down to level %(level)d.",
        ])
        msg = msg % dict(name=self.hero.name, level=level)
        return msg

    def fight(self):
        won = self.hero.fight_monster()
        if won:
            msg = random.choice([
                u"The monster is slaughtered.",
                u"%(name)s kills yet another monster.",
                u"Another one bites the dust.",
            ])
        else:
            msg = random.choice([
                u"Your hero has died.",
                u"The entire village mourns the death of %(name)s.",
                u"%(name)s dies a hero's death.",
            ])
        msg = msg % dict(name=self.hero.name)
        return msg

    def show_charsheet(self, hero=None):
        if not hero:
            hero = self.hero
        msg = "%(name)s - Strength: %(strength)d Health: %(health)d Hurt: %(hurt)d Kills: %(kills)d Gold: %(gold)d Level: %(level)d"
        msg = msg % dict(
            name = hero.name,
            strength = hero.strength,
            health = hero.health,
            hurt = hero.hurt,
            kills = hero.kills,
            gold = hero.gold,
            level = hero.level,
        )
        return msg

