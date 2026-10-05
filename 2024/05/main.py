from functools import cmp_to_key

def is_valid(l, r):
    if (r, l) in ordering_rules:
        return False
    return True

def compare(l, r):
    if (l, r) in ordering_rules:
        return -1
    if (r, l) in ordering_rules:
        return 1
    if l == r:
        return 0
    return None
    
def is_valid_production(p):
    is_valids = [is_valid(l, r) for i, l in enumerate(p[:-1]) for r in p[1+i:]]
    return all(is_valids)

text = open("test.txt", "r").read()
text = open("input.txt", "r").read()
ordering_rules_str, productions_str = text.strip().split("\n\n")

ordering_rules = set([tuple(map(int, r.split("|"))) for r in ordering_rules_str.split("\n")])
productions = [list(map(int, p.split(","))) for p in productions_str.split("\n")]
sorted_productions = [list(sorted(p, key=cmp_to_key(compare))) for p in productions]

part1 = sum(p[len(p)//2] for p in productions if is_valid_production(p))
print("Part 1:", part1)

part1 = sum(p[len(p)//2] for p, ps in zip(productions, sorted_productions) if p == ps)
print("Part 1:", part1)

part2 = sum(ps[len(ps)//2] for p, ps in zip(productions, sorted_productions) if p != ps)
print("Part 2:", part2)
