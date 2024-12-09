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

line = list(map(int, [c for c in lines[0]]))
p1_result = 0

line_i_start = 0
line_i_end = len(line) - 1
data_i = 0
data_length = sum(line)
in_file = True
start_file = None
end_file = None
free_space = 0

while data_i < data_length:
    if in_file:
        if start_file is None:
            start_file = (line_i_start // 2, line[line_i_start], 0)

        file_id, file_length, file_i = start_file
        if file_i < file_length:
            p1_result += data_i * file_id
            data_i += 1

        file_i += 1
        if file_i >= file_length:
            start_file = None
            in_file = False

            line_i_start += 1
            free_space = line[line_i_start]
            line_i_start += 1
        else:
            start_file = (file_id, file_length, file_i)
    else:
        if free_space <= 0:
            in_file = True
            continue

        if end_file is None:
            end_file = (line_i_end // 2, line[line_i_end], line[line_i_end] - 1)

        file_id, file_length, file_i = end_file
        if file_i >= 0:
            p1_result += data_i * file_id
            data_i += 1
            data_length -= 1

        file_i -= 1
        if file_i < 0:
            end_file = None

            line_i_end -= 1
            # decrement length of free space
            data_length -= line[line_i_end]
            line_i_end -= 1
        else:
            end_file = (file_id, file_length, file_i)

        free_space -= 1

print("p1:", p1_result)


free_spaces = []
data_i = 0
for i, e in enumerate(line):
    if i % 2 == 1:
        free_spaces.append((data_i, line[i]))
    data_i += line[i]

files = []

line_i = len(line) - 1
data_length = sum(line)
data_i = data_length
while line_i >= 0:
    file_length = line[line_i]

    if line_i % 2 == 1:
        data_i -= file_length
        line_i -= 1
        continue

    file_id = line_i // 2

    i = 0
    found = False
    for i, free_space in enumerate(free_spaces):
        free_space_i, free_space_length = free_space
        if free_space_length < file_length:
            continue
        if free_space_i > data_i:
            break

        files.append((free_space_i, file_id, file_length))
        if free_space_length == file_length:
            del free_spaces[i]
        else:
            free_spaces[i] = (
                free_space_i + file_length,
                free_space_length - file_length,
            )

        found = True
        break

    data_i -= file_length

    if not found:
        files.append((data_i, file_id, file_length))

    line_i -= 1

p2_result = 0

for data_i, file_id, file_length in files:
    for i in range(data_i, data_i + file_length):
        p2_result += i * file_id

print("p2:", p2_result)
