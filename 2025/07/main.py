from functools import lru_cache

input_file = "test.txt"
input_file = "input.txt"
rows = open(input_file, "r").read().strip().split("\n")

def part_one():
    start_idx = rows[0].index("S")
    beam_idxs = set([start_idx])
    split_count = 0
    for row in rows:
        new_beam_idxs = set()
        for beam_idx in beam_idxs:
            if row[beam_idx] == '.':
                new_beam_idxs.add(beam_idx)
            else:
                new_beam_idxs.add(beam_idx-1)
                new_beam_idxs.add(beam_idx+1)
                split_count += 1
        beam_idxs = new_beam_idxs
    return split_count
 

@lru_cache(maxsize=1000000)
def num_splits(i, j):
    if i == len(rows)-1:
        return 1
    if rows[i+1][j] == '^':
        return num_splits(i+1, j-1) + num_splits(i+1, j+1)
    return num_splits(i+1, j)

        
def part_two():
    start_idx = rows[0].index("S")
    return num_splits(0, start_idx)

print("Part One:", part_one())
print("Part Two:", part_two())
        

