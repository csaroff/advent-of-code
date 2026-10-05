import numpy as np
from copy import deepcopy
from math import lcm

cave_width = 7

def chars_to_nums(str_lists):
    return [[1 if c == '#' else 0 for c in row] for row in str_lists]


def nums_to_chars(int_lists):
    return [''.join(['#' if c == 1 else '.' for c in row]) for row in int_lists]

jet_to_idx = {
    '>': 1,
    '<': -1,
}

def can_move(cave, rock, x, y):
    rock_width = len(rock[0])
    rock_height = len(rock)
    if y + rock_height > len(cave) or x < 0 or x + rock_width > len(cave[0]):
        return False
    for i, row in enumerate(reversed(cave[-y-rock_height:-y])):
        for j, cell in enumerate(row[x:x+rock_width]):
            if cell and rock[i][j]:
                return False
    return True


def get_cave_view(cave, rock, x, depth):
    cave = deepcopy(cave)
    for i, row in enumerate(rock):
        for j, cell in enumerate(row):
            cave[depth + i][x + j] = cell

    return cave

# @profile
def simulate_falling_rocks(jet_pattern, n):
    rocks = [
        ["####"],
        [".#.", "###", ".#."],
        ["..#", "..#", "###"],
        ["#", "#", "#", "#"],
        ["##", "##"]
    ]

    rocks = [chars_to_nums(rock) for rock in rocks]
    cave = []
    jet_index = 0
    skipped_cave_size = 0
    lowest_points = np.array([0] * cave_width)

    rock_index = 0
    while rock_index < n:
        if jet_index == 0:
            print(f"Rock index: {rock_index}", f"Jet Index: {jet_index}")
        if rock_index != 0 and rock_index % len(rocks) == 0 and jet_index == 0:
            print(f"Discovered repeat pattern at rock index {rock_index}")

            repeat_length = rock_index + 1
            repeats_remaining = n // repeat_length
            rock_index += (repeats_remaining - 1) * repeat_length
            skipped_cave_size = repeats_remaining * len(cave)

        rock = rocks[rock_index % len(rocks)]
        rock_width = len(rock[0])
        x = 2
        for i in range(3):
            dx = jet_to_idx[jet_pattern[jet_index]]
            x  = max(0, min(x + dx, cave_width - rock_width))
            jet_index = (jet_index + 1) % len(jet_pattern)

        cave_top = [[0] * cave_width for _ in range(len(rock))]
        cave = cave_top + cave
        cave.extend(cave_top)
        depth = 0
        while True:
            dx = jet_to_idx[jet_pattern[jet_index]]
            if can_move(cave, rock, x+dx, depth):
                x += dx

            if can_move(cave, rock, x, depth+1):
                depth += 1
            else:
                jet_index = (jet_index + 1) % len(jet_pattern)
                break

            jet_index = (jet_index + 1) % len(jet_pattern)

        for i, row in enumerate(rock):
            for j, cell in enumerate(row):
                cave[-depth - i - 1][x + j] = cell

        print('len(rock):', len(rock), 'depth:', depth)
        add_cave_len = min(len(rock), depth)
        del cave[len(cave)-min(len(rock), depth):]
        rock_index += 1

    # print("\n".join(nums_to_chars(reversed(cave))))

    return len(cave) + skipped_cave_size


jet_pattern = open("input.txt").read().strip()
n = 100000  # Change this value to the number of rocks you want to simulate
height = simulate_falling_rocks(jet_pattern, n)
print("The height of the rock tower after {} rocks have fallen is: {}".format(n, height))
# print("\n".join(cave))

1,000,000,000,000
