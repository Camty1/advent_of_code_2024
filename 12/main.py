import argparse
from collections import defaultdict
from itertools import product


def read_file(file_path: str) -> tuple[list[list[str]], tuple[int, int]]:
    with open(file_path, "r", encoding="UTF-8") as file:
        lines = file.readlines()

    garden_map: list[list[str]] = []
    for line in lines:
        line = line.strip()
        row = []
        for char in line:
            row.append(char)

        garden_map.append(row)

    return garden_map, (len(garden_map), len(garden_map[0]))


def graph_from_garden_map(
    garden_map: list[list[str]], map_size: tuple[int, int]
) -> dict[tuple[int, int], set[tuple[int, int]]]:
    num_rows, num_cols = map_size
    graph: dict[tuple[int, int], set[tuple[int, int]]] = defaultdict(set)
    for row in range(num_rows):
        for col in range(num_cols):
            current_char = garden_map[row][col]
            if row != 0:
                above_char = garden_map[row - 1][col]
                if above_char == current_char:
                    graph[(row, col)].add((row - 1, col))
                    graph[(row - 1, col)].add((row, col))
            if col != 0:
                above_char = garden_map[row][col - 1]
                if above_char == current_char:
                    graph[(row, col)].add((row, col - 1))
                    graph[(row, col - 1)].add((row, col))

    return graph


def get_fence_cost(
    graph: dict[tuple[int, int], set[tuple[int, int]]], map_size: tuple[int, int]
):
    num_rows, num_cols = map_size
    not_yet_visited: set[tuple[int, int]] = set()
    for row in range(num_rows):
        for col in range(num_cols):
            not_yet_visited.add((row, col))

    cost = 0
    while not_yet_visited:
        starting_node = not_yet_visited.pop()
        node_stack: list[tuple[int, int]] = [starting_node]
        visited: set[tuple[int, int]] = set()
        area = 0
        perimeter = 0
        while node_stack:
            current_node = node_stack.pop()
            visited.add(current_node)
            area += 1
            perimeter += 4 - len(graph[current_node])

            for neighbor in graph[current_node]:
                if neighbor not in visited and neighbor not in node_stack:
                    node_stack.append(neighbor)

        not_yet_visited -= visited
        cost += area * perimeter

    return cost


def part_1(file_path: str):
    garden_map, map_size = read_file(file_path)
    graph = graph_from_garden_map(garden_map, map_size)
    print(get_fence_cost(graph, map_size))


def get_bulk_fence_cost(
    graph: dict[tuple[int, int], set[tuple[int, int]]],
    map_size: tuple[int, int],
    garden_map: list[list[str]],
) -> int:
    num_rows, num_cols = map_size
    not_yet_visited: set[tuple[int, int]] = set()
    for row in range(num_rows):
        for col in range(num_cols):
            not_yet_visited.add((row, col))

    cost = 0
    while not_yet_visited:
        starting_node = not_yet_visited.pop()
        node_stack: list[tuple[int, int]] = [starting_node]
        visited: set[tuple[int, int]] = set()
        area = 0
        while node_stack:
            current_node = node_stack.pop()
            visited.add(current_node)
            area += 1

            for neighbor in graph[current_node]:
                if neighbor not in visited and neighbor not in node_stack:
                    node_stack.append(neighbor)

        sides = 0
        for node in visited:
            row, col = node
            for row_offset, col_offset in product([-1, 1], repeat=2):
                row_in_region = (row + row_offset, col) in visited
                col_in_region = (row, col + col_offset) in visited
                if not (row_in_region or col_in_region):
                    sides += 1

                if row_in_region and col_in_region:
                    corner_in_region = (row + row_offset, col + col_offset) in visited
                    if not corner_in_region:
                        sides += 1

        not_yet_visited -= visited
        cost += area * sides

    return cost


def part_2(file_path: str):
    garden_map, map_size = read_file(file_path)
    graph = graph_from_garden_map(garden_map, map_size)
    print(get_bulk_fence_cost(graph, map_size, garden_map))
    pass


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
