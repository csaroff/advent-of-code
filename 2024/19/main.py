from collections import deque

def count_ways_to_form_design(patterns, design):
    """
    Function to count the number of ways a design can be formed using the available towel patterns.
    """
    # Use a dynamic programming approach to speed up the process
    ways_to_form = [1] + [0] * len(design)

    for i in range(1, len(design) + 1):
        for pattern in patterns:
            if i >= len(pattern) and design[i - len(pattern):i] == pattern:
                ways_to_form[i] += ways_to_form[i - len(pattern)]

    return ways_to_form[len(design)]

def count_possible_designs(patterns, designs, count_arrangements=False):
    """
    Function to count how many designs are possible using the available towel patterns.
    """
    possible_count = 0
    for design in designs:
        count = count_ways_to_form_design(patterns, design)
        possible_count += count if count_arrangements else int(bool(count))
    return possible_count

def parse_options_file(file_path):
    patterns, designs = open(file_path).read().strip().split("\n\n")
    patterns, designs = patterns.split(", "), designs.split("\n")
    return patterns, designs

print(f"Part 1 Test:  {count_possible_designs(*parse_options_file('test.txt'))}")
print(f"Part 1 Input: {count_possible_designs(*parse_options_file('input.txt'))}")

print(f"Part 2 Test:  {count_possible_designs(*parse_options_file('test.txt'), count_arrangements=True)}")
print(f"Part 2 Input: {count_possible_designs(*parse_options_file('input.txt'), count_arrangements=True)}")
