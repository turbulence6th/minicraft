from item import *
from random import choice
import ConfigParser
import os
class User(object):
    userList = []
    def __init__(self, username, password):
        self.username = username
        self.inventory = []
        self.handle = None
        self.active = True
        self.health = 1000
        self.password = password
    def showItems(self):
        return self.inventory
    def useItem(self, item):
        if item.handable and self.hasItems(item):
            if self.handle:
                self.getItem(self.handle)
            self.handle = item
            self.inventory[self.inventory.index(item)] -= 1
            if None in self.inventory:
                self.inventory.remove(None)
    def setActive(self, active):
        self.active = active
    def getItem(self, item):
        if item in self.inventory:
            self.inventory[self.inventory.index(item)] += 1
        else:
            self.inventory.append(item)
    def eat(self):
        if Item('meat') in self.inventory:
            self.inventory[self.inventory.index(Item('meat'))] -= 1
            self.health += 50
            if self.health>1000:
                self.health = 1000
            if None in self.inventory:
                self.inventory.remove(None)
    def merge(self, target):
        Config = ConfigParser.ConfigParser()
        PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
        Config.read(os.path.join(PROJECT_PATH, '../minicraft/config_merge'))
        def ConfigSectionMap(section):
            dict1 = {}
            options = Config.options(section)
            for option in options:
                try:
                    dict1[option] = Config.get(section, option)
                    if dict1[option] == -1:
                        pass
                except:
                    print("exception on %s!" % option)
                    dict1[option] = None
            return dict1

        ingr = ConfigSectionMap(target)
        has = True
        for i in ingr:
            if not self.hasItems(Item(i, int(ingr[i]))):
                has = False

        if has:
            for i in ingr:
                self.inventory[self.inventory.index(Item(i))] -= int(ingr[i])
            self.getItem(Item(target))

        self.inventory = [x for x in self.inventory if x != None]
    def hasItems(self, item):
        for i in self.inventory:
            if i>=item:
                return True
        return False
    def getDamage(self, damage):
        self.health -= damage
        if self.health <= 0:
            User.userList.remove(self)
            if self.inventory!=[]:
                return choice(self.inventory)
            return None
        return self

    def __repr__(self):
        return self.username + ' : ' + str(self.health)
    def __eq__(self, other):
        if type(other)==User and self.username == other.username and self.password == other.password:
            return True
        return False

