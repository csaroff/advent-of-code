import itertools
from functools import lru_cache

numpad = [["7",  "8", "9"],
          ["4",  "5", "6"],
          ["1",  "2", "3"],
          [None, "0", "A"]]
numpad = tuple(tuple(row) for row in numpad)

dirpad = [[None, "^", "A"],
          ["<",  "v", ">"]]
dirpad = tuple(tuple(row) for row in dirpad)

dir_symbol_to_direction = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}

def is_valid_movement_sequence(pad, start_pos, movement_sequence):
    pi, pj = start_pos
    for symbol in movement_sequence:
        if symbol == "A": continue
        di, dj = dir_symbol_to_direction[symbol]
        pi, pj = (pi + di, pj + dj)
        if pad[pi][pj] is None:
            return False
    return True

@lru_cache(maxsize=None)
def get_paths(pad, start_symbol, end_symbol):
    start_pos = None
    end_pos = None
    for i, row in enumerate(pad):
        for j, cell in enumerate(row):
            if cell == start_symbol: start_pos = (i, j)
            if cell == end_symbol: end_pos = (i, j)
    if start_pos is None or end_pos is None:
        raise ValueError(f"Start symbol {start_symbol} or end symbol {end_symbol} not found in pad")

    di, dj = (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])

    movement_sequences = itertools.permutations("" + (">" * dj if dj > 0 else "<" * -dj) + ("^" * -di if di < 0 else "v" * di))
    return ["".join(movement_sequence) + "A" for movement_sequence in movement_sequences if is_valid_movement_sequence(pad, start_pos, movement_sequence)]

def pairwise(sliceable):
    return zip(sliceable, sliceable[1:])

@lru_cache(maxsize=None)
def get_shortest_path(numpad, dirpad, start_symbol, end_symbol, numpad_iterations=1, dirpad_iterations=2):
    movement_sequences = get_paths(numpad if numpad_iterations > 0 else dirpad, start_symbol, end_symbol)
    if numpad_iterations > 0:
        numpad_iterations -= 1
    else:
        dirpad_iterations -= 1

    if numpad_iterations == 0 and dirpad_iterations == 0:
        return len(min(movement_sequences, key=lambda ms: len(ms)))

    total = float("inf")
    for seq in movement_sequences:
        subtotal = sum(get_shortest_path(numpad, dirpad, s1, s2, numpad_iterations, dirpad_iterations) for s1, s2 in pairwise("A" + seq))
        total = min(total, subtotal)

    return total


def get_iterated_numpad_sequence(numpad, dirpad, numpad_sequence, numpad_iterations=1, dirpad_iterations=2, debug=False):
    return sum(get_shortest_path(numpad, dirpad, s1, s2, numpad_iterations=numpad_iterations, dirpad_iterations=dirpad_iterations) for s1, s2 in pairwise("A" + numpad_sequence))

def get_complexity(numpad, dirpad, numpad_sequence, numpad_iterations=1, dirpad_iterations=2):
    iterated_numpad_sequence_length = get_iterated_numpad_sequence(numpad, dirpad, numpad_sequence, numpad_iterations=numpad_iterations, dirpad_iterations=dirpad_iterations)
    return iterated_numpad_sequence_length * int(numpad_sequence.replace("A", ""))

def part1(codes):
    return sum(get_complexity(numpad, dirpad, code, numpad_iterations=1, dirpad_iterations=2) for code in codes)

def part2(codes):
    return sum(get_complexity(numpad, dirpad, code, numpad_iterations=1, dirpad_iterations=25) for code in codes)

print("Part 1 Test: ", part1(open("test.txt").read().strip().splitlines()))
print("Part 2 Test: ", part2(open("test.txt").read().strip().splitlines()))

print()

print("Part 1 Input:", part1(open("input.txt").read().strip().splitlines()))
print("Part 2 Input:", part2(open("input.txt").read().strip().splitlines()))

# def _dirpad_to_numpad(pad, sequence, starting_position):
#     pi, pj = starting_position
#     new_sequence = ""
#     for i, symbol in enumerate(sequence):
#         if symbol == "A":
#             new_sequence += pad[pi][pj]
#             continue
#         di, dj = dir_symbol_to_direction[symbol]
#         pi, pj = (pi + di, pj + dj)
#         if pad[pi][pj] is None:
#             raise ValueError(f"Invalid sequence {sequence[:i+1]} for pad {pad}")
#     return new_sequence

# def dirpad_to_numpad(numpad, dirpad, sequence, numpad_iterations=1, dirpad_iterations=2):
#     for _ in range(dirpad_iterations):
#         sequence = _dirpad_to_numpad(dirpad, sequence, starting_position=(0, 2))

#     for _ in range(numpad_iterations):
#         sequence = _dirpad_to_numpad(numpad, sequence, starting_position=(3, 2))
#     return sequence

# def validate_code(code, numpad_iterations, dirpad_iterations):
#     robot_code = get_iterated_numpad_sequence(numpad, dirpad, code, numpad_iterations=numpad_iterations, dirpad_iterations=dirpad_iterations)
#     reproduced_code = dirpad_to_numpad(numpad, dirpad, robot_code, numpad_iterations=numpad_iterations, dirpad_iterations=dirpad_iterations)
#     assert code == reproduced_code, f"Code {code} does not match reproduced code {reproduced_code} Robot code: {robot_code}"

# validate_code("0", numpad_iterations=1, dirpad_iterations=0)
# validate_code("<A", numpad_iterations=0, dirpad_iterations=1)
# validate_code("v<<A>>^A", numpad_iterations=0, dirpad_iterations=1) # Their version
# validate_code("<<vA>>^A", numpad_iterations=0, dirpad_iterations=1) # My version
# validate_code("0", numpad_iterations=1, dirpad_iterations=1)
# validate_code("0", numpad_iterations=1, dirpad_iterations=2)
# validate_code("029A", numpad_iterations=1, dirpad_iterations=2)
# validate_code("980A", numpad_iterations=1, dirpad_iterations=2)
# validate_code("179A", numpad_iterations=1, dirpad_iterations=2)
# validate_code("456A", numpad_iterations=1, dirpad_iterations=2)
# validate_code("379A", numpad_iterations=1, dirpad_iterations=2)
