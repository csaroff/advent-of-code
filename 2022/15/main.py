import numpy as np

def get_coordinates(stmts):
    return tuple([int(stmt.split("=")[-1]) for stmt in stmts.split(", ")])

def get_beacons_and_sensors():
    beacons_and_sensors = []
    for line in open("input.txt").readlines():
        sensor, beacon = line.split(": ")
        sensor = get_coordinates(sensor.split("Sensor at ")[-1])
        beacon = get_coordinates(beacon.split("closest beacon is at ")[-1])
        beacons_and_sensors.append((sensor, beacon))
    return beacons_and_sensors

def get_row_blacklist(y, beacons_and_sensors=get_beacons_and_sensors()):
    row_blacklist = []
    for sensor, beacon in beacons_and_sensors:
        manhattan_distance = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
        distance_to_y = abs(sensor[1] - y)
        horizontal_distance = manhattan_distance - distance_to_y
        if horizontal_distance < 0:
            continue
        row_blacklist.append((sensor[0] - horizontal_distance, sensor[0] + horizontal_distance))

    return row_blacklist

def get_blacklist(y, min_x=None, max_x=None, row=None):
    row_blacklist = get_row_blacklist(y)
    starts, ends = zip(*row_blacklist)
    row_start = min(starts) if min_x is None else min_x
    row_end = max(ends) if max_x is None else max_x
    if row is None:
        row = np.full((row_end-row_start,), 0, dtype=np.int8)
    else:
        row = row * 0
    for start, end in row_blacklist:
        row[max(start-row_start, 0):end-row_start+1] = 1

    # print(row)
    return row


def part_2(min_x=0, max_x=400000):
    blacklist = np.full((max_x-min_x,), 0, dtype=np.int32)
    ones = blacklist * 0 + 1

    for y in range(min_x, max_x):
        blacklist = get_blacklist(y=y, min_x=min_x, max_x=max_x, row=blacklist)
        # if blacklist.sum() != max_x - min_x:
        if blacklist == ones:
            col_idx = np.argwhere(blacklist == 0)
            return col_idx[0][0] * 4000000 + y

# print("Part 1: ", get_blacklist(y=10).sum())
# print("Part 2: ", part_2(min_x=0, max_x=20))

print("Part 1: ", get_blacklist(y=2000000).sum())
print("Part 2: ", part_2(min_x=0, max_x=400000))
