import textwrap
import itertools

def get_answer(multistack=reversed):
    with open('input.txt') as f:
        boxes, moves = f.read().split('\n\n')
        boxes = [[row[i*4+1:i*4+2] for i in range(len(row)//4 + 1)] for row in boxes.splitlines()[:-1]]
        boxes = list(map(list, itertools.zip_longest(*boxes, fillvalue=' '))) # Transpose the list of lists
        boxes = [list(filter(lambda a:a.strip(), l)) for l in boxes] # Remove empty strings
        for m in moves.splitlines():
            _, n, _, start, _, end = m.split(' ')
            n, start, end = int(n), int(start), int(end)
            boxes[end - 1] = list(multistack(boxes[start - 1][:n])) + boxes[end - 1]
            boxes[start - 1] = boxes[start - 1][n:]

        return ''.join([box[0] for box in boxes if len(box)])

print('part1', get_answer(multistack=reversed))
print('part2', get_answer(multistack=lambda a:a))
