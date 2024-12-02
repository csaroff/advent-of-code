from copy import copy
from math import prod

def is_cmap_possible(cmap):
    if cmap.get("red", 0) > 12:
        return False
    if cmap.get("green", 0) > 13:
        return False
    if cmap.get("blue", 0) > 14:
        return False
    return True

def draw_to_cmap(draw):
    return {c.split()[1]: int(c.split()[0]) for c in draw.split(", ")}

def cmaps_to_min_cubes(cmaps):
    result = copy(cmaps[0])
    for cmap in cmaps[1:]:
        for c, v in cmap.items():
            result[c] = max(result[c], v) if c in result else v
    return result

lines = open("input.txt", "r").readlines()
games = [(int(line.split(": ")[0].split()[-1]), line.split(": ")[-1].split("; ")) for line in lines]
games = [(id, [draw_to_cmap(draw) for draw in game]) for id, game in games]

part1 = sum([id for id, cmaps in games if all(is_cmap_possible(cmap) for cmap in cmaps)])
print("Part 1:", part1)

part2 = sum([prod(v for k, v in cmaps_to_min_cubes(cmaps).items() if v > 0) for id, cmaps in games])
print("Part 2:", part2)

