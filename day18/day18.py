from collections import defaultdict
import sys
import heapq

if len(sys.argv) != 4:
    print("provide file name and map_size and bytes_used")
    exit(1)

map_size = int(sys.argv[2])
bytes_used = int(sys.argv[3])

with open(sys.argv[1], mode="r") as in_file:
    input = in_file.read().rstrip()

input = list(map(lambda line: tuple(map(int, line.split(","))), input.split("\n")))


def h(position: tuple[int, int], map_size: int) -> int:
    return map_size - 1 - position[0] + map_size - 1 - position[1]


def dijkstra(bytes: set[tuple[int, int]], map_size: int) -> int | None:
    vectors = [
        (-1, 0),
        (0, 1),
        (1, 0),
        (0, -1),
    ]

    queue: list[tuple[int, int, tuple[int, int]]] = [(h((0, 0), map_size), 0, (0, 0))]

    positions: dict[tuple[int, int], int | None] = defaultdict(lambda: None)

    while len(queue) > 0:
        _, score, position = heapq.heappop(queue)

        for vector in vectors:
            next_position = (position[0] + vector[0], position[1] + vector[1])

            if (
                next_position[0] < 0
                or next_position[0] >= map_size
                or next_position[1] < 0
                or next_position[1] >= map_size
                or next_position in bytes
            ):
                continue

            next_score = score + 1

            if next_position == (map_size - 1, map_size - 1):
                return next_score

            current_best = positions[next_position]
            if current_best is None or current_best > next_score:
                heapq.heappush(
                    queue,
                    (
                        next_score + h(next_position, map_size),
                        next_score,
                        next_position,
                    ),
                )
                positions[next_position] = next_score

    return None


p1_result = dijkstra(set(input[:bytes_used]), map_size)
print("p1:", p1_result)

lower_bound = bytes_used + 1
upper_bound = len(input) - 1
while lower_bound <= upper_bound:
    mid = lower_bound + (upper_bound - lower_bound) // 2

    bytes = set(input[: mid + 1])
    if dijkstra(bytes, map_size) is None:
        upper_bound = mid - 1
    else:
        lower_bound = mid + 1

print("p2:", ",".join(map(str, input[lower_bound])))
