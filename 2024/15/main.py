from copy import deepcopy
import sys

def get_map_and_instructions(string):
    map, instructions = string.strip().split("\n\n")
    map = [list(l) for l in map.strip().split("\n")]
    instructions = list("".join(instructions.strip().split("\n")))
    return map, instructions

direction_to_delta = {"^": (-1, 0),">": (0, 1),"v": (1, 0),"<": (0, -1)}

def get_positions_to_move(map, pos, direction):
    """
    Returns a list of (from_pos, to_pos) tuples representing moves that need to happen,
    ordered from last move to first move.
    Returns empty list if movement is not possible.
    """
    pi, pj = pos
    current_obj = map[pi][pj]

    if current_obj == "]": current_positions = [(pi, pj-1), (pi, pj)]
    elif current_obj == "[": current_positions = [(pi, pj), (pi, pj+1)]
    else: current_positions = [(pi, pj)]
    del current_obj, pi, pj

    di, dj = direction_to_delta[direction]
    next_positions = [(pi + di, pj + dj) for pi, pj in current_positions if (pi + di, pj + dj) not in current_positions]
    next_objs = [map[ni][nj] for ni, nj in next_positions]
    current_objs = [map[pi][pj] for pi, pj in current_positions]

    if "#" in next_objs:
        return []
    if all("." == obj for obj in next_objs):
        return current_positions
    moves = [get_positions_to_move(map, (ni, nj), direction) for ni, nj in next_positions if map[ni][nj] != "."]
    if not all(moves):
        return []
    return [m for move in moves for m in move] + current_positions

def dir_sort_key(direction):
    di, dj = direction_to_delta[direction]
    if di: return lambda p: (-p[0] * di, p[1])
    return lambda p: (-p[1] * dj, p[0])

def push_one_step(map, current_pos, direction):
    """
    Push the object at current_pos one step in the given direction.
    Returns the new position of the object, or the original position if the object cannot be pushed.
    """
    positions = get_positions_to_move(map, current_pos, direction)
    # positions = list(sorted(positions, key=lambda p: (p[0], p[1]) if direction in ["^", "v"] else (p[1], p[0])))
    positions = list(sorted(set(positions), key=dir_sort_key(direction)))
    if not positions:
        return current_pos

    # Apply all moves in order (last to first)
    di, dj = direction_to_delta[direction]
    # print("positions", positions)
    for pi, pj in positions:
        ni, nj = pi + di, pj + dj
        map[ni][nj] = map[pi][pj]
        map[pi][pj] = "."

    # Return the new position of the pushed object
    ci, cj = current_pos
    return ci + di, cj + dj

def print_map(map):
    print("\n".join("".join(row) for row in map))

def advance_map(map, instructions, log_progress=False):
    map = deepcopy(map)
    start_pos = [(i, j) for i in range(len(map)) for j in range(len(map[i])) if map[i][j] == "@"][0]
    if log_progress:
        print("Initial state:")
        print_map(map)

    for i, instruction in enumerate(instructions):
        # log_progress = log_progress and i < 10
        if log_progress:
            print(f"\nMove {i}: {instruction}:")
        start_pos = push_one_step(map, start_pos, instruction)
        if log_progress:
            print_map(map)
    return map

def scale_up_map(original_map):
    tile_to_tiles = {"#": ["#", "#"], "O": ["[", "]"], ".": [".", "."], "@": ["@", "."]}
    return [[t for og_tile in row for t in tile_to_tiles[og_tile]] for row in original_map]

def get_gps_sum(map):
    return sum(100*i + j for i in range(len(map)) for j in range(len(map[i])) if map[i][j] in ("O", "["))

def part1(string, log_progress=False):
    map, instructions = get_map_and_instructions(string)
    final_map = advance_map(deepcopy(map), instructions, log_progress=log_progress)
    return get_gps_sum(final_map)

def part2(string, log_progress=False):
    map, instructions = get_map_and_instructions(string)
    final_map = advance_map(scale_up_map(deepcopy(map)), instructions, log_progress=log_progress)
    return get_gps_sum(final_map)


assert part1(open("part1_small_test.txt").read()) == 2028
assert part1(open("medium_test.txt").read()) == 10092
assert part1(open("input.txt").read()) == 1552879
assert part2(open("part2_small_test.txt").read()) == 618
assert part2(open("medium_test.txt").read()) == 9021

print("Part 1:", part1(open("input.txt").read()))
print("Part 2:", part2(open("input.txt").read(), log_progress=False))
