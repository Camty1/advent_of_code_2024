import argparse
from collections import defaultdict

import numpy as np


def read_file(
    file_path: str,
) -> np.ndarray:
    with open(file_path, "r", encoding="UTF-8") as file:
        lines = file.readlines()

    return np.array([[int(x) for x in line.strip()] for line in lines])


def read_map(
    map: np.ndarray,
) -> tuple[
    set[tuple[int, int]],
    set[tuple[int, int]],
    dict[tuple[int, int], set[tuple[int, int]]],
]:
    rows, cols = map.shape
    graph: dict[tuple[int, int], set[tuple[int, int]]] = defaultdict(set)
    trailheads: set[tuple[int, int]] = set()
    peaks: set[tuple[int, int]] = set()

    for row in range(rows):
        for col in range(cols):
            current_pos = (row, col)
            height = map[row, col]
            if height == 0:
                trailheads.add(current_pos)

            if height == 9:
                peaks.add(current_pos)

            if row != 0:
                other_pos = (row - 1, col)
                other_height = map[row - 1, col]
                if height - other_height == 1:
                    graph[other_pos].add(current_pos)

                if other_height - height == 1:
                    graph[current_pos].add(other_pos)

            if col != 0:
                other_pos = (row, col - 1)
                other_height = map[row, col - 1]
                if height - other_height == 1:
                    graph[other_pos].add(current_pos)

                if other_height - height == 1:
                    graph[current_pos].add(other_pos)

    return trailheads, peaks, graph


def count_trails(
    trailheads: set[tuple[int, int]],
    peaks: set[tuple[int, int]],
    graph: dict[tuple[int, int], set[tuple[int, int]]],
) -> int:

    def dfs_helper(
        graph: dict[tuple[int, int], set[tuple[int, int]]],
        starting_point: tuple[int, int],
    ) -> set[tuple[int, int]]:
        visited = set()
        node_stack = [starting_point]

        while node_stack:
            current_node = node_stack.pop()
            visited.add(current_node)

            for child in graph[current_node]:
                if child not in visited and child not in node_stack:
                    node_stack.append(child)

        return visited

    num_trails = 0
    for trailhead in trailheads:
        visited = dfs_helper(graph, trailhead)
        num_trails += len(visited.intersection(peaks))

    return num_trails


def part_1(file_path: str):
    topo_map = read_file(file_path)
    trailheads, peaks, graph = read_map(topo_map)
    print(count_trails(trailheads, peaks, graph))


def count_ratings(trailheads: set[tuple[int, int]], peaks: set[tuple[int, int]], graph: dict[tuple[int, int], set[tuple[int, int]]]) -> int:

    def dfs_helper(
        graph: dict[tuple[int, int], set[tuple[int, int]]],
        starting_point: tuple[int, int],
    ) -> dict[tuple[int, int], int]:
        visit_counts: dict[tuple[int, int], int] = defaultdict(int)
        node_stack = [starting_point]

        while node_stack:
            current_node = node_stack.pop()
            visit_counts[current_node] += 1

            for child in graph[current_node]:
                node_stack.append(child)

        return visit_counts

    ratings = 0
    for trailhead in trailheads:
        visit_counts = dfs_helper(graph, trailhead)

        for peak in peaks:
            ratings += visit_counts[peak]

    return ratings



def part_2(file_path: str):
    topo_map = read_file(file_path)
    trailheads, peaks, graph = read_map(topo_map)
    print(count_ratings(trailheads, peaks, graph))


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
