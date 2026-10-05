def get_token_cost(X1, Y1, X2, Y2, Px, Py):
    determinant = X1 * Y2 - X2 * Y1

    if determinant == 0:
        return 0

    a_num = Px * Y2 - Py * X2
    b_num = X1 * Py - Y1 * Px

    if a_num % determinant != 0 or b_num % determinant != 0:
        return 0

    k = 0
    while True:
        a = (a_num // determinant) + k * X2
        b = (b_num // determinant) + k * -X1
        if a >= 0 and b >= 0:
            return 3 * a + b
        if k > abs(determinant):
            return 0
        k += 1

def input_to_conditions(input):
    return [list(map(int, [xy[2:] for xy in inp.strip().split(": ")[-1].split(", ")])) for inp in input.split("\n")]

def get_p1_tokens(conditions):
    (a, b, prize) = conditions
    (ax, ay), (bx, by), (px, py) = a, b, [p for p in prize]
    b_pushes = min(px // bx, py // by)
    while b_pushes > 0:
        remaining_x, remaining_y = px - bx * b_pushes, py - by * b_pushes
        if remaining_x == 0 and remaining_y == 0:
            return b_pushes
        a_pushes = min(remaining_x // ax, remaining_y // ay)
        remaining_x, remaining_y = remaining_x - ax * a_pushes, remaining_y - ay * a_pushes
        if remaining_x == 0 and remaining_y == 0:
            return 3 * a_pushes + b_pushes
        b_pushes -= 1
    return 0

inputs = open("test.txt").read().strip().split("\n\n")
inputs = open("input.txt").read().strip().split("\n\n")

conditions = [input_to_conditions(input) for input in inputs]

machines = [(*a, *b, *prize) for a, b, prize in conditions]
part1 = sum(get_token_cost(*machine) for machine in machines)
print("Part 1:", part1)

machines = [(*a, *b, *[p + 10000000000000 for p in prize]) for a, b, prize in conditions]
part2 = sum(get_token_cost(*machine) for machine in machines)
print("Part 2:", part2)
