from functools import reduce
from collections import Counter

import operator
def prod(iterable):
    return reduce(operator.mul, iterable, 1)

def get_updated_position(pv, seconds, map_width=101, map_height=103):
    (px, py), (vx, vy) = pv
    return (px + vx * seconds) % map_width, (py + vy * seconds) % map_height

def get_quadrant(pv, seconds, map_width=101, map_height=103):
    px, py = get_updated_position(pv, seconds, map_width=map_width, map_height=map_height)
    if px == map_width // 2 or py == map_height // 2:
        return 0
    if px < map_width // 2 and py < map_height // 2:
        return 1
    elif px > map_width // 2 and py < map_height // 2:
        return 2
    elif px < map_width // 2 and py > map_height // 2:
        return 3
    elif px > map_width // 2 and py > map_height // 2:
        return 4
    else:
        raise ValueError("Invalid quadrant")

def get_safety_factor(pvs, seconds, map_width=101, map_height=103):
    quadrants = [get_quadrant(pv, seconds, map_width=map_width, map_height=map_height) for pv in pvs]
    return prod(Counter(q for q in quadrants if q != 0).values())

def get_map_str(pvs, map_width=101, map_height=103):
    arr = [[0 for _ in range(map_width)] for _ in range(map_height)]
    for (j, i) in pvs:
        arr[i][j] += 1

    result  = "+" + "-" * (map_width) + "+\n"
    result += "\n".join(["|" + "".join(map(str, row)) + "|" for row in arr]).replace("0", ".") + "\n"
    result += "+" + "-" * (map_width) + "+\n"
    return result

def possible_tree(positions):
    pos_set = set(positions)
    for x, y in pos_set:
        if set([(x, y+j) for j in range(10)]) <= pos_set:
            return True
    return False

def print_map(pvs, seconds, map_width=101, map_height=103):
    positions = [get_updated_position(pv, seconds, map_width=map_width, map_height=map_height) for pv in pvs]

    if possible_tree(positions):
        print("Iteration:", seconds)
        print(get_map_str(positions, map_width=map_width, map_height=map_height))

lines = open("test.txt").read().strip().split("\n"); map_width = 11; map_height = 7
lines = open("input.txt").read().strip().split("\n"); map_width = 101; map_height = 103

pvs = [[list(map(int, pv[2:].split(","))) for pv in line.split(" ")] for line in lines]
part1 = get_safety_factor(pvs, 100, map_width=map_width, map_height=map_height)
print("Part 1:", part1)

print("Part 2 confirmed by visual inspection")
for i in range(10001):
    print_map(pvs, i, map_width=map_width, map_height=map_height)
