import argparse
import itertools
from collections import defaultdict


def read_file(file_path: str) -> dict[str, set[str]]:
    graph: dict[str, set[str]] = defaultdict(set)
    with open(file_path, "r", encoding="UTF-8") as file:
        line = file.readline()
        while line:
            a, b = line.strip().split("-")
            graph[a].add(b)
            graph[b].add(a)
            line = file.readline()

    return graph


def part_1(file_path: str):
    graph = read_file(file_path)

    visited: set[str] = set()
    triples: set[tuple[str, str, str]] = set()
    for vertex in graph.keys():
        if vertex in visited:
            continue

        stack: list[str] = [vertex]
        while stack:
            vertex = stack.pop()
            if vertex in visited:
                continue
            visited.add(vertex)

            for neighbor in graph[vertex]:
                for neighbors_neigbor in graph[neighbor]:
                    if neighbors_neigbor in graph[vertex]:
                        triples.add(
                            tuple(sorted([vertex, neighbor, neighbors_neigbor]))
                        )
                stack.append(neighbor)

    print(
        len({x for x in triples if x[0][0] == "t" or x[1][0] == "t" or x[2][0] == "t"})
    )


def part_2(file_path: str):
    graph = read_file(file_path)

    visited: set[str] = set()
    components: set[frozenset[str]] = set()
    for vertex in graph.keys():
        if vertex in visited:
            continue

        stack: list[str] = [vertex]
        while stack:
            vertex = stack.pop()
            if vertex in visited:
                continue
            visited.add(vertex)

            powerset = itertools.chain.from_iterable(
                itertools.combinations(list(graph[vertex]), r)
                for r in range(1, len(graph[vertex]) + 1)
            )
            starting_set = {vertex}.union(graph[vertex])
            for set_group in powerset:
                set_copy = starting_set

                for neighbor in set_group:
                    set_copy = set_copy.intersection({neighbor}.union(graph[neighbor]))

                components.add(
                    frozenset(set_copy.intersection({vertex}.union(set_group)))
                )

            for neighbor in graph[vertex]:
                stack.append(neighbor)

    largest_component = max(components, key=len)

    print(",".join(sorted(largest_component)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("part", type=int)
    parser.add_argument("file_path", type=str)
    results = parser.parse_args()

    assert results.part in [1, 2]

    if results.part == 1:
        part_1(results.file_path)
    else:
        part_2(results.file_path)
