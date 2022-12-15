import numpy as np
np.set_printoptions(linewidth=120)


def get_grid(endless_bottom=False):
    lines = [[tuple(map(int, reversed(p.split(",")))) for p in line.split(" -> ")] for line in open("input.txt").readlines()]
    xs = [x for points in lines for x, y in points]
    ys = [y for points in lines for x, y in points]
    minx, maxx = min(0, min(xs)), max(xs)
    miny, maxy = min(ys), max(max(ys), 500)

    if endless_bottom:
        maxx += 2
        miny -= maxx - minx
        maxy += maxx - minx

    grid = np.full((maxx+1, maxy+1), ".")

    if endless_bottom:
        grid[-1, :] = "#"

    grid[0, 500] = "+"

    for points in lines:
        for i in range(len(points)-1):
            x1, y1 = points[i]
            x2, y2 = points[i+1]
            if x1 == x2:
                grid[x1, min(y1, y2):max(y1, y2)+1] = "#"
            else:
                grid[min(x1, x2):max(x1, x2)+1, y1] = "#"
    return grid

def get_rest_position(grid, x, y):
    while True:
        if x+1 >= len(grid):
            return -1, -1
        if grid[x+1, y] == ".":
            x += 1
        elif grid[x+1, y-1] == ".":
            x += 1
            y -= 1
        elif grid[x+1, y+1] == ".":
            x += 1
            y += 1
        else:
            return x, y

def get_sand_count(grid):
    count = 0
    while True:
        x, y = get_rest_position(grid, 0, 500)
        if x == -1:
            break
        grid[x, y] = "o"
        count += 1
        if x == 0 and y == 500:
            break
    return count

print("Part 1: ", get_sand_count(get_grid(endless_bottom=False)))
print("Part 2: ", get_sand_count(get_grid(endless_bottom=True)))
