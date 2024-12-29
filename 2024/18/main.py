from heapq import heappush, heappop

def parse_input(input_data):
    # Parse the input list of coordinates
    return [tuple(map(int, line.split(','))) for line in input_data.strip().splitlines()]

def simulate_falling_bytes(grid_size, bytes_list):
    # Initialize memory grid as safe (all `.`)
    grid = [["." for _ in range(grid_size)] for _ in range(grid_size)]
    
    # Corrupt memory based on bytes list
    for x, y in bytes_list:
        grid[y][x] = "#"

    return grid

def find_shortest_path(grid):
    grid_size = len(grid)
    start = (0, 0)
    end = (grid_size - 1, grid_size - 1)

    # Directions for moving in 4 directions (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Priority queue for Dijkstra's algorithm
    pq = [(0, start)]  # (steps, position)
    visited = set()

    while pq:
        steps, (x, y) = heappop(pq)

        # If we reach the exit, return the steps
        if (x, y) == end:
            return steps

        if (x, y) in visited:
            continue

        visited.add((x, y))

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # Check if the move is within bounds and not corrupted
            if 0 <= nx < grid_size and 0 <= ny < grid_size and grid[ny][nx] == ".":
                heappush(pq, (steps + 1, (nx, ny)))

    return -1  # No path found

def part1(input_str, grid_size, run_after):
    bytes_list = parse_input(input_str)
    grid = simulate_falling_bytes(grid_size, bytes_list[:run_after])
    return find_shortest_path(grid)

def part2(input_str, grid_size):
    bytes_list = parse_input(input_str)
    lo=0
    hi=len(bytes_list)
    run_after = (lo + hi) // 2
    while run_after != lo and run_after != hi:
        sp = find_shortest_path(simulate_falling_bytes(grid_size, bytes_list[:run_after]))
        if sp == -1:
            hi = run_after
        else:
            lo = run_after
        run_after = (lo + hi) // 2
    if find_shortest_path(simulate_falling_bytes(grid_size, bytes_list[:run_after])) != -1:
        run_after += 1
    return ",".join(map(str,  bytes_list[run_after-1]))


print(f"Part 1 Test: ", part1(open("test.txt").read(), grid_size=7, run_after=12))
print(f"Part 1 Input:", part1(open("input.txt").read(), grid_size=71, run_after=1024))

print(f"Part 2 Test: ", part2(open("test.txt").read(), grid_size=7))
print(f"Part 2 Input:", part2(open("input.txt").read(), grid_size=71))
