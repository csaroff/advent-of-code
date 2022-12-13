from math import prod

class Monkey:
    def __init__(self, items, operation, divisible_by, next_monkeys, reduce_worry):
        self.items = items
        self.operation = operation
        self.divisible_by = divisible_by
        self.next_monkeys = next_monkeys
        self.reduce_worry = reduce_worry
        self.total_inspected = 0

    def inspect(self):
        result = []
        for old in self.items:
            self.total_inspected += 1
            new = eval(self.operation)
            new = eval(self.reduce_worry)
            divisible = (new % self.divisible_by == 0)
            result.append((self.next_monkeys[1 - divisible], new))
        self.items = []
        return result

def monkey_business(rounds, reduce_worry=None):
    monkeys = []
    for monkey_config in open("input.txt").read().split("\n\n"):
        monkey_config = monkey_config.split("\n")
        items = list(map(int, monkey_config[1].split("Starting items: ")[1].split(", ")))
        operation = monkey_config[2].split("Operation: new = ")[1]
        divisible_by = int(monkey_config[3].split("Test: divisible by ")[1])
        true_next = int(monkey_config[4].split("If true: throw to monkey ")[1])
        false_next = int(monkey_config[5].split("If false: throw to monkey ")[1])
        monkeys.append(Monkey(items, operation, divisible_by, [true_next, false_next], reduce_worry=reduce_worry))

    if reduce_worry is None:
        product = prod([monkey.divisible_by for monkey in monkeys])
        for monkey in monkeys:
            monkey.reduce_worry = f"new % {product}"

    for round in range(rounds):
        for monkey in monkeys:
            for idx, worry in monkey.inspect():
                monkeys[idx].items.append(worry)

    first, second = list(sorted([monkey.total_inspected for monkey in monkeys]))[-2:]
    return first * second

print("Monkey business:", monkey_business(20, reduce_worry="new // 3"))
print("Monkey business:", monkey_business(10000))
