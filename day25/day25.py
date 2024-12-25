import sys

if len(sys.argv) != 2:
    print("provide file name")
    exit(1)

with open(sys.argv[1], mode="r") as in_file:
    input = in_file.read().rstrip()

locks = []
keys = []

for block in input.split("\n\n"):
    lines = block.split("\n")

    heights = [
        len([line[col] for line in lines if line[col] == "#"]) - 1
        for col in range(len(lines[0]))
    ]

    if lines[0].startswith("#"):
        locks.append(heights)
    else:
        keys.append(heights)


def fits(lock: list[int], key: list[int]) -> bool:
    for p, k in zip(lock, key):
        if p + k > 5:
            return False
    return True


result = 0

for lock in locks:
    for key in keys:
        if fits(lock, key):
            result += 1

print("result:", result)
