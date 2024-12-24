from collections import defaultdict
import sys

if len(sys.argv) != 2:
    print("provide file name")
    exit(1)

with open(sys.argv[1], mode="r") as in_file:
    input = in_file.read().rstrip()

wires_input, gates_input = input.split("\n\n")

wires: dict[str, int] = {}

for wire in wires_input.split("\n"):
    name, value = wire.split(": ")

    wires[name] = int(value)

gates = []
dependencies = defaultdict(list)

for gate in gates_input.split("\n"):
    w1, op, w2, arrow, w3 = gate.split(" ")

    gates.append((op, w1, w2, w3))

    dependencies[w3].append(w1)
    dependencies[w3].append(w2)

    # graphviz -> fdp
    print(f'{w1} -> {w3} [label="{op}"];')
    print(f'{w2} -> {w3} [label="{op}"];')


def get_level(wire: str):
    if len(dependencies[wire]) == 0:
        return 0

    return max(get_level(w) for w in dependencies[wire]) + 1


levels = defaultdict(list)

for gate in gates:
    op, w1, w2, w3 = gate
    levels[get_level(w3)].append(gate)

top_level = max(levels.keys())


def evaluate(op: str, w1: str, w2: str) -> int:
    match op:
        case "AND":
            return wires[w1] & wires[w2]
        case "OR":
            return wires[w1] | wires[w2]
        case "XOR":
            return wires[w1] ^ wires[w2]
        case _:
            raise Exception(f"Unknown operator {op}")


for level in range(1, top_level + 1):
    for op, w1, w2, w3 in levels[level]:
        wires[w3] = evaluate(op, w1, w2)

z_wires = sorted(filter(lambda e: e.startswith("z"), wires), reverse=True)
print("p1:", int("".join([str(wires[e]) for e in z_wires]), 2))


def expect(w1: str, w2: str, op: str, w3: str | None = None) -> str | None:
    for i, (gate_op, gate_w1, gate_w2, gate_w3) in enumerate(gates):
        if gate_op == op and (
            (gate_w1 == w1 and gate_w2 == w2) or (gate_w2 == w1 and gate_w1 == w2)
        ):
            if w3 is not None and w3 != gate_w3:
                print("swapping at:", w1, w2, op, w3, gate_w3)

                swap(gate_w3, w3)

                return w3

            return gate_w3

    return None


swaps = []


def swap(w1: str, w2: str):
    for i, gate in enumerate(gates):
        if gate[3] == w1:
            break
    else:
        raise Exception(f"Did not find {w1}")

    for j, gate in enumerate(gates):
        if j != i and gate[3] == w2:
            break
    else:
        raise Exception(f"Did not find {w2}")

    gates[i] = (gates[i][0], gates[i][1], gates[i][2], w2)
    gates[j] = (gates[j][0], gates[j][1], gates[j][2], w1)

    swaps.append(w1)
    swaps.append(w2)


expect("x00", "y00", "XOR", "z00")
carry = expect("x00", "y00", "AND")
if carry is None:
    print("first carry not found")
    exit(1)

for i in range(1, 43):
    x_y_xor = expect(f"x{i:02}", f"y{i:02}", "XOR")
    if x_y_xor is None:
        raise Exception("unrecoverable")
    expect(carry, x_y_xor, "XOR", f"z{i:02}")
    tmp_carry = expect(carry, x_y_xor, "AND")
    if tmp_carry is None:
        for gate in gates:
            if gate[0] == "AND" and (gate[1] == carry or gate[2] == carry):
                other = gate[1] if carry == gate[2] else gate[2]
                print("swapping", other, x_y_xor)

                swap(other, x_y_xor)
                x_y_xor = other
                tmp_carry = expect(carry, x_y_xor, "AND")
                break
        else:
            raise Exception(f"Did not find {carry} AND")

    x_y_and = expect(f"x{i:02}", f"y{i:02}", "AND")
    if x_y_and is None:
        raise Exception("unrecoverable")
    carry = expect(tmp_carry, x_y_and, "OR")
    if carry is None:
        raise Exception("unrecoverable")

print("p2:", ",".join(sorted(swaps)))
