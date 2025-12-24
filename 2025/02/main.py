def part_one(input_file):
    id_ranges = [list(map(int, s.split("-"))) for s in open(input_file, "r").read().split(",")]

    invalid_id_sum = 0
    for lo, hi in id_ranges:
        for id in map(str, range(lo, hi + 1)):
            if len(id) % 2 == 0 and id[:len(id)//2] == id[len(id)//2:]:
                invalid_id_sum += int(id)
    return invalid_id_sum


def part_two(input_file):
    # Returns true of all subsequences of a given size match.
    def all_sequences_match(id, sequence_size):
        for sequence_idx in range(len(id) // sequence_size):
            if id[sequence_idx*sequence_size:(sequence_idx+1)*sequence_size] != id[:sequence_size]:
                return False
        return True

    # An id is considered invalid if it is made up of any-sized sequence of repeating digits.
    def is_id_invalid(id):
        for sequence_size in range(1, len(id) // 2 + 1):
            if len(id) % sequence_size == 0 and all_sequences_match(id, sequence_size):
                return True
        return False

    id_ranges = [list(map(int, s.split("-"))) for s in open(input_file, "r").read().split(",")]

    invalid_id_sum = 0
    for lo, hi in id_ranges:
        for id in map(str, range(lo, hi + 1)):
            if is_id_invalid(id):
                # print(f"Invalid id {id}")
                invalid_id_sum += int(id)
    return invalid_id_sum

print(f"Part 1:", part_one("test.txt"))
print(f"Part 1:", part_one("input.txt"))

print(f"Part 2:", part_two("test.txt"))
print(f"Part 2:", part_two("input.txt"))
