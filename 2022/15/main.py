import numpy as np
np.set_printoptions(linewidth=120)

def get_coordinates(stmts):
    return tuple(reversed([int(stmt.split("=")[-1]) for stmt in stmts.split(", ")]))

def get_beacons_and_sensors():
    beacons = []
    sensors = []
    for line in open("input.txt").readlines():
        sensor, beacon = line.split(": ")
        sensors.append(get_coordinates(sensor.split("Sensor at ")[-1]))
        beacons.append(get_coordinates(beacon.split("closest beacon is at ")[-1]))
    return sensors, beacons

def get_grid(min_gridsize=None, max_gridsize=None):
    sensors, beacons = get_beacons_and_sensors()
    if min_gridsize is None:
        min_gridsize = min([min(s + b) for s, b in zip(sensors, beacons)])
        max_gridsize = max([max(s + b) for s, b in zip(sensors, beacons)])

    print("beacons", beacons)

    gridspan = max_gridsize - min_gridsize
    grid = np.full((gridspan+1, gridspan+1), ".")
    for sensor, beacon in zip(sensors, beacons):
        manhattan_distance = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
        x, y = sensor
        for i in range(manhattan_distance+1):
            row_start = max(0, x-i-min_gridsize)
            row_end = min(gridspan+1, x+i+1-min_gridsize)
            col_start = max(0, y-manhattan_distance+i-min_gridsize)
            col_end = min(gridspan+1, y+manhattan_distance-i+1-min_gridsize)
            grid[row_start:row_end, col_start:col_end] = "#"

    for s, b in zip(sensors, beacons):
        if min(b) >= min_gridsize and max(b) <= max_gridsize:
            if b[0] == 10:
                print(s, b)
            grid[b[0]-min_gridsize, b[1]-min_gridsize] = "B"
        if min(s) >= min_gridsize and max(s) <= max_gridsize:
            grid[s[0]-min_gridsize, s[1]-min_gridsize] = "S"

    return grid, min_gridsize, max_gridsize

def get_part1(check_row):
    grid, min_gridsize, max_gridsize = get_grid()
    return (grid[10-min_gridsize] == "#").sum() + (grid[10-min_gridsize] == "S").sum()

def get_part2(min_gridsize, max_gridsize):
    pass


print("Part 1: ", get_part1(check_row=10))
# print("Part 1: ", get_part1(min_gridsize=-2, max_gridsize=26, check_row=10))

# print("Part 1: ", (get_grid(min_gridsize=-40, max_gridsize=40)[10] == "#").sum())
