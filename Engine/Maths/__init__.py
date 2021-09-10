import math


class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if type(other == Vec2):
            return Vec2(self.x + other.x, self.y + other.y)
        else:
            return Vec2(self.x + other, self.y + other)

    def __sub__(self, other):
        if type(other == Vec2):
            return Vec2(self.x - other.x, self.y - other.y)
        else:
            return Vec2(self.x - other, self.y - other)

    def __mul__(self, other):
        if type(other == Vec2):
            return Vec2(self.x * other.x, self.y * other.y)
        else:
            return Vec2(self.x * other, self.y * other)

    def __div__(self, other):
        if type(other == Vec2):
            return Vec2(self.x / other.x, self.y / other.y)
        else:
            return Vec2(self.x / other, self.y / other)

    def __pow__(self, other):
        if type(other == Vec2):
            return Vec2(self.x ** other.x, self.y ** other.y)
        else:
            return Vec2(self.x ** other, self.y ** other)

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    def __radd__(self, other):
        return Vec2(self.x + other, self.y + other)

    def __rdiv__(self, other):
        return Vec2(other/self.x, other/self.y)

    def __rmul__(self, other):
        return Vec2(other * self.x, other * self.y)

    def __rsub__(self, other):
        return Vec2(other - self.x, other - self.y)

    @classmethod
    def from_tuple(cls, tp):
        return cls(*tp)

    def to_tuple(self):
        return tuple((self.x, self.y))


def map_range(val, from_min, from_max, to_min, to_max):
    fromRange = from_max - from_min
    toRange = to_max - to_min
    sc = toRange/fromRange
    co = -1 * from_min * sc + to_min
    return val * sc+co


def pythagoras(a, b):
    return (a ** 2 + b ** 2) ** 0.5


def dist(a: Vec2, b: Vec2):
    return pythagoras(a, b)
