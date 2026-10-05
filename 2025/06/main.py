import math
input_file = "test.txt"
input_file = "input.txt"
rows = [line.split() for line in open(input_file, "r").read().strip().split("\n")]

def part_one():
    rows = [line.split() for line in open(input_file, "r").read().strip().split("\n")]
    nums, ops = [list(map(int, row)) for row in rows[:-1]], rows[-1]
    total = 0
    for j, op in enumerate(ops):
        if op == '*':
            total += math.prod(nums[i][j] for i in range(len(nums)))
        else:
            total += sum(nums[i][j] for i in range(len(nums)))
    return total

def nums_to_cols_strs(rows):
    idx = 0
    indexes = [idx]
    while idx < len(rows[0]) - 1:
        idx += max(len(row[idx:].split()[0]) for row in rows) + 1
        indexes.append(idx)
    result = []
    for start, stop in zip(indexes[:-1], indexes[1:]):
        result.append([rows[i][start:stop-1] for i in range(len(rows))])
    return result

def col_str_r2l(col_str):
    result = []
    for i in range(len(col_str[0]) - 1, -1, -1):
        result.append(int("".join(s[i] for s in col_str).strip()))
    return result


def part_two():
    rows = [line for line in open(input_file, "r").read().strip().split("\n")]
    nums, ops = rows[:-1], rows[-1].split()
    cols_strs = nums_to_cols_strs(nums)
    r2l_cols = [col_str_r2l(col_str) for col_str in cols_strs]
    totals = [math.prod(r2l_col) if op == '*' else sum(r2l_col) for op, r2l_col in zip(ops, r2l_cols)]
    return sum(totals)


print("Part one:", part_one())
print("Part two:", part_two())
        
