from collections import defaultdict
import heapq
from enum import Enum
from typing import List, Tuple, Set, Dict

class Direction(Enum):
    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)

    def __eq__(self, other):
        return True

    def __hash__(self):
        return hash(self.value)

    def __lt__(self, other):
        if not isinstance(other, Direction): return NotImplemented
        return 0

    def turn_clockwise(self):
        return {
            Direction.NORTH: Direction.EAST,
            Direction.EAST: Direction.SOUTH,
            Direction.SOUTH: Direction.WEST,
            Direction.WEST: Direction.NORTH
        }[self]

    def turn_counterclockwise(self):
        return {
            Direction.NORTH: Direction.WEST,
            Direction.EAST: Direction.NORTH,
            Direction.SOUTH: Direction.EAST,
            Direction.WEST: Direction.SOUTH
        }[self]

def parse_input(filename: str) -> List[str]:
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]

def find_start_end(grid: List[str]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    start = end = None
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 'S':
                start = (x, y)
            elif cell == 'E':
                end = (x, y)
    return start, end

def find_optimal_paths(grid: List[str]) -> Tuple[int, Set[Tuple[int, int]]]:
    start_pos, end_pos = find_start_end(grid)
    rows, cols = len(grid), len(grid[0])

    # Priority queue entries: (score, x, y, direction, path)
    pq = [(0, start_pos[0], start_pos[1], Direction.EAST, {start_pos})]
    # Keep track of visited states and their scores: (x, y, direction) -> score
    visited = {}
    optimal_score = float('inf')
    optimal_paths = set()

    while pq:
        score, x, y, direction, path = heapq.heappop(pq)

        # If we've found the end, update optimal score and paths
        if (x, y) == end_pos:
            if score < optimal_score:
                optimal_score = score
                optimal_paths = {frozenset(path)}
            elif score == optimal_score:
                optimal_paths.add(frozenset(path))
            continue

        # If we've exceeded the optimal score, skip this path
        if score > optimal_score:
            continue

        state = (x, y, direction)
        if state in visited and visited[state] < score:
            continue
        visited[state] = score

        # Try moving forward
        dx, dy = direction.value
        new_x, new_y = x + dx, y + dy
        if (0 <= new_x < cols and 0 <= new_y < rows and
            grid[new_y][new_x] != '#'):
            new_path = path | {(new_x, new_y)}
            heapq.heappush(pq, (score + 1, new_x, new_y, direction, new_path))

        # Try turning clockwise
        new_dir = direction.turn_clockwise()
        heapq.heappush(pq, (score + 1000, x, y, new_dir, path))

        # Try turning counterclockwise
        new_dir = direction.turn_counterclockwise()
        heapq.heappush(pq, (score + 1000, x, y, new_dir, path))

    # Combine all optimal paths into a single set of tiles
    all_optimal_tiles = set()
    for path in optimal_paths:
        all_optimal_tiles.update(path)

    return optimal_score, all_optimal_tiles

def visualize_paths(grid: List[str], optimal_tiles: Set[Tuple[int, int]]) -> None:
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == '#':
                print('#', end='')
            elif (x, y) in optimal_tiles:
                print('O', end='')
            else:
                print('.', end='')
        print()

def main():
    # Test the first example
    grid = parse_input("test1.txt")
    score, tiles = find_optimal_paths(grid)
    print(f"Example 1 score: {score}")
    print(f"Example 1 tiles: {len(tiles)}")
    print("Example 1 visualization:")
    visualize_paths(grid, tiles)
    assert score == 7036, f"Expected 7036, got {score}"
    assert len(tiles) == 45, f"Expected 45 tiles, got {len(tiles)}"
    print()

    # Test the second example
    grid = parse_input("test2.txt")
    score, tiles = find_optimal_paths(grid)
    print(f"Example 2 score: {score}")
    print(f"Example 2 tiles: {len(tiles)}")
    print("Example 2 visualization:")
    visualize_paths(grid, tiles)
    assert score == 11048, f"Expected 11048, got {score}"
    assert len(tiles) == 64, f"Expected 64 tiles, got {len(tiles)}"
    print()

    # Solve the actual puzzle
    grid = parse_input("input.txt")
    score, tiles = find_optimal_paths(grid)
    print(f"Part 1: {score}")
    print(f"Part 2: {len(tiles)}")
    print("Full input visualization:")
    visualize_paths(grid, tiles)

if __name__ == "__main__":
    main()
