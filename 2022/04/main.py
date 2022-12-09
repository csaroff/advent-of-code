def is_range_in_range(line):
    (lo1, hi1), (lo2, hi2) = [map(int, sections.split('-')) for sections in line.split(',')]
    return (lo2 - lo1) * (hi1 - hi2) >= 0

def overlapping_range(line):
    (lo1, hi1), (lo2, hi2) = [map(int, sections.split('-')) for sections in line.split(',')]
    # If range A is to the left of range B, then hi1 < lo2. hi1 - lo2 < 0
    # If range A is to the right of range B, then hi2 < lo1. hi2 - lo1 < 0
    return not (hi1 < lo2 or hi2 < lo1)

with open('input.txt') as f:
    lines = f.read().splitlines()
    strict_subranges = list(filter(is_range_in_range, lines))
    overlapping_ranges = list(filter(overlapping_range, lines))
    print(len(strict_subranges))
    print(len(overlapping_ranges))
