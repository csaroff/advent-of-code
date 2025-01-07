from pprint import pprint
import itertools
numpad = [["7",  "8", "9"],
          ["4",  "5", "6"],
          ["1",  "2", "3"],
          [None, "0", "A"]]

dirpad = [[None, "^", "A"],
          ["<",  "v", ">"]]

dir_symbol_to_direction = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}

def get_shortest_path(numpad, start_symbol, end_symbol):
    start_pos = None
    end_pos = None
    for i, row in enumerate(numpad):
        for j, cell in enumerate(row):
            if cell == start_symbol:
                start_pos = (i, j)
            if cell == end_symbol:
                end_pos = (i, j)
    if start_pos is None or end_pos is None:
        raise ValueError(f"Start or end symbol not found in numpad")

    di, dj = (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
    return "" + (">" * dj if dj > 0 else "<" * -dj) + ("^" * -di if di < 0 else "v" * di)

s, e = "A", "9"; sp = get_shortest_path(numpad, s, e); assert sp == "^^^", f"{s} -> {e}: {sp}"
s, e = "A", "0"; sp = get_shortest_path(numpad, s, e); assert sp == "<", f"{s} -> {e}: {sp}"
s, e = "A", "A"; sp = get_shortest_path(numpad, s, e); assert sp == "", f"{s} -> {e}: {sp}"
s, e = "7", "9"; sp = get_shortest_path(numpad, s, e); assert sp == ">>", f"{s} -> {e}: {sp}"
s, e = "8", "0"; sp = get_shortest_path(numpad, s, e); assert sp == "vvv", f"{s} -> {e}: {sp}"


def is_valid_movement_sequence(numpad, start_pos, movement_sequence):
    pi, pj = start_pos
    for symbol in movement_sequence:
        if symbol == "A": continue
        di, dj = dir_symbol_to_direction[symbol]
        pi, pj = (pi + di, pj + dj)
        if numpad[pi][pj] is None:
            return False
    return True

def get_paths(numpad, start_symbol, end_symbol):
    start_pos = None
    end_pos = None
    for i, row in enumerate(numpad):
        for j, cell in enumerate(row):
            if cell == start_symbol: start_pos = (i, j)
            if cell == end_symbol: end_pos = (i, j)
    if start_pos is None or end_pos is None:
        raise ValueError(f"Start or end symbol not found in numpad")

    di, dj = (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])

    movement_sequences = itertools.permutations("" + (">" * dj if dj > 0 else "<" * -dj) + ("^" * -di if di < 0 else "v" * di))
    return [movement_sequence for movement_sequence in movement_sequences if is_valid_movement_sequence(numpad, start_pos, movement_sequence)]

def pairwise(sliceable):
    return zip(sliceable, sliceable[1:])

def get_iterated_numpad_sequence(numpad, dirpad, numpad_sequence, iterations=2, debug=False):
    keypad_sequence = "A".join([get_shortest_path(numpad, s, e) for s, e in pairwise("A" + numpad_sequence)]) + "A"
    if debug:
        print(keypad_sequence)

    for _ in range(iterations):
        keypad_sequence = "A".join([get_shortest_path(dirpad, s, e) for s, e in pairwise("A" + keypad_sequence)]) + "A"
        if debug:
            print(keypad_sequence)
    return keypad_sequence

def get_complexity(numpad, dirpad, numpad_sequence, iterations=2):
    iterated_numpad_sequence = get_iterated_numpad_sequence(numpad, dirpad, numpad_sequence, iterations)
    print(len(iterated_numpad_sequence), int(numpad_sequence.replace("A", "")))
    return len(iterated_numpad_sequence) * int(numpad_sequence.replace("A", ""))
    # return len(iterated_numpad_sequence), int(numpad_sequence.replace("A", "").replace("0", ""))

def part1(codes):
    # return [get_complexity(numpad, dirpad, code, 2) for code in codes]
    return sum(get_complexity(numpad, dirpad, code, 2) for code in codes)

print("Part 1 Test: ", part1(open("test.txt").read().strip().splitlines()))
# print("Part 1 Input:", part1(open("input.txt").read().strip().splitlines()))

# print(get_iterated_numpad_sequence(numpad, dirpad, "179A", 2, debug=True))
# print(get_iterated_numpad_sequence(numpad, dirpad, "1", 2, debug=True))

def _dirpad_to_numpad(pad, sequence, starting_position):
    pi, pj = starting_position
    new_sequence = ""
    for symbol in sequence:
        if symbol == "A":
            new_sequence += pad[pi][pj]
            continue
        di, dj = dir_symbol_to_direction[symbol]
        pi, pj = (pi + di, pj + dj)
        if pad[pi][pj] is None:
            raise ValueError(f"Invalid symbol: {symbol}")
    return new_sequence

def dirpad_to_numpad(numpad, dirpad, sequence, iterations=2):
    for _ in range(iterations):
        print(sequence)
        sequence = _dirpad_to_numpad(dirpad, sequence, starting_position=(0, 2))

    print("line 86: ", sequence)
    sequence = _dirpad_to_numpad(numpad, sequence, starting_position=(3, 2))
    print("line 88: ", sequence)
    return sequence
