import numpy as np
from functools import cache

inp = open("input.txt").readlines()


def parse_connection(var_map, line):
    left, output_wire = line.split(" -> ")
    left = left.strip()
    output_wire = output_wire.strip()

    @cache
    def get_val(w):
        return var_map[w]()

    if not " " in left:
        var_map[output_wire] = lambda: get_val(left)
    elif "AND" in left:
        l, r = left.split(" AND ")
        var_map[output_wire] = lambda: get_val(l) & get_val(r)
    elif "OR" in left:
        l, r = left.split(" OR ")
        var_map[output_wire] = lambda: get_val(l) | get_val(r)
    elif "LSHIFT" in left:
        l, r = left.split(" LSHIFT ")
        var_map[output_wire] = lambda: get_val(l) << get_val(r)
    elif "RSHIFT" in left:
        l, r = left.split(" RSHIFT ")
        var_map[output_wire] = lambda: get_val(l) >> get_val(r)
    elif "NOT" in left:
        v = left.split("NOT ")[1]
        var_map[output_wire] = lambda: ~(get_val(v))


def part_one():
    var_map = {}
    for i in range(0, 2**16-1):
        var_map[str(i)] = lambda i=i: np.uint16(i)
    for line in inp:
        parse_connection(var_map, line)
    return var_map["a"]()

def part_two():
    wire_b_signal = part_one()
    var_map = {}
    for i in range(0, 2**16-1):
        var_map[str(i)] = lambda i=i: np.uint16(i)
    for line in inp:
        parse_connection(var_map, line)
    var_map["b"] = lambda: wire_b_signal
    return var_map["a"]()

    
print("Part One:", part_one())
print("Part Two:", part_two())
