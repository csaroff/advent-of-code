from collections import Counter

lines = open("input.txt", "r").readlines()
lines = [map(int, l.split()) for l in lines]
left, right = zip(*lines)
left, right = sorted(left), sorted(right)
diffs = [abs(r - l) for l, r in zip(left, right)]
print('Part 1: ', sum(diffs))

right_counter = Counter(right)
similarities = [l * right_counter[l] for l in left]
print('Part 2:', sum(similarities))
