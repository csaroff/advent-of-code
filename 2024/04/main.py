import numpy as np
text = open("input.txt", "r").readlines()

def array_iterations(arr):
    array = np.array(arr)
    results = {}

    # Horizontal and backward horizontal
    results['horizontal'] = ["".join(row) for row in array]
    results['horizontal_backwards'] = ["".join(row[::-1]) for row in array]

    # Vertical and backward vertical
    results['vertical'] = ["".join(col) for col in array.T]
    results['vertical_backwards'] = ["".join(col[::-1]) for col in array.T]

    # Diagonal and backward diagonal
    diags = [array.diagonal(i) for i in range(-array.shape[0]+1, array.shape[1])]
    anti_diags = [np.fliplr(array).diagonal(i) for i in range(-array.shape[0]+1, array.shape[1])]
    results['diagonal'] = ["".join(diag) for diag in diags]
    results['diagonal_backwards'] = ["".join(diag[::-1]) for diag in diags]

    # Anti-diagonal and backward anti-diagonal
    results['anti_diagonal'] = ["".join(diag) for diag in anti_diags]
    results['anti_diagonal_backwards'] = ["".join(diag[::-1]) for diag in anti_diags]

    return results

def count_horizontal(puzzle, word):
    total = 0
    for s in puzzle:
        total += sum(s[i:].startswith(word) for i in range(len(s)))
    return total

def count_all_occurrences(puzzle, word):
    total = 0
    for order_name, order_board in array_iterations(text).items():
        total += count_horizontal(order_board, word)
    return total

def count_x_mas(puzzle):
    result = 0
    for i in range(len(puzzle) - 2):
        for j in range(len(puzzle[i]) - 2):
            sub_puzzle = [p[j:j+3] for p in puzzle[i:i+3]]
            counts = { order_name: count_horizontal(order_board, "MAS") for order_name, order_board in array_iterations(sub_puzzle).items() }
            if max(counts["diagonal"], counts["diagonal_backwards"]) + max(counts["anti_diagonal"], counts["anti_diagonal_backwards"]) == 2:
                result += 1
    return result


text = [list(t.strip()) for t in text]
part1 = count_all_occurrences(text, "XMAS")
print("Part 1:", part1)

part2 = count_x_mas(text)
print("Part 2:", part2)
    
