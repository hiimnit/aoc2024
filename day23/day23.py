from collections import defaultdict
import sys

if len(sys.argv) != 2:
    print("provide file name")
    exit(1)

with open(sys.argv[1], mode="r") as in_file:
    lines = in_file.read().rstrip()

edges: dict[str, list[str]] = defaultdict(list)
nodes: set[str] = set()

for line in lines.split("\n"):
    node1, node2 = line.split("-")

    edges[node1].append(node2)
    edges[node2].append(node1)

    nodes.add(node1)
    nodes.add(node2)


def find_loops(loop: list[str]):
    result = []

    if len(loop) == 3:
        for edge in edges[loop[-1]]:
            if edge == loop[0]:
                result.append(loop)
        return result

    for edge in edges[loop[-1]]:
        if edge in loop:
            continue
        result.extend(find_loops(loop + [edge]))

    return result


t_loops: set[tuple[str, str, str]] = set()

for node in nodes:
    t_loops.update(
        map(
            lambda loop: tuple(sorted(loop)),
            filter(
                lambda loop: any(e.startswith("t") for e in loop), find_loops([node])
            ),
        )
    )

print("p1:", len(t_loops))

tested = set()


def find_clusters(cluster: str):
    if cluster in tested:
        return []
    tested.add(cluster)

    result = [cluster]
    cluster_arr = cluster.split(",")

    for node in edges[cluster_arr[-1]]:
        back_links = edges[node]

        if not all(map(lambda e: e in back_links, cluster_arr)):
            continue

        next_cluster = ",".join(sorted(cluster_arr + [node]))
        result.extend(find_clusters(next_cluster))

    return result


clusters = set()

for node in nodes:
    clusters.update(find_clusters(node))

print("p2:", max(clusters, key=len))
