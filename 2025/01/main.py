def part_one(input_file):
    turns = [(t[0], int(t[1:])) for t in open(input_file, "r").readlines()]
    num_zeros = 0
    dial = 50
    for direction, distance in turns:
        if direction == 'L':
            dial = (dial - distance) % 100
        else:
            dial = (dial + distance) % 100
        if dial == 0:
            num_zeros += 1
        # print(f"{direction}{distance} landed us at {dial}")
    return num_zeros

def part_two(input_file):
    turns = [(t[0], int(t[1:])) for t in open(input_file, "r").readlines()]
    num_zeros = 0
    dial = 50
    for direction, distance in turns:
        if direction == 'L':
            num_zeros += (distance - dial) // 100 + 1 - (dial == 0)
            dial = (dial - distance) % 100
        else:
            num_zeros += (dial + distance) // 100
            dial = (dial + distance) % 100
        # print(f"{direction}{distance} landed us at {dial} with {num_zeros} zeros")
    return num_zeros


print("Part 1:", part_one("input.txt"))
print("Part 2:", part_two("input.txt"))


