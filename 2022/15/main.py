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

def interval_union(intervals):
    b = []
    for begin,end in sorted(intervals):
        if b and b[-1][1] >= begin - 1:
            b[-1][1] = max(b[-1][1], end)
        else:
            b.append([begin, end])
    return b

def get_unioned_blacklist_intervals(y, beacons_and_sensors=get_beacons_and_sensors()):
    intervals = []
    for sensor, beacon in beacons_and_sensors:
        manhattan_distance = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
        distance_to_y = abs(sensor[1] - y)
        horizontal_distance = manhattan_distance - distance_to_y
        if horizontal_distance < 0:
            continue
        intervals.append((sensor[0] - horizontal_distance, sensor[0] + horizontal_distance))
    intervals = interval_union(intervals)
    return intervals

def part_2(min_x=0, max_x=4000000):
    for y in range(min_x, max_x):
        intervals = get_unioned_blacklist_intervals(y=y)
        if len(intervals) > 1:
            gap = intervals[0][1] + 1
            return gap * 4000000 + y

# print("Part 1: ", get_blacklist(y=10).sum())
# print("Part 2: ", part_2(min_x=0, max_x=20))

print("Part 1: ", sum([end - start for start, end in get_unioned_blacklist_intervals(y=2000000)]))
print("Part 2: ", part_2(min_x=0, max_x=4000000))
