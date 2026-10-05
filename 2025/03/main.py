input_file = "test.txt"
input_file = "input.txt"
battery_banks = [list(map(int, bank)) for bank in open(input_file, "r").read().strip().split("\n")]
print(battery_banks)

def part_one(battery_banks):
    max_joltages = []
    for bank in battery_banks:
        # Flip the idx sign so that earlier indexes are weighed higher
        l, l_idx = max((j, -idx) for idx, j in enumerate(bank[:-1]))
        l_idx *= -1
        r = max(bank[l_idx+1:])
        max_joltages.append(10 * l + r)
    print(max_joltages)
    return sum(max_joltages)

def max_joltage(battery_bank, num_batteries):
    max_joltage = 0
    l_idx = -1
    for i in range(num_batteries):
        # print(f"{l_idx+1}:{i-num_batteries+1}", battery_bank[l_idx+1:i-num_batteries+i+1], max_joltage)
        l, l_idx = max((j, -idx) for idx, j in list(enumerate(battery_bank))[l_idx+1:len(battery_bank)-num_batteries+i+1])
        l_idx *= -1
        max_joltage += 10**(num_batteries-i-1) * l
    return max_joltage

def part_two(battery_banks, num_batteries=12):
    max_joltages = []
    for battery_bank in battery_banks:
        max_joltages.append(max_joltage(battery_bank, num_batteries))
    print(max_joltages)
    return sum(max_joltages)

print("Part One:", part_one(battery_banks))
print("Part Two:", part_two(battery_banks))
