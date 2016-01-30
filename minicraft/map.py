from coordinate import *
from animal import *
from random import randint
from user import *
from threading import *

class Map(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.arr = [[None for x in range(width)] for x in range(height)]
        self.lockArray = [[True for x in range(width)] for x in range(height)]
        self.lock = Lock()
        self.lockCondition = Condition(self.lock)

    def releaselock(self, coord, coord2):
        self.lock.acquire()
        self.lockArray[coord.y][coord.x] = True
        self.lockArray[coord2.y][coord2.x] = True
        self.lockCondition.notifyAll()
        self.lock.release()


    def acquirelock(self, coord, coord2):
        self.lock.acquire()
        while True:
            if  (self.lockArray[coord.y][coord.x] and self.lockArray[coord2.y][coord2.x]):
                self.lockArray[coord.y][coord.x] = False
                self.lockArray[coord2.y][coord2.x] = False
                self.lockCondition.release()
                return
            else:
                self.lockCondition.wait()


    def addObject(self, coordinate, object):
        if coordinate.y<self.height and coordinate.x<self.width:
            if not self.getObject(coordinate):
                if object:
                    object.coordinate = coordinate
                self.arr[coordinate.y][coordinate.x] = object
    def deleteObject(self, object):
        coordinate = self.findCoordinate(object)
        if coordinate!=None:
            self.arr[coordinate.y][coordinate.x] = None
    def moveObject(self, object, direction):
        coordinate = object.coordinate

        if direction=='up' and coordinate.y!=0 and not self.getObject(coordinate.decY()):
            self.acquirelock(coordinate, coordinate.decY())
            self.deleteObject(object)
            if type(object)==User:
                self.addObject(coordinate.decY(), object.getDamage(1))
            else:
                self.addObject(coordinate.decY(), object)
            self.releaselock(coordinate, coordinate.decY())


        elif direction=='down' and coordinate.y!=self.height-1 and not self.getObject(coordinate.incY()):
            self.acquirelock(coordinate, coordinate.incY())
            self.deleteObject(object)
            if type(object)==User:
                self.addObject(coordinate.incY(), object.getDamage(1))
            else:
                self.addObject(coordinate.incY(), object)
            self.releaselock(coordinate, coordinate.incY())

        elif direction=='left' and coordinate.x!=0 and not self.getObject(coordinate.decX()):
            self.acquirelock(coordinate, coordinate.decX())
            self.deleteObject(object)
            if type(object)==User:
                self.addObject(coordinate.decX(), object.getDamage(1))
            else:
                self.addObject(coordinate.decX(), object)
            self.releaselock(coordinate, coordinate.decX())

        elif direction=='right' and coordinate.x!=self.width-1 and not self.getObject(coordinate.incX()):
            self.acquirelock(coordinate, coordinate.incX())
            self.deleteObject(object)
            if type(object)==User:
                self.addObject(coordinate.incX(), object.getDamage(1))
            else:
                self.addObject(coordinate.incX(), object)
            self.releaselock(coordinate, coordinate.incX())

    def getObject(self, coordinate):
        if coordinate.x >= self.width or coordinate.y >= self.height:
            return None
        return self.arr[coordinate.y][coordinate.x]
    def findCoordinate(self, object):
        if hasattr(object, 'coordinate'):
            return object.coordinate
        else:
            for i in range(len(self.arr)):
                for j in range(len(self.arr[i])):
                    if self.arr[i][j] == object:
                        return Coordinate(j, i)
        return None
    def deleteCoordinate(self, coordinate):
        self.arr[coordinate.y][coordinate.x] = None
    def addObjectRandom(self, object):
        x = randint(0, self.width-1)
        y = randint(0, self.height-1)
        while self.getObject(Coordinate(x, y)):
            x = randint(0, self.width-1)
            y = randint(0, self.height-1)
        self.addObject(Coordinate(x, y), object)
    def acquireObject(self, user, direction):
        coordinate = self.findCoordinate(user)
        if direction=='up' and coordinate.y!=0 and type(self.getObject(coordinate.decY()))==Item:
            self.acquirelock(coordinate, coordinate.decY())
            object = self.getObject(coordinate.decY())
            user.getItem(Item(object.itemType))
            self.addObjectForce(coordinate.decY(), object-1)
            self.releaselock(coordinate, coordinate.decY())
        elif direction=='down' and coordinate.y!=self.height-1 and type(self.getObject(coordinate.incY()))==Item:
            self.acquirelock(coordinate, coordinate.incY())
            object = self.getObject(coordinate.incY())
            user.getItem(Item(object.itemType))
            self.addObjectForce(coordinate.incY(), object-1)
            self.releaselock(coordinate, coordinate.incY())
        elif direction=='left' and coordinate.x!=0 and type(self.getObject(coordinate.decX()))==Item:
            self.acquirelock(coordinate, coordinate.decX())
            object = self.getObject(coordinate.decX())
            user.getItem(Item(object.itemType))
            self.addObjectForce(coordinate.decX(), object-1)
            self.releaselock(coordinate, coordinate.decX())
        elif direction=='right' and coordinate.x!=self.width-1 and type(self.getObject(coordinate.incX()))==Item:
            self.acquirelock(coordinate, coordinate.incX())
            object = self.getObject(coordinate.incX())
            user.getItem(Item(object.itemType))
            self.addObjectForce(coordinate.incX(), object-1)
            self.releaselock(coordinate, coordinate.incX())
    def addObjectForce(self, coordinate, object):
        self.arr[coordinate.y][coordinate.x] = object
    def putObject(self, user, direction, object):
        if user.hasItems(object):
            coordinate = self.findCoordinate(user)
            if direction=='up' and coordinate.y!=0:
                self.acquirelock(coordinate, coordinate.decY())
                object2 = self.getObject(coordinate.decY())
                if object2==None:
                    self.addObjectForce(coordinate.decY(), Item(object.itemType))
                    user.inventory[user.inventory.index(object)] -= 1
                elif object==object2:
                    self.addObjectForce(coordinate.decY(), object2+1)
                    user.inventory[user.inventory.index(object)] -= 1
                self.releaselock(coordinate, coordinate.decY())

            elif direction=='down' and coordinate.y!=self.height-1:
                self.acquirelock(coordinate, coordinate.incY())
                object2 = self.getObject(coordinate.incY())
                if object2==None:
                    self.addObjectForce(coordinate.incY(), Item(object.itemType))
                    user.inventory[user.inventory.index(object)] -= 1
                elif object==object2:
                    self.addObjectForce(coordinate.incY(), object2+1)
                    user.inventory[user.inventory.index(object)] -= 1
                self.releaselock(coordinate, coordinate.incY())
            elif direction=='left' and coordinate.x!=0:
                self.acquirelock(coordinate, coordinate.decX())
                object2 = self.getObject(coordinate.decX())
                if object2==None:
                    self.addObjectForce(coordinate.decX(), Item(object.itemType))
                    user.inventory[user.inventory.index(object)] -= 1
                elif object==object2:
                    self.addObjectForce(coordinate.decX(), object2+1)
                    user.inventory[user.inventory.index(object)] -= 1
                self.releaselock(coordinate, coordinate.decX())
            elif direction=='right' and coordinate.x!=self.width-1:
                self.acquirelock(coordinate, coordinate.incX())
                object2 = self.getObject(coordinate.incX())
                if object2==None:
                    self.addObjectForce(coordinate.incX(), Item(object.itemType))
                    user.inventory[user.inventory.index(object)] -= 1
                elif object==object2:
                    self.addObjectForce(coordinate.incX(), object2+1)
                    user.inventory[user.inventory.index(object)] -= 1
                self.releaselock(coordinate, coordinate.incX())
            if None in user.inventory:
                user.inventory.remove(None)
    def damage(self, user, direction):
        coordinate = self.findCoordinate(user)
        bonus = 0
        if user.handle:
            bonus = user.handle.attack
        if direction=='up' and coordinate.y!=0 and (type(self.getObject(coordinate.decY()))==Animal or type(self.getObject(coordinate.decY()))==User):
            self.acquirelock(coordinate, coordinate.decY())
            live = self.getObject(coordinate.decY())
            self.addObjectForce(coordinate.decY(), live.getDamage(randint(30,50) + bonus))
            self.releaselock(coordinate, coordinate.decY())
        elif direction=='down' and coordinate.y!=self.height-1 and (type(self.getObject(coordinate.incY()))==Animal or type(self.getObject(coordinate.incY()))==User):
            self.acquirelock(coordinate, coordinate.incY())
            live = self.getObject(coordinate.incY())
            self.addObjectForce(coordinate.incY(), live.getDamage(randint(30,50) + bonus))
            self.releaselock(coordinate, coordinate.incY())
        elif direction=='left' and coordinate.x!=0 and (type(self.getObject(coordinate.decX()))==Animal or type(self.getObject(coordinate.decX()))==User):
            self.acquirelock(coordinate, coordinate.decX())
            live = self.getObject(coordinate.decX())
            self.addObjectForce(coordinate.decX(), live.getDamage(randint(30,50) + bonus))
            self.releaselock(coordinate, coordinate.decX())
        elif direction=='right' and coordinate.x!=self.width-1 and (type(self.getObject(coordinate.incX()))==Animal or type(self.getObject(coordinate.incX()))==User):
            self.acquirelock(coordinate, coordinate.incX())
            live = self.getObject(coordinate.incX())
            self.addObjectForce(coordinate.incX(), live.getDamage(randint(30,50) + bonus))
            self.releaselock(coordinate, coordinate.incX())
    def addSquareRandomObject(self, object, size, maxCount):
        startX = randint(0, self.width-1)
        startY = randint(0, self.height-1)

        for i in range(size):
            for j in range(size):
                self.addObject(Coordinate(startX+i, startY+j), Item(object.itemType, randint(1, maxCount)))


    def __repr__(self):
        ret = ''
        for i in self.arr:
            ret += str(i) + '\n'
        return ret

    def printAs(self, user):
        coordinate = self.findCoordinate(user)
        leftTop = Coordinate(coordinate.x-5, coordinate.y-5)
        rightBot = Coordinate(coordinate.x+5, coordinate.y+5)

        if leftTop.x < 0 :
            leftTop.x = 0
        if leftTop.y < 0:
            leftTop.y = 0

        if rightBot.x >= self.width:
            rightBot.x = self.width-1
        if rightBot.y >= self.height:
            rightBot.y = self.height-1

        for j in range(leftTop.y, rightBot.y+1):
            for i in range(leftTop.x, rightBot.x+1):
                print self.arr[j][i],
            print

    def map(self, user):
        coordinate = self.findCoordinate(user)
        leftTop = Coordinate(coordinate.x-5, coordinate.y-4)
        rightBot = Coordinate(coordinate.x+4, coordinate.y+5)

        if leftTop.x < 0 :
            leftTop.x = 0
        if leftTop.y < 0:
            leftTop.y = 0

        if rightBot.x >= self.width:
            rightBot.x = self.width-1
        if rightBot.y >= self.height:
            rightBot.y = self.height-1

        ret = []

        for j in range(leftTop.y, rightBot.y+1):
            temp = []
            for i in range(leftTop.x, rightBot.x+1):
                x = self.arr[j][i]
                if type(x) == User:
                    temp.append({'username': x.username, 'health': x.health})
                elif type(x) == Item:
                    temp.append({'itemType': x.itemType, 'count': x.count})
                elif type(x) == Animal:
                    temp.append({'animalType': x.animalType, 'health': x.health})
                else:
                    temp.append(None)
            ret.append(temp)
        return ret



