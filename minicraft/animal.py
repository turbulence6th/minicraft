from item import *
class Animal(object):
    def __init__(self, animalType):
        self.animalType = animalType
        if animalType=='chicken':
            self.health = 100
            self.meat = 1
        elif animalType=='sheep':
            self.health = 250
            self.meat = 3
    def getDamage(self, damage):
        self.health -= damage
        if self.health <= 0:
            return Item('meat', self.meat)
        return self

    def __repr__(self):
        return self.animalType + ' : ' + str(self.health)
