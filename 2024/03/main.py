import re

def sum_of_muls(t):
    mul_pattern = r"mul\((-?\d+),\s*(-?\d+)\)"
    matches = re.findall(mul_pattern, t)
    return sum([int(m[0]) * int(m[1]) for m in matches])

def sum_of_muls_with_donts(t):
    # dont_pattern = r"do(n't)?\(\)"
    dont_pattern = r"do(?:n't)?\(\)"
    matches = [(m.group(), m.start(), m.end()) for m in re.finditer(dont_pattern, t)]
    result = sum_of_muls(text[:matches[0][1]])
    # print(text[:matches[0][1]])
    for i, (match, start, end) in enumerate(matches):
        start, end = end, matches[i+1][1] if i < len(matches) - 1 else len(t)
        print(i, match, start, end, text[start:end], sum_of_muls(text[start:end]))
        if match == "don't()":
            continue
        result += sum_of_muls(text[start:end])
    return result

text = open("input.txt", "r").read()
# text = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
part1 = sum_of_muls(text)
print("Part 1:", part1)

part2 = sum_of_muls_with_donts(text)
print("Part 2:", part2)

