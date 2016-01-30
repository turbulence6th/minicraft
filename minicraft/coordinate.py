class Coordinate(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def incX(self):
        return Coordinate(self.x+1, self.y)
    def decX(self):
        return Coordinate(self.x-1, self.y)
    def incY(self):
        return Coordinate(self.x, self.y+1)
    def decY(self):
        return Coordinate(self.x, self.y-1)
    def __eq__(self, other):
        if type(other)==Coordinate and self.x == other.x and self.y == other.y:
            return True
        return False
    def __repr__(self):
        return str(self.x) + ' : ' + str(self.y)