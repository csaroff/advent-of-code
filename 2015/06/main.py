import numpy as np

lights_per_row = 1000
lights_per_col = lights_per_row
lines = open("input.txt").readlines()

# lines = [
#     "turn on 0,0 through 999,999",
#     "toggle 0,0 through 999,0",
#     "turn off 499,499 through 500,500"
# ]

# Return op, top, left, bottom, right
def parse_line(line):
    lleft, br = line.split(" through ")
    op, tl = lleft.rsplit(" ", maxsplit=1)
    top, left = list(map(int, tl.split(",")))
    bottom, right = list(map(int, br.split(",")))
    return op, top, left, bottom, right

def run_p1(lights, instruction):
    op, top, left, bottom, right = instruction
    if op == "turn on":
        lights[top:bottom+1,left:right+1] = 1
    elif op == "turn off":
        lights[top:bottom+1,left:right+1] = 0
    else:
        lights[top:bottom+1,left:right+1] = 1 - lights[top:bottom+1,left:right+1]

    return lights

instructions = [parse_line(line) for line in lines]

def part1(instructions):
    lights = np.zeros((lights_per_row, lights_per_col))
    for instruction in instructions:
        run_p1(lights, instruction)

    return int(np.sum(lights))

def run_p2(lights, instruction):
    op, top, left, bottom, right = instruction
    if op == "turn on":
        lights[top:bottom+1,left:right+1] += 1
    elif op == "turn off":
        lights[top:bottom+1,left:right+1] -= 1
        np.maximum(lights, 0, lights)
    else:
        lights[top:bottom+1,left:right+1] += 2

    return lights

instructions = [parse_line(line) for line in lines]

def part2(instructions):
    lights = np.zeros((lights_per_row, lights_per_col))
    for instruction in instructions:
        run_p2(lights, instruction)

    return int(np.sum(lights))

print("Part One:", part1(instructions))
print("Part Two:", part2(instructions))
