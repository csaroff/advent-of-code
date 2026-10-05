from copy import deepcopy
import math

def file_blocks_str(file_blocks):
    return "".join([str(fb if fb is not None else ".") for fb in file_blocks])

def nums_to_aloc_frees(nums):
    aloc_frees = [nums[2*i:2*i+2] for i in range(len(nums)//2)]
    if len(nums) % 2 != 0:
        aloc_frees.append([nums[-1], 0])
    return aloc_frees

def aloc_frees_to_init_file_blocks(aloc_frees):
    file_blocks = []
    for i, (aloc, free) in enumerate(aloc_frees):
        file_blocks.extend([i] * aloc)
        if free:
            file_blocks.extend([None] * free)
    return file_blocks

def get_updated_file_blocks_fragmented(file_blocks):
    file_blocks = deepcopy(file_blocks)
    i, j = 0, len(file_blocks) - 1
    while i < j:
        if file_blocks[i] is None:
            file_blocks[i] = file_blocks[j]
            file_blocks[j] = None
            j -= 1
            continue

        if file_blocks[i] is not None:
            i += 1
    return file_blocks

def get_updated_file_blocks(file_blocks, fragmented):
    updated_file_blocks = deepcopy(file_blocks)
    min_free = 0
    j = len(file_blocks)
    while j > 0:
        if file_blocks[j-1] is None:
            j -= 1
            continue
        num_blocks = 1 if fragmented else next((idx for idx in range(1, j) if file_blocks[j-idx] != file_blocks[j-1]), j) - 1
        if num_blocks < 1:
            break

        is_contiguous = True
        for i in range(min_free, len(file_blocks) - num_blocks):
            # Speed up the loop
            if updated_file_blocks[i] is not None:
                if is_contiguous:
                    min_free = i
                continue
            else:
                is_contiguous = False

            if i >= j:
                break

            if set(updated_file_blocks[i:i+num_blocks]) == {None}:
                # print("updated_file_blocks", file_blocks_str(updated_file_blocks))
                updated_file_blocks[i:i+num_blocks] = updated_file_blocks[j-num_blocks:j]
                updated_file_blocks[j-num_blocks:j] = [None] * num_blocks
                break
        j -= num_blocks
    return updated_file_blocks

text = open("test.txt").read().strip()
text = open("input.txt").read().strip()

nums = list(map(int, list(text)))
aloc_frees = nums_to_aloc_frees(nums)
file_blocks = aloc_frees_to_init_file_blocks(aloc_frees)

def part1(file_blocks):
    # file_blocks = get_updated_file_blocks_fragmented(file_blocks)
    file_blocks = get_updated_file_blocks(file_blocks, fragmented=True)
    return sum(i * fb for i, fb in enumerate(file_blocks) if fb is not None)

def part2(file_blocks):
    file_blocks = get_updated_file_blocks(file_blocks, fragmented=False)
    return sum(i * fb for i, fb in enumerate(file_blocks) if fb is not None)

print("Part 1", part1(file_blocks))
print("Part 2", part2(file_blocks))
