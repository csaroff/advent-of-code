from disjoint_set import DisjointSet

def get_neighbors(arr, i, j, with_dir_symbols=False, bounded=True):
    dir_symbols = ["N", "E", "S", "W"]
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    result = [(i + di, j + dj) for di, dj in directions if not bounded or (0 <= i + di < len(arr) and 0 <= j + dj < len(arr[0]))]
    if with_dir_symbols: return list(zip(dir_symbols, result))
    return result

def get_subgrid_groups(garden):
    disjoint_set = DisjointSet()
    for i in range(len(garden)):
        for j in range(len(garden[i])):
            symbol = garden[i][j]
            matching_neighbors = [(ni, nj) for ni, nj in get_neighbors(garden, i, j) if garden[ni][nj] == symbol]
            disjoint_set.union((i, j), (i, j))
            for ni, nj in matching_neighbors:
                disjoint_set.union((i, j), (ni, nj))
    return list(disjoint_set.itersets())

def get_subgrid_area(subgrid_group):
    return len(subgrid_group)

def get_subgrid_perimeter(subgrid_group):
    perimeter = 0
    for i, j in subgrid_group:
        group_neighbors = [n for n in get_neighbors(garden, i, j) if n in subgrid_group]
        perimeter += 4 - len(group_neighbors)
    return perimeter

def get_subgrid_side_count(subgrid_group):
    i, j = next(iter(subgrid_group))
    segments = set()
    for i, j in subgrid_group:
        neighbors = get_neighbors(garden, i, j, with_dir_symbols=True, bounded=False)
        segments.update(((dir, segment) for dir, segment in neighbors if segment not in subgrid_group))
    disjoint_set = DisjointSet()
    for dir, (i, j) in segments:
        disjoint_set.union((dir, (i, j)), (dir, (i, j)))
        for n in get_neighbors(garden, i, j, bounded=False):
            if (dir, n) in segments:
                disjoint_set.union((dir, (i, j)), (dir, n))
    return len(list(disjoint_set.itersets()))


garden = [list(line.strip()) for line in open("test.txt").readlines()]
garden = [list(line.strip()) for line in open("input.txt").readlines()]

subgrid_groups = get_subgrid_groups(garden)

perimeters = [get_subgrid_perimeter(subgrid_group) for subgrid_group in subgrid_groups]
areas = [get_subgrid_area(subgrid_group) for subgrid_group in subgrid_groups]

part1 = sum(p * a for p, a in zip(perimeters, areas))
print("Part 1:", part1)

segments = [get_subgrid_side_count(subgrid_group) for subgrid_group in subgrid_groups]
part2 = sum(s * a for s, a in zip(segments, areas))
print("Part 2:", part2)
