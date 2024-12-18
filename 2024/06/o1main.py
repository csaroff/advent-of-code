import sys
from copy import deepcopy

def read_grid(text):
    return [list(line) for line in text.strip().split("\n")]

def find_guard(grid):
    """
    Finds the guard's starting position and initial direction.
    Returns a tuple (x, y), direction.
    """
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell in '^v<>':
                return (x, y), cell
    return None, None

def turn_right(direction):
    """
    Given a current direction, returns the direction after turning right.
    Directions are represented as '^', '>', 'v', '<'.
    """
    dirs = ['^', '>', 'v', '<']
    idx = dirs.index(direction)
    return dirs[(idx + 1) % 4]

def move_forward(pos, direction):
    """
    Given a current position and direction, returns the next position after moving forward.
    """
    x, y = pos
    if direction == '^':
        return (x, y - 1)
    elif direction == '>':
        return (x + 1, y)
    elif direction == 'v':
        return (x, y + 1)
    elif direction == '<':
        return (x - 1, y)

def is_inside(pos, grid):
    """
    Checks if a given position is inside the grid boundaries.
    """
    x, y = pos
    return 0 <= y < len(grid) and 0 <= x < len(grid[0])

def simulate(grid, start_pos, start_dir, record_positions=False):
    """
    Simulates the guard's movement on the grid.
    If record_positions is True, returns the set of positions visited before exiting or looping.
    Otherwise, returns True if a loop is detected, False if the guard exits the grid.
    """
    pos = start_pos
    direction = start_dir
    seen = set()
    visited_positions = set()

    while True:
        state = (pos, direction)
        if state in seen:
            if record_positions:
                return visited_positions  # Loop detected
            return True  # Loop detected
        seen.add(state)
        visited_positions.add(pos)

        # Determine the cell in front
        next_pos = move_forward(pos, direction)
        if not is_inside(next_pos, grid):
            if record_positions:
                return visited_positions  # Guard exits the grid
            return False  # Guard exits the grid

        cell_ahead = grid[next_pos[1]][next_pos[0]]
        if cell_ahead == '#':
            # Turn right
            direction = turn_right(direction)
        else:
            # Move forward
            pos = next_pos

def main():
    grid = read_grid(open("test.txt").read())
    grid = read_grid(open("input.txt").read())
    
    # Find the guard's starting position and direction
    start_pos, start_dir = find_guard(grid)
    if start_pos is None:
        print("No guard found on the grid.")
        return
    
    # Part 1: Simulate the guard's movement and record visited positions
    visited = simulate(grid, start_pos, start_dir, record_positions=True)
    part1_answer = len(visited)
    print(f"Part 1: The guard visits {part1_answer} distinct positions before leaving the grid.")
    
    # Part 2: Determine valid obstruction positions that cause the guard to loop
    # Exclude the starting position
    obstruction_candidates = visited - {start_pos}
    
    loop_count = 0
    for obs in obstruction_candidates:
        x, y = obs
        if grid[y][x] != '.':
            continue  # Only place obstruction on empty cells
        # Create a deep copy of the grid and add obstruction
        modified_grid = deepcopy(grid)
        modified_grid[y][x] = '#'
        # Simulate the guard's movement on the modified grid
        has_loop = simulate(modified_grid, start_pos, start_dir)
        if has_loop:
            loop_count += 1
    
    part2_answer = loop_count
    print(f"Part 2: There are {part2_answer} possible obstruction positions that cause the guard to loop.")

if __name__ == "__main__":
    main()

