from collections import Counter, defaultdict
from functools import lru_cache
from collections.abc import Iterable

stones = list(map(int, open("test.txt").read().strip().split()))
stones = list(map(int, open("input.txt").read().strip().split()))

@lru_cache(maxsize=None)
def evolve(stone):
    if stone == 0:
        return (1,)
    str_stone = str(stone)
    if len(str_stone) % 2 == 0:
        return (int(str_stone[:len(str_stone)//2]), int(str_stone[len(str_stone)//2:]))
    return (stone * 2024,)

def blink(stones):
    new_stones = defaultdict(int)
    for stone, count in stones.items():
        for sprime in evolve(stone):
            new_stones[sprime] += count
    return new_stones

def blink_x(stones, x):
    stones = Counter(stones)
    for i in range(x):
        stones = blink(stones)
    return stones

part1 = sum(blink_x(stones, 25).values())
print("Part 1", part1)

part2 = sum(blink_x(stones, 75).values())
print("Part 2", part2)
