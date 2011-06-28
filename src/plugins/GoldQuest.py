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

import random

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
        pass

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
        luck = random.randint(1, 100)
        if luck > 50:
            found_gold = random.randint(1, self.level)
            self.gold = self.gold + found_gold
            return found_gold
        return 0

    def fight_monster(self):
        monster_health = self.roll(self.level)
        monster_strength = self.roll(self.level)
        print("Monster:", monster_health, monster_strength)
        while monster_health >= 0 and self.hurt <= self.health:
            hit = self.roll(self.strength)
            monster_health = monster_health - hit
            print("Hit:", hit, "Monster Health:", monster_health)
            if monster_health > 0:
                monster_hit = self.roll(monster_strength)
                self.hurt = self.hurt + monster_hit
                print("Monster Hits:", monster_hit, "Hero Hurt:", self.hurt)
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

    def go_deeper(self):
        self.level = self.level + 1
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

    def write(self):
        if self.alive:
            status = "(Alive)"
        else:
            status = "(Deceased)"
        print "Name:", self.name, status
        print "Strength:", self.strength
        print "Health:", self.health
        print "Hurt:", self.hurt
        print "Kills:", self.kills
        print "Gold:", self.gold
        

    
