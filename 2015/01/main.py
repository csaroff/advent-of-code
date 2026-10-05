instructions = open("input.txt", "r").read().strip()


def part_one(instructions):
    end_floor = sum([1 if instr == '(' else -1 for instr in instructions])
    return end_floor

def part_two(instructions):
    current_floor = 0
    for idx, instr in enumerate(instructions):
        current_floor += 1 if instr == '(' else -1
        if current_floor < 0:
            return idx + 1
    return -1


print("Part 1", part_one(instructions))
print("Part 2", part_two(instructions))
