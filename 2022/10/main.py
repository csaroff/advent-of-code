import numpy as np
np.set_printoptions(linewidth=120)


cycle = 1
register_x = 1
signal_strengths = []
crt = np.full((6, 40), ".")

lines = [line.strip() for line in open("input.txt").readlines()]

def update_signal_strengths(cycle):
    if cycle in list(range(20, 221, 40)):
        signal_strengths.append(cycle * register_x)

def update_crt(cycle):
    crt[cycle//40, cycle%40] = "#" if cycle%40 in (register_x - 1, register_x, register_x + 1) else "."

for line in lines:
    if line == "noop":
        update_crt(cycle-1)
        cycle += 1
        update_signal_strengths(cycle)
    else:
        addx, x = line.split(" ")
        x = int(x)
        for i in range(2):
            update_crt(cycle-1)
            cycle += 1

            if i == 1:
                register_x += x

            update_signal_strengths(cycle)



print("signal strength: ", sum(signal_strengths))
for row in crt:
    print("".join(row))

