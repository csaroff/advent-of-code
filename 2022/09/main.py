
import numpy as np
np.set_printoptions(linewidth=120)

def print_knots(knots, grid_size=(28, 28)):
    grid = np.zeros(grid_size, dtype=int)
    for i, knot in enumerate(reversed(knots)):
        grid[-1 - knot[1], knot[0]] = len(knots) - i
    grid -= 1
    grid = grid.astype(str)
    grid = np.char.replace(grid, '-1', '.')
    grid = np.char.replace(grid, '0', 'H')
    print(grid)

# Only move the tail if the head is ahead of it in any direction by more than 1.
def get_next_tail_position(head, tail):
    if abs(head[0] - tail[0]) > 1 and abs(head[1] - tail[1]) > 1:
        return (head[0] + tail[0]) // 2, (head[1] + tail[1]) // 2
    if abs(head[0] - tail[0]) > 1:
        return (head[0] + tail[0]) // 2, head[1]
    if abs(head[1] - tail[1]) > 1:
        return head[0], (head[1] + tail[1]) // 2
    return tail

def update_head_position(head, direction):
    if direction == "U":
        head = head[0], head[1] + 1
    elif direction == "D":
        head = head[0], head[1] - 1
    elif direction == "L":
        head = head[0] - 1, head[1]
    elif direction == "R":
        head = head[0] + 1, head[1]
    return head

def get_tail_positions(lines, num_knots, starting_position=(0, 0)):
    knots = [starting_position] * num_knots
    previous_tails = set()
    for line in lines:
        direction, count = line.split(" ")
        count = int(count)
        for i in range(count):
            knots[0] = update_head_position(knots[0], direction)
            for i in range(len(knots) - 1):
                knots[i + 1] = get_next_tail_position(knots[i], knots[i + 1])
            previous_tails.add(knots[-1])
    return previous_tails

lines = open("input.txt").readlines()

print("Number of previous tails:", len(get_tail_positions(lines, 2)))
print("Number of previous tails:", len(get_tail_positions(lines, 10)))
