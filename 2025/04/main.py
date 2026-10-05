
input_file = "test.txt"
input_file = "input.txt"
grid = [list(line) for line in open(input_file, "r").read().strip().split("\n")]

def get_neighbors(arr, i, j, diag=True):
    neighbors = []
    for i_d in [-1, 0, 1]:
        for j_d in [-1, 0, 1]:
            if (i_d == 0 and j_d == 0):
                pass
            elif i+i_d < 0 or j+j_d < 0:
                pass
            elif i+i_d >= len(arr) or j+j_d >= len(arr[0]):
                pass
            else:
                neighbors.append((i+i_d, j+j_d))

    # neighbors = [(i+i_d, j+j_d) for i_d in [-1, 0, 1] for j_d in [-1, 0, 1] if 0 < i+i_d < len(arr) and 0 < j+j_d < len(arr[0])]
    return neighbors

def part_one(grid):
    total = 0
    for i, row in enumerate(grid):
        for j, marker in enumerate(row):
            if marker == ".":
                continue
            neighboring_rolls = sum(map(lambda n: grid[n[0]][n[1]] == "@", get_neighbors(grid, i, j)))
            if neighboring_rolls < 4:
                total += 1
    return total

def part_two(grid):
    total = 0
    removed_paper = True
    while removed_paper:
        removed_paper = False
        for i, row in enumerate(grid):
            for j, marker in enumerate(row):
                if marker == ".":
                    continue
                neighboring_rolls = sum(map(lambda n: grid[n[0]][n[1]] == "@", get_neighbors(grid, i, j)))
                if neighboring_rolls < 4:
                    grid[i][j] = "."
                    total += 1
                    removed_paper=True
    return total


print(grid)
print(get_neighbors(grid, 0, 0))
print(get_neighbors(grid, len(grid)-1, len(grid[0])-1))
print("Part One:", part_one(grid))
print("Part Two:", part_two(grid))
