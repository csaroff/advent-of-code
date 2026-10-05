import math

def get_valid_operators(result, operands, op_candidates):
    if len(operands) < 2:
        raise ValueError("Need at least two operands to compute result")
    if len(operands) == 2:
        for op in op_candidates:
            if result == op(operands):
                return [op.__name__]
        return False
    for op in op_candidates:
        operators = get_valid_operators(result, [op(operands[:2])] + operands[2:], op_candidates=op_candidates)
        if operators:
            return [op.__name__] + operators

    return False

def product(numbers):
    return math.prod(numbers)

def concat(arr):
    return int("".join(map(str, arr)))
        


lines = open("test.txt").readlines()
lines = open("input.txt").readlines()
equations = [line.split() for line in lines]
equations = [list(map(int, [eq[0][:-1]] + eq[1:])) for eq in equations]
equations = [(eq[0], eq[1:]) for eq in equations]
part1 = sum(r for r, operands in equations if get_valid_operators(r, operands, op_candidates=[sum, product]))
print("Part 1:", part1)

part2 = sum(r for r, operands in equations if get_valid_operators(r, operands, op_candidates=[sum, product, concat]))
print("Part 2:", part2)

