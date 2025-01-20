import argparse
from functools import cmp_to_key


def read_file(file_path: str) -> tuple[list[tuple[int, int]], list[list[int]]]:
    with open(file_path, "r", encoding="UTF-8") as file:
        lines = file.readlines()

    relations: list[tuple[int, int]] = []
    orders: list[list[int]] = []
    on_relations = True
    for line in lines:
        if on_relations:
            if line == "\n":
                on_relations = False
                continue
            pair = tuple(int(x) for x in line.split("|"))
            assert len(pair) == 2
            relations.append(pair)
        else:
            orders.append([int(x) for x in line.split(",")])

    return relations, orders


def create_relation_graph(relations: list[tuple[int, int]]) -> dict[int, list[int]]:
    graph: dict[int, list[int]] = {}

    for edge in relations:
        start, end = edge
        if start in graph:
            if end not in graph[start]:
                graph[start].append(end)
        else:
            graph[start] = [end]

        if end not in graph:
            graph[end] = []

    return graph


def get_followers(graph: dict[int, list[int]]) -> dict[int, list[int]]:
    followers: dict[int, list[int]] = {}

    def get_followers_helper(
        vertex: int, graph: dict[int, list[int]], followers: dict[int, list[int]]
    ):
        # Already visited
        if vertex in followers:
            return

        # No neighbors
        if not graph[vertex]:
            followers[vertex] = []
            return

        # Followers are neighbors and their followers
        followers[vertex] = graph[vertex].copy()
        for neighbor in graph[vertex]:
            get_followers_helper(neighbor, graph, followers)
            followers[vertex] += followers[neighbor]

        followers[vertex] = list(set(followers[vertex]))

    for vertex in graph:
        get_followers_helper(vertex, graph, followers)

    return followers


def sum_middles_of_valid_orders(
    orders: list[list[int]], followers: dict[int, list[int]]
) -> int:
    running_sum = 0
    for order in orders:
        valid = True
        for index, preceding_page in enumerate(order):
            for following_page in order[index + 1 :]:
                if preceding_page in followers[following_page]:
                    valid = False
                    break
            if not valid:
                break

        if valid:
            middle = len(order) // 2
            running_sum += order[middle]

    return running_sum


def part_1(file_path: str):
    relations, orders = read_file(file_path)
    graph = create_relation_graph(relations)
    output = sum_middles_of_valid_orders(orders, graph)
    print(output)


def sum_middles_of_fixed_orders(
    orders: list[list[int]], followers: dict[int, list[int]]
) -> int:
    def comparison(a, b):
        if b in followers[a]:
            return -1

        return 1

    running_sum = 0
    for order in orders:
        valid = True
        for index, preceding_page in enumerate(order):
            for following_page in order[index + 1 :]:
                if preceding_page in followers[following_page]:
                    valid = False
                    break
            if not valid:
                break

        if not valid:
            fixed = sorted(order, key=cmp_to_key(comparison))
            middle = len(order) // 2
            running_sum += fixed[middle]

    return running_sum


def part_2(file_path: str):
    relations, orders = read_file(file_path)
    graph = create_relation_graph(relations)
    output = sum_middles_of_fixed_orders(orders, graph)
    print(output)


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
