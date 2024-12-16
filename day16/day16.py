from collections import defaultdict
import sys
from enum import Enum
import heapq


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


vectors = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1),
]

if len(sys.argv) != 2:
    print("provide file name")
    exit(1)


with open(sys.argv[1], mode="r") as in_file:
    input = in_file.read().rstrip()


def find_char(map: list[list[str]], char: str) -> tuple[int, int] | None:
    for row, line in enumerate(map):
        for col, c in enumerate(line):
            if c == char:
                return (row, col)
    return None


map = [[char for char in line] for line in input.split("\n")]

start_position = find_char(map, "S")
if start_position is None:
    print("Start not found")
    exit(1)

end_position = find_char(map, "E")
if end_position is None:
    print("End not found")
    exit(1)


def dijkstra(
    map: list[list[str]], start_position: tuple[int, int], start_direction: Direction
) -> int | None:
    queue: list[tuple[int, tuple[int, int], Direction]] = [
        (0, start_position, start_direction)
    ]

    positions: dict[tuple[int, int], int | None] = defaultdict(lambda: None)

    while len(queue) > 0:
        score, position, direction = heapq.heappop(queue)

        for next_direction in Direction:
            vector = vectors[next_direction.value]
            next_position = (position[0] + vector[0], position[1] + vector[1])

            next_char = map[next_position[0]][next_position[1]]

            if next_char == "#":
                continue

            next_score = score + 1
            if next_direction != direction:
                # TODO not precise
                next_score += 1000

            if next_char == "E":
                return next_score

            if next_position == (11, 3):
                print(next_position, next_score, next_direction)

            current_best = positions[next_position]
            if current_best == next_score:
                print("same found at", next_position, "score", next_score)
            if current_best is None or current_best > next_score:
                heapq.heappush(queue, (next_score, next_position, next_direction))
                positions[next_position] = next_score

    return None


p1_result = dijkstra(map, start_position, Direction.RIGHT)
print("p1", p1_result)


def is_intersection(
    map: list[list[str]], position: tuple[int, int], direction: Direction
) -> bool:
    for i in [-1, 1]:
        next_direction = Direction((direction.value + i) % 4)
        next_char = map[position[0] + vectors[next_direction.value][0]][
            position[1] + vectors[next_direction.value][1]
        ]

        if next_char == ".":
            return True

    return False


def convert_to_graph(map: list[list[str]], start_position: tuple[int, int]):
    graph = dict()

    queue = [start_position]

    while len(queue) > 0:
        position = queue.pop()
        if position in graph:
            continue

        nodes: list[tuple[int, tuple[int, int]]] = []

        for direction in Direction:
            vector = vectors[direction.value]
            next_position = (position[0] + vector[0], position[1] + vector[1])
            length = 1

            while True:
                char = map[next_position[0]][next_position[1]]
                if char == "#":
                    break

                if is_intersection(map, next_position, direction) or char == "E":
                    nodes.append((length, next_position))
                    queue.append(next_position)

                next_position = (
                    next_position[0] + vector[0],
                    next_position[1] + vector[1],
                )
                length += 1

        graph[position] = nodes

    return graph


def dijkstra_graph(
    map: dict[tuple[int, int], list[tuple[int, tuple[int, int]]]],
    start_position: tuple[int, int],
) -> tuple[
    dict[tuple[int, int], int | None], dict[tuple[int, int], set[tuple[int, int]]]
]:
    queue: list[tuple[int, tuple[int, int]]] = [(0, start_position)]

    positions: dict[tuple[int, int], int | None] = defaultdict(lambda: None)
    from_positions: dict[tuple[int, int], set[tuple[int, int]]] = defaultdict(set)

    while len(queue) > 0:
        score, position = heapq.heappop(queue)

        for length, next_position in map[position]:
            next_score = score + 1000 + length
            # special case when we start moving in the starting direction
            if position == start_position and next_position[0] == position[0]:
                next_score -= 1000

            current_best = positions[next_position]
            if current_best is None or current_best >= next_score:
                if current_best is not None and current_best > next_score:
                    from_positions[next_position] = set()

                heapq.heappush(queue, (next_score, next_position))
                positions[next_position] = next_score

                from_positions[next_position].add(position)

    return (positions, from_positions)


graph = convert_to_graph(map, start_position)
positions, from_positions = dijkstra_graph(graph, start_position)

p1_result = positions[end_position]
print("p1", p1_result)

visited: set[tuple[int, int]] = set()

queue = [end_position]
while len(queue) > 0:
    position = queue.pop()
    for previous_position in from_positions[position]:
        if previous_position[0] == position[0]:
            row = position[0]
            for col in range(
                min(previous_position[1], position[1]),
                max(previous_position[1], position[1]) + 1,
            ):
                visited.add((row, col))
                map[row][col] = "O"
        else:
            col = position[1]
            for row in range(
                min(previous_position[0], position[0]),
                max(previous_position[0], position[0]) + 1,
            ):
                visited.add((row, col))
                map[row][col] = "O"

        if previous_position != start_position:
            queue.append(previous_position)

for line in map:
    print("".join(line))

print("p2:", len(visited))
