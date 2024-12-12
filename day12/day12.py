import sys
from typing import Set
from enum import Enum
from collections import defaultdict

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


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


bounds = (len(lines), len(lines[0]))

visited: Set[tuple[int, int]] = set()


def in_bounds(row: int, col: int):
    return row >= 0 and col >= 0 and row < bounds[0] and col < bounds[1]


def solve(row: int, col: int):
    char = lines[row][col]
    queue = [(row, col)]

    edges = []
    fields = []

    while len(queue) > 0:
        next = queue.pop()

        if next in visited:
            continue

        visited.add(next)
        fields.append(next)

        row, col = next

        if not in_bounds(row - 1, col) or lines[row - 1][col] != char:
            edges.append((row, col, Direction.UP))
        else:
            queue.append((row - 1, col))
        if not in_bounds(row, col + 1) or lines[row][col + 1] != char:
            edges.append((row, col, Direction.RIGHT))
        else:
            queue.append((row, col + 1))
        if not in_bounds(row + 1, col) or lines[row + 1][col] != char:
            edges.append((row, col, Direction.DOWN))
        else:
            queue.append((row + 1, col))
        if not in_bounds(row, col - 1) or lines[row][col - 1] != char:
            edges.append((row, col, Direction.LEFT))
        else:
            queue.append((row, col - 1))

    return (fields, edges)


p1_result = 0

plots = []

for row in range(bounds[0]):
    for col in range(bounds[1]):
        if (row, col) in visited:
            continue

        fields, edges = solve(row, col)
        p1_result += len(fields) * len(edges)

        plots.append((fields, edges))

print("p1:", p1_result)


def merge_edges(edges: list[tuple[int, int, Direction]]):
    grouped = defaultdict(list)

    for row, col, direction in edges:
        match direction:
            case Direction.UP:
                grouped[(direction, row)].append(col)
            case Direction.RIGHT:
                grouped[(direction, col)].append(row)
            case Direction.DOWN:
                grouped[(direction, row)].append(col)
            case Direction.LEFT:
                grouped[(direction, col)].append(row)

    result = 0

    for positions in grouped.values():
        positions.sort()

        result += 1

        for a, b in zip(positions, positions[1:]):
            if a != b - 1:
                result += 1

    return result


p2_result = 0

for fields, edges in plots:
    p2_result += len(fields) * merge_edges(edges)

print("p2:", p2_result)
