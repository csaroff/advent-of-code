import sys
from collections import defaultdict
import itertools
from copy import deepcopy

def get_antenna_locations(roof):
    antenna_locations = defaultdict(list)
    for i, row in enumerate(roof):
        for j, symbol in enumerate(row):
            if symbol != ".":
                antenna_locations[symbol].append((i, j))
    return antenna_locations

# arange is the range of the antennas.
# In part 1, they have a range of exactly 1
# In part 2, they have a range from 0 -> the edge of the map
def get_antinode_locations(roof, antenna1, antenna2, arange=range(1, 2)):
    i1, j1 = antenna1
    i2, j2 = antenna2
    antinode_locations = []
    for distance in arange:
        l1 = i1 - distance * (i2 - i1), j1 - distance * (j2 - j1)
        l2 = i2 - distance * (i1 - i2), j2 - distance * (j1 - j2)
        if is_valid_location(roof, l1): antinode_locations.append(l1)
        if is_valid_location(roof, l2): antinode_locations.append(l2)
        if not is_valid_location(roof, l1) and not is_valid_location(roof, l2):
            break
    return antinode_locations

def get_all_antinode_locations(roof, arange=range(1, 2)):
    antenna_locations = get_antenna_locations(roof)
    antinode_locations = []
    for antenna, locations in antenna_locations.items():
        for a1, a2 in itertools.combinations(locations, 2):
            antinode_locations.extend([l for l in get_antinode_locations(roof, a1, a2, arange=arange) if is_valid_location(roof, l)])
    return set(antinode_locations)


def is_valid_location(roof, location):
    i, j = location
    return i >= 0 and i < len(roof) and j >= 0 and j < len(roof[0])

def get_roof_with_antinodes(roof):
    new_roof = deepcopy(roof)
    for i, j in get_all_antinode_locations(roof):
        new_roof[i][j] = "#"
    return new_roof

roof = [list(line.strip()) for line in open("test.txt").readlines()]
roof = [list(line.strip()) for line in open("input.txt").readlines()]

part1 = len(get_all_antinode_locations(roof, arange=range(1, 2)))
print("Part 1", part1)

part2 = len(get_all_antinode_locations(roof, arange=range(0, sys.maxsize)))
print("Part 2", part2)
print("\n".join("".join(row) for row in get_roof_with_antinodes(roof)))
