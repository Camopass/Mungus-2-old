import math


def map_range(val, from_min, from_max, to_min, to_max):
    fromRange = from_max - from_min
    toRange = to_max - to_min
    sc = toRange/fromRange
    co = -1 * from_min * sc + to_min
    return val * sc+co
