import hashlib

inp = "bgvyzdsv"

def min_hash(text, num_zeros):
    count = 0
    while True:
        md5_hash = hashlib.md5((text + str(count)).encode('utf-8')).hexdigest()
        if md5_hash[:num_zeros] == "0" * num_zeros:
            return count
        count += 1

def part_one(text):
    return min_hash(text, 5)

def part_two(text):
    return min_hash(text, 6)

print("Part One:", part_one(inp))
print("Part One:", part_two(inp))
