from map import *

map = Map(300,300)

for i in range(300):
    map.addSquareRandomObject(Item('stone'), 3, 10)
for i in range(300):
    map.addSquareRandomObject(Item('iron'), 3, 10)
for i in range(300):
    map.addSquareRandomObject(Item('wood'), 3, 10)
for i in range(300):
    map.addSquareRandomObject(Item('dirt'), 3, 10)
for i in range(100):
    map.addSquareRandomObject(Item('gold'), 3, 10)
for i in range(800):
    map.addObjectRandom(Animal('chicken'))
for i in range(800):
    map.addObjectRandom(Animal('sheep'))