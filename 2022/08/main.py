import numpy as np
grid = np.array([[int(h) for h in line.strip()] for line in open('input.txt').readlines()])


def is_visible(grid, x, y):
    if x in (0, len(grid) - 1) or y in (0, len(grid[0]) - 1):
        return True
    max_above = max(grid[x][0:y])
    max_below = max(grid[x][y+1:])
    max_left = max(grid[0:x, y])
    max_right = max(grid[x+1:, y])
    return min(max_above, max_below, max_left, max_right) < grid[x][y]

def get_visibility_distance(heights, current_height):
    for i, height in enumerate(heights):
        if height >= current_height:
            return i+1
    return len(heights)

def get_scenic_score(grid, x, y):
    if x in (0, len(grid) - 1) or y in (0, len(grid[0]) - 1):
        return True
    visibility_above = get_visibility_distance(list(reversed(grid[x][0:y])), grid[x][y])
    visibility_below = get_visibility_distance(grid[x][y+1:], grid[x][y])
    visibility_left = get_visibility_distance(list(reversed(grid[0:x, y])), grid[x][y])
    visibility_right = get_visibility_distance(grid[x+1:, y], grid[x][y])
    return visibility_above * visibility_below * visibility_left * visibility_right

num_hidden = 0
best_visibility = 0
for i in range(1, len(grid) - 1):
    for j in range(1, len(grid[0]) - 1):
        num_hidden += not is_visible(grid, i, j)
        best_visibility = max(best_visibility, get_scenic_score(grid, i, j))


print('Visible Trees:', grid.shape[0] * grid.shape[1] - num_hidden)
print('Best Visibility:', best_visibility)


