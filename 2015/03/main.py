directions = open("input.txt").read()


# Takes in current x, y, and a movement direction and returns your new location
def move(x, y, direction):
    if direction == "^":
        return x, y+1
    elif direction == ">":
        return x+1, y
    elif direction == "v":
        return x, y-1
    else:
        return x-1, y

def part_one(directions):
    current = (0, 0)
    visited = set([current])

    for direction in directions:
        cx, cy = current
        current = move(cx, cy, direction)
        visited.add(current)

    return len(visited)


def part_two(directions):
    santa_dirs = [d for i, d in enumerate(directions) if i % 2 == 0]
    robo_dirs = [d for i, d in enumerate(directions) if i % 2 == 1]

    current = (0, 0)
    visited = set([current])

    for direction in santa_dirs:
        cx, cy = current
        current = move(cx, cy, direction)
        visited.add(current)

    current = (0, 0)

    for direction in robo_dirs:
        cx, cy = current
        current = move(cx, cy, direction)
        visited.add(current)

    return len(visited)

print(part_one(directions))
print(part_two(directions))
