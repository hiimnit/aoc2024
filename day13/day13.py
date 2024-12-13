import re
import sys

if len(sys.argv) != 2:
    print("provide file name")
    exit(1)


with open(sys.argv[1], mode="r") as in_file:
    input = in_file.read().rstrip()


blocks = input.split("\n\n")

lines: list[tuple[int, int, int, int, int, int]] = []

for block in blocks:
    a_line, b_line, prize_line = block.split("\n")

    a = re.match(r"Button A: X\+(\d+), Y\+(\d+)", a_line)
    if a is None:
        exit(1)
    b = re.match(r"Button B: X\+(\d+), Y\+(\d+)", b_line)
    if b is None:
        exit(1)
    prize = re.match(r"Prize: X=(\d+), Y=(\d+)", prize_line)
    if prize is None:
        exit(1)

    lines.append(
        (
            int(a.group(1)),
            int(a.group(2)),
            int(b.group(1)),
            int(b.group(2)),
            int(prize.group(1)),
            int(prize.group(2)),
        )
    )


def solve(xa: int, ya: int, xb: int, yb: int, xp: int, yp: int):
    m = (xa * yp - xp * ya) / (xa * yb - xb * ya)
    n = (xp - m * xb) / xa

    return (n, m)


p1_result = 0

for xa, ya, xb, yb, xp, yp in lines:
    n, m = solve(xa, ya, xb, yb, xp, yp)

    if n != int(n) or m != int(m):
        continue
    if n > 100 or m > 100:
        continue

    p1_result += 3 * n + m

print("p1:", int(p1_result))

p2_result = 0

for xa, ya, xb, yb, xp, yp in lines:
    n, m = solve(xa, ya, xb, yb, xp + 10000000000000, yp + 10000000000000)

    if n != int(n) or m != int(m):
        continue

    p2_result += 3 * n + m

print("p2:", int(p2_result))
