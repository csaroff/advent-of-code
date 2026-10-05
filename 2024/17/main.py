class Computer:
    def __init__(self, program, register_a=0, register_b=0, register_c=0):
        self.opcode_to_method = [self.adv, self.bxl, self.bst, self.jnz, self.bxc, self.out, self.bdv, self.cdv]
        self.program = program
        self.pointer = 0
        self.register_a=register_a
        self.register_b=register_b
        self.register_c=register_c
        self.output = []

    def reinit(self, register_a=0):
        self.pointer = 0
        self.register_a=register_a
        self.output = []

    def combo(self, operand):
        if 0 <= operand <= 3:
            return operand
        elif operand == 4:
            return self.register_a
        elif operand == 5:
            return self.register_b
        elif operand == 6:
            return self.register_c
        else:
            raise ValueError(f"Illegal Combo Operand {operand}")

    def adv(self, operand):
        self.register_a = self.register_a // (2 ** self.combo(operand))

    def bxl(self, operand):
        self.register_b = self.register_b ^ operand

    def bst(self, operand):
        self.register_b = self.combo(operand) % 8

    def jnz(self, operand):
        if self.register_a == 0:
            return
        self.pointer = operand

    def bxc(self, operand):
        self.register_b = self.register_b ^ self.register_c

    def out(self, operand):
        return self.combo(operand) % 8

    def bdv(self, operand):
        self.register_b = self.register_a // (2 ** self.combo(operand))

    def cdv(self, operand):
        self.register_c = self.register_a // (2 ** self.combo(operand))

    def tick(self):
        opcode = self.program[self.pointer]
        operand = self.program[self.pointer+1]
        op = self.opcode_to_method[opcode]
        self.pointer = self.pointer + 2
        result = op(operand)
        if result is not None:
            self.output.append(result)

    def run_program(self, early_halt=lambda computer: False):
        while self.pointer < len(self.program) and not early_halt(self):
            self.tick()
        return self.output, self.register_a, self.register_b, self.register_c

    def parse_text_input(text_input):
        registers_str, program_str = text_input.strip().split("\n\n")
        registers = [int(register_str.split(": ")[-1].strip()) for register_str in registers_str.split("\n")]
        program = list(map(int, program_str.split(": ")[-1].strip().split(",")))
        return (program, *registers)


class FastComputer:
    def __init__(self, program, register_a=0, register_b=0, register_c=0):
        # Convert program to bytes for faster access
        self.program = bytes(program)
        self.pointer = 0
        self.register_a = register_a
        self.register_b = register_b
        self.register_c = register_c
        # Pre-allocate output list with estimated size
        self.output = []

    def reinit(self, register_a=0):
        # No need to convert program again since it's already bytes
        self.pointer = 0
        self.register_a = register_a
        self.output = []

    def combo(self, operand):
        # Replace if/elif chain with faster lookup table
        if operand <= 3:
            return operand
        return (self.register_a, self.register_b, self.register_c)[operand - 4]

    def tick(self):
        opcode = self.program[self.pointer]
        operand = self.program[self.pointer+1]
        self.pointer = self.pointer + 2

        match opcode:
            case 0:
                self.register_a = self.register_a >> self.combo(operand)
            case 1:
                self.register_b = self.register_b ^ operand
            case 2:
                self.register_b = self.combo(operand) & 7
            case 3:
                if self.register_a != 0: self.pointer = operand
            case 4:
                self.register_b = self.register_b ^ self.register_c
            case 5:
                self.output.append(self.combo(operand) % 8)
            case 6:
                self.register_b = self.register_a // (2 ** self.combo(operand))
            case 7:
                self.register_c = self.register_a // (2 ** self.combo(operand))

    def run_program(self, early_halt=lambda computer: False):
        while self.pointer < len(self.program) and not early_halt(self):
            self.tick()
        return self.output, self.register_a, self.register_b, self.register_c

    def parse_text_input(text_input):
        registers_str, program_str = text_input.strip().split("\n\n")
        registers = [int(register_str.split(": ")[-1].strip()) for register_str in registers_str.split("\n")]
        program = list(map(int, program_str.split(": ")[-1].strip().split(",")))
        return (program, *registers)


out, a, b, c = FastComputer([2, 6], register_c=9).run_program()
assert b == 1, f"Expected register b to equal 1, but got {b}"

out, a, b, c = FastComputer([5, 0, 5, 1, 5, 4], register_a=10).run_program()
assert out == [0, 1, 2], f"Expected output to equal [0, 1, 2], but got {out}"

out, a, b, c = FastComputer([0, 1, 5, 4, 3, 0], register_a=2024).run_program()
assert out == [4,2,5,6,7,7,7,7,3,1,0], f"Expected output to equal [4,2,5,6,7,7,7,7,3,1,0], but got {out}"
assert a == 0, f"Expected register a to equal 0, but got {a}"

out, a, b, c = FastComputer([1, 7], register_b=29).run_program()
assert b == 26, f"Expected register b to equal 26, but got {b}"

out, a, b, c = FastComputer([4, 0], register_b=2024, register_c=43690).run_program()
assert b == 44354, f"Expected register b to equal 44354, but got {b}"

def part1(text_input):
    out, a, b, c = FastComputer(*FastComputer.parse_text_input(text_input)).run_program()
    return ",".join(map(str, out))

def part2(program, debug=False):
    a = -1
    output = None

    def early_halt(computer):
        return computer.output != program[:len(computer.output)] or len(computer.output) > len(program)

    computer = FastComputer(program, register_a=a)

    while program != output:
        if debug and a % 10000 == 0:
            print(f"Testing register a={a}")
        a += 1
        computer.reinit(register_a=a)
        output, *_ = computer.run_program(early_halt=early_halt)

    return a

# The program from our puzzle input has unique properties.
# Here it is in a more readable format:
# 2,4, # register B = register A & 7 (Keep last 3 bits)
# 1,1, # register B = register B XOR 1
# 7,5, # register C = self.register_a // (2 ** register B)
# 1,5, # register B = register B XOR 5
# 4,2, # register B = register B XOR register C
# 5,5, # print register B % 8
# 0,3, # register A = register A // 8
# 3,0  # if register A != 0: self.pointer = 0
#
# This can be rewritten as set of three instructions that does not utilize registers B or C:
# print((((A & 7) ^ 1) ^ 5) ^ (A // (2 ** (A & 7) ^ 1)) % 8) # print a value that's a function of register A.
# A = A >> 3 # Right shift by 3 bits(integer division by 8)
# if A != 0: self.pointer = 0 # GOTO first instruction unless A is 0
#
# Because we print and right-shift only once per iteration and because register A is unmodified outside of the right-shift,
# our starting register value must be by 3 bits * 16 iterations = 48 bits.
# Due to the iterated right-shifting, we also know that the final printed output value is only a function of the last 3 bits of the initial value in register A.
#
# We can work backwards from the final output value to the first 3 bits of the initial value of register A.
def part2_fast(program, debug=False):
    computer = FastComputer(program)
    valid_base_8_prefixes = [[]]

    for i in range(len(program)):
        valid_base_8_prefixes_next = []
        for valid_prefix in valid_base_8_prefixes:
            for j in range(0, 8):
                base_8_candidate = valid_prefix + [j] + [0] * (len(program) - len(valid_prefix) - 1)
                a = sum(digit * (8 ** (len(program) - 1 - idx)) for idx, digit in enumerate(base_8_candidate))
                computer.reinit(register_a=a)
                program_output, *_ = computer.run_program()
                if program_output[-(i + 1):] == program[-(i + 1):]:
                    valid_base_8_prefixes_next.append(valid_prefix + [j])
        valid_base_8_prefixes = valid_base_8_prefixes_next

    a_base_10_options = [sum(digit * (8 ** (len(program) - 1 - idx)) for idx, digit in enumerate(base_8_candidate)) for base_8_candidate in valid_base_8_prefixes]
    if debug:
        print("valid_base_8_prefixes", valid_base_8_prefixes)
        print("a_base_10_options", a_base_10_options)

    lowest_a = min(a_base_10_options)
    return lowest_a


test_input = """
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""

out, a, b, c = FastComputer(*FastComputer.parse_text_input(test_input)).run_program()
assert out == [4,6,3,5,6,3,5,2,1,0], f"Expected output to equal [4,6,3,5,6,3,5,2,1,0], but got {out}"

test_output = part1(test_input)
assert test_output == "4,6,3,5,6,3,5,2,1,0", f"Expected output to equal '4,6,3,5,6,3,5,2,1,0', but got {test_output}"

print("Part 1:", part1(open("input.txt").read()))

test_input = """
Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
"""

program, *registers = FastComputer.parse_text_input(test_input)
test_output = part2(program)
assert test_output == 117440, f"Expected output to equal 117440, but got {test_output}"

program = [2, 4, 1, 1, 7, 5, 1, 5, 4, 2, 5, 5, 0, 3, 3, 0]
p2_answer = part2_fast(program)

out, *registers = FastComputer(program, register_a=p2_answer).run_program()
assert out == program, f"Expected output to equal {program}, but got {out}"

print("Part 2:", p2_answer)

