from collections import deque, defaultdict
from typing import List, Tuple, Dict

def parse_input(input_map: str) -> Tuple[Tuple[Tuple[str, ...], ...], Tuple[int, int], Tuple[int, int]]:
    grid = [list(line) for line in input_map.strip().split('\n')]
    start = None
    end = None

    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == 'S':
                start = (r, c)
                grid[r][c] = '.'  # Replace S with . for easier path finding
            elif cell == 'E':
                end = (r, c)
                grid[r][c] = '.'  # Replace E with . for easier path finding

    # Convert to tuple of tuples for immutability
    return tuple(tuple(row) for row in grid), start, end

def get_neighbors(arr: Tuple[Tuple[str, ...], ...], pos: Tuple[int, int]) -> List[Tuple[int, int]]:
    i, j = pos
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    return [(i + di, j + dj) for di, dj in directions if 0 <= i + di < len(arr) and 0 <= j + dj < len(arr[0])]

def build_distance_map(grid: Tuple[Tuple[str, ...], ...], source: Tuple[int, int]) -> Dict[Tuple[int, int], int]:
    """Calculate distances from source to all reachable points."""
    distances = {source: 0}
    queue = deque([source])

    while queue:
        pos = queue.popleft()

        for next_pos in get_neighbors(grid, pos):
            if next_pos not in distances and grid[next_pos[0]][next_pos[1]] == '.':
                distances[next_pos] = distances[pos] + 1
                queue.append(next_pos)

    return distances

def find_cheats(grid: Tuple[Tuple[str, ...], ...], start: Tuple[int, int], end: Tuple[int, int],
                cheat_range: int) -> Dict[int, int]:
    height, width = len(grid), len(grid[0])
    savings = defaultdict(int)

    # Pre-compute all valid positions
    valid_positions = [
        (r, c) for r in range(height) for c in range(width)
        if grid[r][c] == '.'
    ]

    # Pre-compute distances from start and end to all points
    start_distances = build_distance_map(grid, start)
    end_distances = build_distance_map(grid, end)

    normal_time = start_distances[end]

    # Try all possible cheat start positions
    for start_pos in valid_positions:
        if start_pos not in start_distances:  # Skip if unreachable from start
            continue

        sr, sc = start_pos
        time_to_cheat = start_distances[start_pos]

        # Try all possible cheat end positions within 2 steps
        for er in range(max(0, sr-cheat_range), min(height, sr+cheat_range+1)):
            for ec in range(max(0, sc-cheat_range), min(width, sc+cheat_range+1)):
                end_pos = (er, ec)

                if grid[er][ec] != '.' or end_pos not in end_distances:
                    continue

                # Skip if same position or too far apart
                if start_pos == end_pos or abs(er-sr) + abs(ec-sc) > cheat_range:
                    continue

                # Calculate total time using pre-computed distances
                total_time = time_to_cheat + abs(er-sr) + abs(ec-sc) + end_distances[end_pos]
                time_saved = normal_time - total_time

                if time_saved > 0:
                    savings[time_saved] += 1

    return savings

def get_num_cheats_that_save_gte_picoseconds(fname: str, cheat_range: int, savings_threshold: int, debug: bool = False):
    grid, start, end = parse_input(open(fname).read())

    print(f"Normal path length: {build_distance_map(grid, start)[end]}")

    savings = find_cheats(grid, start, end, cheat_range=cheat_range)
    if debug:
        print("\nCheats by time saved:")
        for time_saved in sorted(savings.keys()):
            print(f"Save {time_saved} picoseconds: {savings[time_saved]} cheats")

    return sum(count for time_saved, count in savings.items() if time_saved >= savings_threshold)

print("Part 1 Test: ", get_num_cheats_that_save_gte_picoseconds("test.txt", cheat_range=2, savings_threshold=10))
print("Part 1 Input:", get_num_cheats_that_save_gte_picoseconds("input.txt", cheat_range=2, savings_threshold=100))
print("Part 2 Test: ", get_num_cheats_that_save_gte_picoseconds("test.txt", cheat_range=20, savings_threshold=50))
print("Part 2 Input:", get_num_cheats_that_save_gte_picoseconds("input.txt", cheat_range=20, savings_threshold=100))
