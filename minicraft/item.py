from termcolor import colored
class Item(object):
    def __init__(self, itemType, count=1):
        self.itemType = itemType
        self.count = count
        self.handable = False

        if itemType=='sword':
            self.handable = True
            self.attack = 30

        elif itemType=='axe':
            self.handable = True
            self.attack = 10

    def __add__(self, addition):
        return Item(self.itemType, self.count+addition)
    def __sub__(self, subtract):
        if self.count-subtract<=0:
            return None
        return Item(self.itemType, self.count-subtract)
    def __repr__(self):
        return self.itemType + ' * ' + str(self.count)
    def __eq__(self, other):
        if type(other)==Item and other.itemType==self.itemType:
            return True
        return False
    def __ge__(self, other):
        if type(other)==Item and other.itemType==self.itemType and self.count>=other.count:
            return True
        return False