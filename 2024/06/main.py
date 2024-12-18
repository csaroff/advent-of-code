import numpy as np

def get_next_idx(marker, i, j):
    if marker == "^":
        return i - 1, j
    elif marker == ">":
        return i, j + 1
    elif marker == "v":
        return i + 1, j
    elif marker == "<":
        return i, j - 1
    else:
        raise ValueError(f"marker must be one of '^', '>', 'v', '<', not {marker}")

def turn_right(marker):
    if marker == "^":
        return ">"
    if marker == ">":
        return "v"
    if marker == "v":
        return "<"
    if marker == "<":
        return "^"
    raise ValueError(f"marker must be one of '^', '>', 'v', '<', not {marker}")

def update(char_arr, i, j):
    marker = char_arr[i,j]
    k, l = get_next_idx(marker, i, j)
    char_arr[i, j] = "|" if marker in ["^", "v"] else "-"
    if k < 0 or k >= len(char_arr) or l < 0 or l >= len(char_arr[0]):
        return (-1, -1)

    if char_arr[k, l] == "#":
        char_arr[i, j] = "+"
        marker = turn_right(marker)
        k, l = get_next_idx(marker, i, j)
    char_arr[k, l] = marker
    return k, l

def simulate_guard(char_arr):
    char_arr = np.copy(char_arr)

    i, j = np.argwhere(np.isin(char_arr, ['^', '<', '>', 'v']))[0]

    while i >= 0:
        i, j = update(char_arr, i, j)

    return char_arr

def is_constructable_loop(char_arr, starting_pos, obstruction_pos):
    if starting_pos == obstruction_pos:
        return False
    visited = set()
    char_arr = np.copy(char_arr)
    try:
        char_arr[obstruction_pos] = "#"
        i, j = starting_pos

        while i >= 0:
            marker = char_arr[i, j]
            if (i, j, marker) in visited:
                return True
            visited.add((i, j, marker))
            i, j = update(char_arr, i, j)

        return False
    except ValueError as e:
        print(f"marker: {char_arr[i,j]}, i: {i}, j: {j}")
        print(char_arr)
        raise e

def part1(text):
    lines = text.strip().split("\n")
    char_arr = np.array([list(line) for line in lines])
    simulated_map = simulate_guard(char_arr)

    return np.sum(np.isin(simulated_map, ["-", "|", "+"]))

def part2(text):
    lines = text.strip().split("\n")
    char_arr = np.array([list(line) for line in lines])
    simulated_map = simulate_guard(char_arr)
    potential_blockages = np.argwhere(np.isin(simulated_map, ['-', '|', '+']))

    starting_pos = tuple(np.argwhere(np.isin(char_arr, ['^', '<', '>', 'v']))[0].tolist())

    possible_loop_positions = set()
    for i, j in potential_blockages.tolist():
        if is_constructable_loop(char_arr, starting_pos, (i, j)):
            possible_loop_positions.add((i, j))

    return len(possible_loop_positions)

text = open("test.txt").read()
text = open("input.txt").read()

print("Part 1:", part1(text))
print("Part 2:", part2(text))
