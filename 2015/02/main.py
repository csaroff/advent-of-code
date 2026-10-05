boxes = [list(sorted(map(int, line.split("x")))) for line in open("input.txt").readlines()]

# Assumes l is smallest side
def required_wrapping_paper(l, w, h):
    surface_area = 2*l*w + 2*w*h + 2*h*l
    slack = l * w
    return surface_area + slack

def part_one(boxes):
    return sum(required_wrapping_paper(l, w, h) for l, w, h in boxes)


# Sides are sorted smallest to largest
def required_ribbon(l, w, h):
    short_perimeter = 2*l + 2*w
    volume = l * w * h
    return short_perimeter + volume

def part_two(boxes):
    return sum(required_ribbon(l, w, h) for l, w, h in boxes)


print("Part one:", part_one(boxes))
print("Part two:", part_two(boxes))
