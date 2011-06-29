#!/usr/bin/python
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
import cmd

from utils.Conf import *

class Hero(object):
    id = 0
    name = ''
    health = None
    strength = None
    hurt = None
    kills = None
    gold = None
    level = None
    alive = None

    def __init__(self):
        self.hurt = 0
        self.kills = 0
        self.gold = 0
        self.level = 1
        self.alive = True

    def reroll(self, name=None):
        self.health = self.roll(20, 5)
        self.strength = self.roll(20, 5)
        self.hurt = 0
        self.kills = 0
        self.gold = 0
        self.level = 1
        self.alive = True
        if name:
            self.name = name
        else:
            self.name = self.random_name()

    def search_treasure(self):
        luck = self.roll(100)
        if luck > 50:
            found_gold = self.roll(self.level)
            self.gold = self.gold + found_gold
            return found_gold
        return 0

    def injure(self, hurt):
        self.hurt = self.hurt + hurt
        if self.hurt > self.health:
            self.alive = False

    def fight_monster(self, monster):
        #print("Monster:", monster.health, monster.strength)
        while monster.health >= 0 and self.hurt < self.health:
            hit = self.roll(self.strength)
            killed = monster.injure(hit)
            #print("Hit:", hit, "Monster Health:", monster.health)
            if not killed:
                monster_hit = self.roll(monster.strength)
                self.injure(monster_hit)
                #print("Monster Hits:", monster_hit, "Hero Hurt:", self.hurt)
        if self.hurt > self.health:
            self.alive = False
        else:
            self.kills = self.kills + 1
        return self.alive

    def rest(self):
        if self.hurt > 0:
            heal = random.randint(1, 10)
            if heal > self.hurt:
                heal = self.hurt
            self.hurt = self.hurt - heal
            return heal
        return 0

    def go_deeper(self, depth=None):
        if not depth:
            depth = 1
        self.level = self.level + depth
        return self.level

    def roll(self, sides, times=1):
        total = 0
        for i in range(times):
            total = total + random.randint(1, sides)
        return total

    def random_name(self):
        name = random.choice(['Conan', 'Canon', 'Hercules', 'Robin', 'Dante', 'Legolas', 'Buffy', 'Xena'])
        epithet = random.choice(['Barbarian', 'Invincible', 'Mighty', 'Hairy', 'Bastard', 'Slayer'])
        return '%s the %s' % (name, epithet)

    def get_attributes(self):
        attribs = self.__dict__
        attribs['status'] = ""
        if not self.alive:
            attribs['status'] = " (Deceased)"
        #for k, v in attribs.items():
        #    print k, v
        return attribs
        #return self.__dict__

    def get_charsheet(self):
        msg = "%(name)s%(status)s - Strength: %(strength)d Health: %(health)d Hurt: %(hurt)d Kills: %(kills)d Gold: %(gold)d Level: %(level)d"
        msg = msg % self.get_attributes()
        return msg

class Monster(object):
    name = None
    strength = None
    health = None

    def __init__(self, level=None, name=None):
        if not level:
            level = 1
        self.strength = random.randint(1, level)
        self.health = random.randint(1, level)
        if name:
            self.name = name
        else:
            self.name = self.random_name()

    def injure(self, hurt):
        """
        Injure the monster with hurt points. Returns True if the monster died.
        """
        self.health = self.health - hurt
        if self.health <= 0:
            return True
        else:
            return False

    def random_name(self):
        return random.choice([
            "an orc", "an ogre", "a bunch of goblins", "a giant spider",
            "a cyclops", "a minotaur", "a horde of kobolds",
        ])

class Level(object):
    depth = None
    killed = None
    looted = None

    def __init__(self, depth=None):
        self.killed = 0
        self.looted = 0
        if depth:
            self.depth = depth
        else:
            self.depth = 1

    def get_monster(self):
        if self.killed < self.depth:
            return Monster(self.depth)

    def get_loot(self):
        loot = 0
        if self.can_loot():
            self.looted = self.looted + 1
            luck = random.randint(1, 100)
            if luck > 20:
                loot = random.randint(1, self.depth)
            elif luck < 5:
                loot = 0 - luck
        return loot

    def can_loot(self):
        if self.looted < self.killed:
            return True
        return False

class GoldQuest(object):
    cfg = None
    hero = None
    level = None

    def __init__(self, cfg):
        """
        Setup Sqlite SQL tables and start a db session.

        The database will be saved in C{extras/goldquest.db}

        Calls L{setup_tables} to setup table metadata and L{setup_session}
        to instantiate the db session.
        """
        self.cfg = cfg
        try:
            debug = self.cfg.get_bool('debug')
        except AttributeError:
            debug = False
        self.engine = create_engine('sqlite:///extras/quest.db', echo=debug)
        self.setup_tables()
        self.setup_session()
        self.hero = self.get_alive_hero()
        if self.hero and not self.level:
            self.level = Level(self.hero.level)

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
        level_table = Table('level', self.metadata,
            Column('id', Integer, Sequence('hero_id_seq'), primary_key=True),
            Column('depth', Integer),
            Column('killed', Integer),
            Column('looted', Integer),
        )
        mapper(Level, level_table)
        self.metadata.create_all(self.engine)

    def play(self, command):
        msg = ""
        if command in ['reroll', 'ny gubbe']:
            return self.reroll()
        if not self.hero or not self.hero.alive:
            msg = u"Your village doesn't have a champion! Use !quest reroll"
            return msg
        if command in ['rest', 'vila']:
            msg = self.rest()
        elif command in ['fight', u'slåss']:
            msg = self.fight()
        elif command in ['deeper', 'vidare']:
            msg = self.go_deeper()
        elif command in ['loot', 'search', u'sök', 'finna dolda ting']:
            msg = self.search_treasure()
        elif command in ['charsheet', u'formulär']:
            msg = self.show_charsheet()
        else:
            return None
        self.save_hero()
        return msg

    def save_hero(self):
        self.session.add(self.hero)
        self.session.commit()

    def get_alive_hero(self):
        hero = self.session.query(Hero).filter_by(alive=True).first()
        return hero

    def reroll(self):
        if self.hero and self.hero.alive:
            msg = u'%s growls' % self.hero.name
            return msg
        else:
            self.hero = Hero()
            self.hero.reroll()
            self.level = Level(self.hero.level)
            self.save_hero()
            msg = random.choice([
                "There's a new hero in town: %(name)s",
                "The valiant hero %(name)s shows up to help the village.",
                "%(name)s comes forth to fight for the village.",
            ])
            msg = msg % self.hero.get_attributes()
            return msg

    def search_treasure(self):
        #loot = self.hero.search_treasure()
        attribs = self.hero.get_attributes()
        if self.level.can_loot():
            loot = self.level.get_loot()
            attribs['loot'] = loot
            if loot > 0:
                msg = random.choice([
                    u"%(name)s found loot: %(loot)d pieces of gold!",
                    u"%(name)s opens a chest and finds %(loot)d gold coins!",
                    u"%(loot)d gold nuggets are scattered on the ground, %(name)s picks them up.",
                ])
            elif loot < 0:
                attribs['trap_hurt'] = abs(loot)
                self.hero.injure(attribs['trap_hurt'])
                msg = random.choice([
                    u"It's a trap!",
                    u"A trap hurts %(name)s for %(injure)d points.",
                    U"%(name)s drops the lid of a chest on his fingers.",
                ])
            else:
                msg = "%(name)s can't find any gold."
        else:
            msg = random.choice([
                "There are no corpses to loot.",
                "You have to kill more monsters on this level to loot.",
            ])
        msg = msg % attribs
        return msg

    def rest(self):
        rested = self.hero.rest()
        if rested:
            if self.hero.hurt:
                restmsg = random.choice([
                    u"%(name)s rests and heals %(rested)s hurt.",
                    u"After a short rest, %(name)s heals %(rested)s points.",
                ])
            else:
                restmsg = random.choice([
                    u"%(name)s is fully healed.",
                    u"After some rest, %(name)s is healed.",
                ])
        else:
            restmsg = "%(name)s is already fully rested."
        attribs = self.hero.get_attributes()
        attribs['rested'] = rested
        msg = restmsg % attribs
        return msg

    def go_deeper(self):
        level = self.hero.go_deeper()
        self.level = Level(self.hero.level)
        msg = random.choice([
            u"Your valiant hero, %(name)s, delves deeper into the dungeon.",
            u"%(name)s is now at level %(level)d of the dungeon.",
            u"With steady steps %(name)s heads down to level %(level)d.",
        ])
        msg = msg % self.hero.get_attributes()
        return msg

    def fight(self):
        monster = self.level.get_monster()
        attribs = self.hero.get_attributes()
        if not monster:
            msg = random.choice([
                "The hero searches high and low, but can't find any more monsters on this level.",
                "Apparently this level has been cleared of all monsters.",
            ])
            return msg % attribs
        won = self.hero.fight_monster(monster)
        if won:
            self.level.killed = self.level.killed + 1
            msg = random.choice([
                u"%(monster)s is slaughtered.",
                u"%(name)s kills yet another monster.",
                u"Another one bites the dust.",
                u"%(monster)s is slayed by %(name)s.",
                u"%(name)s %(slayed)s %(monster)s.",
            ])
            attribs['slayed'] = random.choice([
                u"narrowly defeats",
                u"easily beats",
                u"slays",
                u"kills",
            ])
        else:
            msg = random.choice([
                u"Your hero has died.",
                u"The entire village mourns the death of %(name)s.",
                u"%(name)s dies a hero's death.",
            ])
        attribs['monster'] = monster.name
        msg = msg % attribs
        msg = self.firstupper(msg)
        return msg

    def show_charsheet(self):
        return self.hero.get_charsheet()

    def firstupper(self, text):
        first = text[0].upper()
        return first + text[1:]

class Game(cmd.Cmd):
    prompt = 'GoldQuest> '
    intro = "Welcome to GoldQuest!"
    game = None

    def preloop(self):
        cfg = Conf('../config.ini', 'LOCAL')
        self.game = GoldQuest(cfg)

    def default(self, line):
        ret = self.game.play(line)
        if ret:
            print ret

    def do_fight(self, line):
        "Find a new monster and fight it to the death!"
        print self.game.play('fight')

    def do_charsheet(self, line):
        "Show the character sheet for the current hero."
        print self.game.play('charsheet')

    def do_reroll(self, line):
        "Reroll a new hero if the village doesn't have one already."
        print self.game.play('reroll')

    def do_rest(self, line):
        "Makes the hero rest for a while to regain hurt."
        print self.game.play('rest')

    def do_loot(self, line):
        "The hero will search for loot in the hope to find gold."
        print self.game.play('loot')

    def do_deeper(self, line):
        "Tells the hero to go deeper into the dungeon."
        print self.game.play('deeper')

    def do_quit(self, line):
        "Quit Game"
        print "A strange game. The only winning move is not to play."
        return True

if __name__ == '__main__':
    Game().cmdloop()


