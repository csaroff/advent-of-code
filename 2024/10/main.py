from pprint import pprint
tmap = [[int(n) for n in line.strip()] for line in open("test.txt").readlines()]
tmap = [[int(n) for n in line.strip()] for line in open("input.txt").readlines()]

def get_neighbors(arr, i, j):
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    return [(i + di, j + dj) for di, dj in directions if 0 <= i + di < len(arr) and 0 <= j + dj < len(arr[0])]

def get_peaks(tmap, i, j):
    elevation = tmap[i][j]
    if elevation == 9:
        return {(i, j)}

    return set().union(*[get_peaks(tmap, ni, nj) for ni, nj in get_neighbors(tmap, i, j) if tmap[ni][nj] == elevation + 1])

def get_rating(tmap, i, j):
    elevation = tmap[i][j]
    if elevation == 9:
        return 1

    return sum(get_rating(tmap, ni, nj) for ni, nj in get_neighbors(tmap, i, j) if tmap[ni][nj] == elevation + 1)

def get_score(tmap, i, j):
    return len(get_peaks(tmap, i, j))

part1 = sum(get_score(tmap, i, j) for i in range(len(tmap)) for j in range(len(tmap[0])) if tmap[i][j] == 0)
print("Part 1", part1)

part2 = sum(get_rating(tmap, i, j) for i in range(len(tmap)) for j in range(len(tmap[0])) if tmap[i][j] == 0)
print("Part 2", part2)
