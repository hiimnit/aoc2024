import sys

if len(sys.argv) != 2:
    print("provide file name")
    exit(1)


with open(sys.argv[1], mode="r") as in_file:
    input = in_file.read().rstrip()


blocks = input.split("\n\n")
if len(blocks) != 2:
    exit(1)


def find_robot(map: list[list[str]]):
    for row, line in enumerate(map):
        for col, char in enumerate(line):
            if char == "@":
                return (row, col)
    raise Exception("Robot not found")


p1_map = [[char for char in line] for line in blocks[0].split("\n")]
instructions = blocks[1].replace("\n", "")

p2_map = []
for p1_line in p1_map:
    p2_line = []
    for char in p1_line:
        match char:
            case "#":
                p2_line.append("#")
                p2_line.append("#")
            case ".":
                p2_line.append(".")
                p2_line.append(".")
            case "O":
                p2_line.append("[")
                p2_line.append("]")
            case "@":
                p2_line.append("@")
                p2_line.append(".")

    p2_map.append(p2_line)

robot = find_robot(p1_map)


def p1_push(
    map: list[list[str]], position: tuple[int, int], direction: tuple[int, int]
) -> tuple[int, int] | None:
    next_position = (position[0] + direction[0], position[1] + direction[1])
    char = map[next_position[0]][next_position[1]]

    if char == "#":
        return None

    can_push = False

    if char == "O":
        can_push = p1_push(map, next_position, direction)
    elif char == ".":
        can_push = True

    if can_push:
        map[next_position[0]][next_position[1]], map[position[0]][position[1]] = (
            map[position[0]][position[1]],
            map[next_position[0]][next_position[1]],
        )
        return next_position

    return None


for instruction in instructions:
    position = robot
    match instruction:
        case "^":
            position = p1_push(p1_map, position, (-1, 0))
        case ">":
            position = p1_push(p1_map, position, (0, 1))
        case "v":
            position = p1_push(p1_map, position, (1, 0))
        case "<":
            position = p1_push(p1_map, position, (0, -1))

    if position is not None:
        robot = position

for line in p1_map:
    print("".join(line))

p1_result = 0

for row, line in enumerate(p1_map):
    for col, char in enumerate(line):
        if char == "O":
            p1_result += 100 * row + col

print("p1:", p1_result)

robot = find_robot(p2_map)


def p2_can_push(
    map: list[list[str]], position: tuple[int, int], direction: tuple[int, int]
) -> bool:
    next_position = (position[0] + direction[0], position[1] + direction[1])
    char = map[next_position[0]][next_position[1]]

    match char:
        case "[":
            match direction:
                case (-1, 0) | (1, 0):
                    return p2_can_push(map, next_position, direction) and p2_can_push(
                        map, (next_position[0], next_position[1] + 1), direction
                    )
                case (0, 1):
                    return p2_can_push(
                        map, (next_position[0], next_position[1] + 1), direction
                    )
                case (0, -1):
                    raise Exception("Should be unreachable.")
        case "]":
            match direction:
                case (-1, 0) | (1, 0):
                    return p2_can_push(map, next_position, direction) and p2_can_push(
                        map, (next_position[0], next_position[1] - 1), direction
                    )
                case (0, 1):
                    raise Exception("Should be unreachable.")
                case (0, -1):
                    return p2_can_push(
                        map, (next_position[0], next_position[1] - 1), direction
                    )
        case ".":
            return True
        case "#":
            return False

    raise Exception("Should be unreachable.")


def swap(map: list[list[str]], a: tuple[int, int], b: tuple[int, int]):
    map[b[0]][b[1]], map[a[0]][a[1]] = map[a[0]][a[1]], map[b[0]][b[1]]


def p2_push(
    map: list[list[str]], position: tuple[int, int], direction: tuple[int, int]
):
    next_position = (position[0] + direction[0], position[1] + direction[1])
    char = map[next_position[0]][next_position[1]]

    match char:
        case "[":
            match direction:
                case (-1, 0) | (1, 0):
                    p2_push(map, next_position, direction)
                    p2_push(map, (next_position[0], next_position[1] + 1), direction)
                case (0, 1):
                    p2_push(map, (next_position[0], next_position[1] + 1), direction)
                    swap(map, next_position, (next_position[0], next_position[1] + 1))
                case (0, -1):
                    raise Exception("Should be unreachable.")
        case "]":
            match direction:
                case (-1, 0) | (1, 0):
                    p2_push(map, next_position, direction)
                    p2_push(map, (next_position[0], next_position[1] - 1), direction)
                case (0, 1):
                    raise Exception("Should be unreachable.")
                case (0, -1):
                    p2_push(map, (next_position[0], next_position[1] - 1), direction)
                    swap(map, next_position, (next_position[0], next_position[1] - 1))

    swap(map, position, next_position)


for instruction in instructions:
    direction: tuple[int, int] = (0, 0)
    match instruction:
        case "^":
            direction = (-1, 0)
        case ">":
            direction = (0, 1)
        case "v":
            direction = (1, 0)
        case "<":
            direction = (0, -1)
        case _:
            raise Exception("Should be unreachable.")

    can_push = p2_can_push(p2_map, robot, direction)
    if not can_push:
        continue

    p2_push(p2_map, robot, direction)

    robot = (robot[0] + direction[0], robot[1] + direction[1])

for line in p2_map:
    print("".join(line))

p2_result = 0

for row, line in enumerate(p2_map):
    for col, char in enumerate(line):
        if char == "[":
            p2_result += 100 * row + col

print("p2:", p2_result)
