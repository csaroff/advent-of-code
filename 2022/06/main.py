with open('input.txt') as f:
    data = f.readlines()[0]

def get_start_index(data, num_uniques):
    for i in range(len(data) - num_uniques):
        if len(set(data[i:i+num_uniques])) == num_uniques:
            return i + num_uniques

print('part1', get_start_index(data, num_uniques=4))
print('part1', get_start_index(data, num_uniques=14))
