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


rows = len(lines)
cols = len(lines[0])


def build_word(row: int, col: int, coords: list[tuple[int, int]]) -> str:
    return "".join(lines[row + r][col + c] for [r, c] in coords)


works = [
    ((range(rows), range(cols - 3)), [(0, 1), (0, 2), (0, 3)]),
    ((range(rows - 3), range(cols)), [(1, 0), (2, 0), (3, 0)]),
    ((range(rows - 3), range(cols - 3)), [(1, 1), (2, 2), (3, 3)]),
    ((range(rows - 3), range(3, cols)), [(1, -1), (2, -2), (3, -3)]),
]

p1_result = 0

for [[rows_range, cols_range], coords] in works:
    for row in rows_range:
        for col in cols_range:
            if lines[row][col] == "X":
                if build_word(row, col, coords) == "MAS":
                    p1_result += 1
            if lines[row][col] == "S":
                if build_word(row, col, coords) == "AMX":
                    p1_result += 1

print("p1:", p1_result)


p2_result = 0

for row in range(rows - 2):
    for col in range(cols - 2):
        w1 = build_word(row, col, [(0, 0), (1, 1), (2, 2)])
        if w1 != "MAS" and w1 != "SAM":
            continue

        w2 = build_word(row, col, [(0, 2), (1, 1), (2, 0)])
        if w2 != "MAS" and w2 != "SAM":
            continue

        p2_result += 1

print("p2:", p2_result)
