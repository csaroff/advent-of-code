import bisect

input_file = "test.txt"
input_file = "input.txt"
in1, in2 = [s.split("\n") for s in open(input_file, "r").read().strip().split("\n\n")]
fresh_ranges = sorted([list(map(int, s.split("-"))) for s in in1])

def merge_ranges(ranges):
    if not ranges:
        return []

    # 1. Sort by the start value O(N log N)
    ranges.sort(key=lambda x: x[0])

    merged = [ranges[0]]

    for current_start, current_end in ranges[1:]:
        last_start, last_end = merged[-1]

        # 2. Check for overlap
        # If current start is <= last end, they overlap
        if current_start <= last_end:
            # Update the end of the last range to the max of both
            merged[-1][1] = max(last_end, current_end)
        else:
            # 3. No overlap, add as a new range
            merged.append([current_start, current_end])

    return merged

fresh_ranges = merge_ranges(fresh_ranges)
available = list(map(int, in2))

def binary_search(ranges, x):
    # Extract just the start values for the binary search
    starts = [r[0] for r in ranges]

    # bisect_right returns the index where x could be inserted while maintaining order
    idx = bisect.bisect_right(starts, x) - 1

    if idx >= 0:
        start, end = ranges[idx]
        if start <= x <= end:
            return True

    return False

def part_one():
    return sum(1 for elem in available if binary_search(fresh_ranges, elem))

def part_two():
    return sum(end - start + 1 for start, end in fresh_ranges)


print("Part One:", part_one())
print("Part Two:", part_two())
