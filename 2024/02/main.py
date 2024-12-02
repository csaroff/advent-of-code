
def is_increasing(report):
    diffs = [report[i+1] - report[i] for i in range(len(report) - 1)]
    return all(diff >= 0 for diff in diffs) or all(diff <= 0 for diff in diffs)

def is_diff_bounded(report):
    diffs = [report[i+1] - report[i] for i in range(len(report) - 1)]
    return all(abs(diff) >= 1 and abs(diff) <= 3 for diff in diffs)

def is_safe(report):
    return is_increasing(report) and is_diff_bounded(report)

def is_safe_tolerating_removal(report):
    return any(is_safe(report[:i] + report[i+1:]) for i in range(len(report)))

lines = open("input.txt", "r").readlines()
reports = [list(map(int, l.split())) for l in lines]

part1 = sum([is_safe(report) for report in reports])
print("Part 1:", part1)

part2 = sum([is_safe_tolerating_removal(report) for report in reports])
print("Part 2:", part2)



