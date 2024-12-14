from functools import reduce
import re
import sys

if len(sys.argv) != 4:
    print("provide file name")
    exit(1)


with open(sys.argv[1], mode="r") as in_file:
    lines = list(map(lambda line: line.strip(), in_file.readlines()))

height = int(sys.argv[2])
width = int(sys.argv[3])

robots: list[tuple[int, int, int, int]] = []

for line in lines:
    match = re.match(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", line)
    if match is None:
        exit(1)

    robots.append(
        (
            int(match.group(1)),
            int(match.group(2)),
            int(match.group(3)),
            int(match.group(4)),
        )
    )

positions = []
for x, y, vx, vy in robots:
    final_position = ((x + vx * 100) % width, (y + vy * 100) % height)
    positions.append(final_position)


p1_result = [0, 0, 0, 0]

for x, y in positions:
    if x < width // 2 and y < height // 2:
        p1_result[0] += 1
    elif x > width // 2 and y < height // 2:
        p1_result[1] += 1
    elif x < width // 2 and y > height // 2:
        p1_result[2] += 1
    elif x > width // 2 and y > height // 2:
        p1_result[3] += 1

print("p1:", reduce(lambda a, b: a * b, p1_result))


def pretty_print(positions: set[tuple[int, int]]):
    for row in range(height):
        line = []
        for col in range(width):
            if (col, row) in positions:
                line.append("█")
            else:
                line.append(" ")
        print("".join(line))


p2_result = 0

i = 98

while True:
    p2_result += i

    robots = [
        ((x + vx * i) % width, (y + vy * i) % height, vx, vy) for x, y, vx, vy in robots
    ]
    print("p2:", p2_result)
    pretty_print(set((x, y) for x, y, _, _ in robots))

    i = 103

    if input() == "q":
        break
