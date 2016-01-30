from map import *

map = Map(1000,1000)

for i in range(3000):
    map.addSquareRandomObject(Item('stone'), 3, 10)
for i in range(3000):
    map.addSquareRandomObject(Item('iron'), 3, 10)
for i in range(3000):
    map.addSquareRandomObject(Item('wood'), 3, 10)
for i in range(3000):
    map.addSquareRandomObject(Item('dirt'), 3, 10)
for i in range(1000):
    map.addSquareRandomObject(Item('gold'), 3, 10)
for i in range(8000):
    map.addObjectRandom(Animal('chicken'))
for i in range(8000):
    map.addObjectRandom(Animal('sheep'))