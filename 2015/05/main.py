from collections import Counter

strings = open("input.txt", "r").readlines()


def contains_min_vowels(s, min_vowel_count=3):
    counter = Counter(s)
    vcount = 0
    for c in s:
        if c in "aeiou":
            vcount += 1
    return vcount >= min_vowel_count

def contains_repeat_letters(s, min_repeat_count=2):
    prev = s[0]
    for curr in s[1:]:
        if prev == curr:
            return True
        prev = curr
    return False

def contains_cursed_pattern(s, cursed_patterns=["ab", "cd", "pq", "xy"]):
    for pattern in cursed_patterns:
        if pattern in s:
            return True
    return False

def is_nice_p1(s):
    return contains_min_vowels(s) and contains_repeat_letters(s) and not contains_cursed_pattern(s)

def part_one(strings):
    return sum(1 if is_nice_p1(s) else 0 for s in strings)

def contains_nonoverlapping_pairs(s):
    pair_to_idx = {}
    for i in range(len(s) - 1):
        pair = s[i:i+2]
        if pair_to_idx.get(pair) == i-1:
            continue
        if pair in pair_to_idx:
            return True
        pair_to_idx[pair] = i
    return False

def contains_repeat_skip_letter(s):
    for i in range(len(s) - 2):
        if s[i] == s[i+2]:
            return True
    return False

def is_nice_p2(s):
    return contains_nonoverlapping_pairs(s) and contains_repeat_skip_letter(s)


def part_two(strings):
    return sum(1 if is_nice_p2(s) else 0 for s in strings)
        
print("Part One:", part_one(strings))
print("Part Two:", part_two(strings))
