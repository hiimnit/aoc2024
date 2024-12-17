from enum import Enum
import sys

if len(sys.argv) != 2:
    print("provide file name")
    exit(1)

with open(sys.argv[1], mode="r") as in_file:
    input = in_file.read().rstrip()


class Instruction(Enum):
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7


class Register(Enum):
    A = 0
    B = 1
    C = 2


input = input.split("\n")
if len(input) != 5:
    exit(1)

registers = []

for line in input[:3]:
    registers.append(int(line.split(" ")[-1]))

instructions = list(map(int, input[4].split(" ")[-1].split(",")))


def combo(registers: list[int], operand: int):
    if operand < 4:
        return operand
    if operand < 7:
        return registers[operand - 4]
    raise Exception("Invalid operand", operand)


def run(registers: list[int]):
    output = []
    pointer = 0

    while pointer < len(instructions):
        instruction, operand = instructions[pointer], instructions[pointer + 1]
        # print(Instruction(instruction), operand)

        match instruction:
            case Instruction.ADV.value:
                numerator = registers[Register.A.value]
                denominator = 2 ** combo(registers, operand)
                registers[Register.A.value] = numerator // denominator
            case Instruction.BXL.value:
                registers[Register.B.value] = registers[Register.B.value] ^ operand
            case Instruction.BST.value:
                registers[Register.B.value] = combo(registers, operand) % 8
            case Instruction.JNZ.value:
                if registers[Register.A.value] != 0:
                    pointer = operand - 2
            case Instruction.BXC.value:
                registers[Register.B.value] = (
                    registers[Register.B.value] ^ registers[Register.C.value]
                )
            case Instruction.OUT.value:
                output.append(combo(registers, operand) % 8)
            case Instruction.BDV.value:
                numerator = registers[Register.A.value]
                denominator = 2 ** combo(registers, operand)
                registers[Register.B.value] = numerator // denominator
            case Instruction.CDV.value:
                numerator = registers[Register.A.value]
                denominator = 2 ** combo(registers, operand)
                registers[Register.C.value] = numerator // denominator
            case _:
                raise Exception("Unexpected instruction", instruction)

        pointer += 2

    return output


p1_result = run(list(registers))

print("p1:", ",".join(map(str, p1_result)))


def get_possible_as(number: list[int | None], offset: int) -> list[list[int | None]]:
    if offset >= len(number):
        return [list(number)]

    d0, d1, d2 = (
        number[offset + 0],
        number[offset + 1] if offset + 1 < len(number) else None,
        number[offset + 2] if offset + 2 < len(number) else None,
    )

    numbers = []

    for i in range(0, 8):
        if d0 is not None and d0 != i & 1:
            continue
        if d1 is not None and d1 != (i & 2) >> 1:
            continue
        if d2 is not None and d2 != (i & 4) >> 2:
            continue

        copy = list(number)
        copy[offset + 0] = i & 1
        if offset + 1 < len(copy):
            copy[offset + 1] = (i & 2) >> 1
        if offset + 2 < len(copy):
            copy[offset + 2] = (i & 4) >> 2

        numbers.append(copy)

    return numbers


def get_a(number: list[int | None], offset: int) -> int:
    return (
        get_checked(number, offset + 0)
        + get_checked(number, offset + 1) * 2
        + get_checked(number, offset + 2) * 4
    )


def get_checked(number: list[int | None], offset: int) -> int:
    if offset >= len(number):
        return 0
    return number[offset]


def min_or_none(a: int | None, b: int | None) -> int | None:
    if a is None:
        return b
    if b is None:
        return a
    if a < b:
        return a
    return b


def test(program: list[int], number: list[int | None], offset: int) -> int | None:
    if offset >= len(program):
        result = 0
        for i, e in enumerate(number):
            result += 2**i * e
        return result

    result = None

    possibilities = get_possible_as(number, offset * 3)
    for possibility in possibilities:
        b = get_a(possibility, offset * 3)
        b = b ^ 0b001

        possible_cs = get_possible_as(possibility, offset * 3 + b)
        for possible_c in possible_cs:
            c = get_a(possible_c, offset * 3 + b) & 0b111
            b_x = b ^ 0b101
            b_x = b_x ^ c

            if b_x != program[offset]:
                continue

            result = min_or_none(result, test(program, possible_c, offset + 1))

    return result


p2_result = test(instructions, [None for _ in range(48)], 0)
print("p2:", p2_result)

registers[Register.A.value] = p2_result
print("program:", ",".join(map(str, run(registers))))
print("output :", ",".join(map(str, instructions)))
