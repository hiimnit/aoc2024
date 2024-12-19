import sys
from functools import cache

if len(sys.argv) != 2:
    print("provide file name")
    exit(1)

with open(sys.argv[1], mode="r") as in_file:
    input = in_file.read().rstrip()

patterns, towels = input.split("\n\n")
patterns = patterns.split(", ")
towels = towels.split("\n")


@cache
def match_patterns(towel: str, offset: int) -> int:
    if offset >= len(towel):
        return 1

    total = 0

    for pattern in patterns:
        if towel[offset : offset + len(pattern)] == pattern:
            total += match_patterns(towel, offset + len(pattern))

    return total


p1_result = 0
p2_result = 0

for towel in towels:
    count = match_patterns(towel, 0)
    if count > 0:
        p1_result += 1
    p2_result += count

print("p1:", p1_result)
print("p2:", p2_result)
