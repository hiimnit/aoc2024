import sys

if len(sys.argv) != 2:
    print("provide file name")
    exit(1)


with open(sys.argv[1], mode="r") as in_file:
    lines = list(
        map(
            lambda s: s.strip(),
            in_file.readlines(),
        )
    )

equations: list[tuple[int, list[int]]] = []

for line in lines:
    first, rest = line.split(": ")
    first = int(first)
    rest = list(map(int, rest.split(" ")))

    equations.append((first, rest))


def solve_p1(result: int, value: int, index: int, numbers: list[int]) -> bool:
    if value == result and index == len(numbers):
        return True
    if value > result or index >= len(numbers):
        return False

    next = numbers[index]
    index += 1

    return solve_p1(result, value * next, index, numbers) or solve_p1(
        result, value + next, index, numbers
    )


def solve_p2(result: int, value: int, index: int, numbers: list[int]) -> bool:
    if value == result and index == len(numbers):
        return True
    if value > result or index >= len(numbers):
        return False

    next = numbers[index]
    index += 1

    return (
        solve_p2(result, value * next, index, numbers)
        or solve_p2(result, int(str(value) + str(next)), index, numbers)
        or solve_p2(result, value + next, index, numbers)
    )


p1_result = 0
p2_result = 0

for result, numbers in equations:
    if solve_p1(result, numbers[0], 1, numbers):
        p1_result += result
        p2_result += result
    elif solve_p2(result, numbers[0], 1, numbers):
        p2_result += result

print("p1:", p1_result)
print("p2:", p2_result)
