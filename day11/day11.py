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

line = list(map(int, lines[0].split(" ")))

mem: dict[int, dict[int, int]] = {}


def solve(number: int, depth: int) -> int:
    if depth == 0:
        return 1

    depth_mem = mem.get(depth)
    if depth_mem is not None:
        result = depth_mem.get(number)
        if result is not None:
            return result

    result = calc(number, depth)

    depth_mem = mem.get(depth)
    if depth_mem is not None:
        depth_mem[number] = result
    else:
        mem[depth] = {number: result}

    return result


def calc(number: int, depth: int) -> int:
    if number == 0:
        return solve(1, depth - 1)

    formatted = str(number)
    if len(formatted) % 2 == 0:
        left = int(formatted[: len(formatted) // 2])
        right = int(formatted[len(formatted) // 2 :])
        return solve(left, depth - 1) + solve(right, depth - 1)

    return solve(number * 2024, depth - 1)


p1_result = 0
p2_result = 0
for number in line:
    p1_result += solve(number, 25)
    p2_result += solve(number, 75)

print("p1:", p1_result)
print("p2:", p2_result)
