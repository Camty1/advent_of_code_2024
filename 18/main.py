import argparse
from collections import defaultdict
from dataclasses import dataclass
from itertools import product
from pprint import pprint

import numpy as np


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int


def read_file(file_path: str) -> list[Coordinate]:
    coordinates: list[Coordinate] = []
    with open(file_path, "r", encoding="UTF-8") as file:
        for line in file.readlines():
            coordinates.append(Coordinate(*[int(x) for x in line.split(",")]))

    return coordinates


Graph = dict[Coordinate, set[Coordinate]]


@dataclass
class Board:
    x_size: int
    y_size: int

    def __post_init__(self):
        self.board = np.zeros((self.x_size, self.y_size))
        self.start = Coordinate(0, 0)
        self.finish = Coordinate(self.x_size - 1, self.y_size - 1)

    def add_obstacle(self, coordinate: Coordinate):
        self.board[coordinate.x, coordinate.y] = 1

    def generate_graph(self) -> Graph:
        graph: Graph = defaultdict(set)
        for x, y in product(range(self.x_size), range(self.y_size)):
            if not self.board[x, y]:
                if x != 0 and not self.board[x - 1, y]:
                    here = Coordinate(x, y)
                    there = Coordinate(x - 1, y)
                    graph[here].add(there)
                    graph[there].add(here)

                if y != 0 and not self.board[x, y - 1]:
                    here = Coordinate(x, y)
                    there = Coordinate(x, y - 1)
                    graph[here].add(there)
                    graph[there].add(here)

        return graph

    def __str__(self) -> str:
        string = ""
        for y in range(self.y_size):
            for x in range(self.x_size):
                string += "#" if self.board[x, y] else "."

            string += "\n"

        return string

    def path_string(self, path: list[Coordinate]) -> str:
        string = ""
        for y in range(self.y_size):
            for x in range(self.x_size):
                if Coordinate(x, y) in path:
                    string += "O"
                elif self.board[x, y]:
                    string += "#"
                else:
                    string += "."

            string += "\n"

        return string



def bfs(graph: Graph, start: Coordinate, end: Coordinate) -> list[Coordinate]:
    queue: list[Coordinate] = [start]
    prev: dict[Coordinate, Coordinate] = {}
    while queue:
        current = queue.pop()
        for child in graph[current]:
            if child not in queue and child not in prev:
                queue.insert(0, child)
                prev[child] = current

    if end not in prev:
        return []

    current = end
    reverse_path: list[Coordinate] = []
    while current != start:
        reverse_path.append(current)
        current = prev[current]

    reverse_path.append(start)
    return list(reversed(reverse_path))


def part_1(file_path: str):
    coordinates = read_file(file_path)
    if "sample" in file_path:
        board = Board(7, 7)
        for coordinate in coordinates[:12]:
            board.add_obstacle(coordinate)
    else:
        board = Board(71, 71)
        for coordinate in coordinates[:1024]:
            board.add_obstacle(coordinate)

    graph = board.generate_graph()
    path = bfs(graph, board.start, board.finish)
    print(len(path))


def part_2(file_path: str):
    coordinates = read_file(file_path)
    if "sample" in file_path:
        board = Board(7, 7)
        for coordinate in coordinates[:12]:
            board.add_obstacle(coordinate)

        graph = board.generate_graph()
        path = bfs(graph, board.start, board.finish)
        for coordinate in coordinates[12:]:
            board.add_obstacle(coordinate)
            if coordinate in path:
                graph = board.generate_graph()
                path = bfs(graph, board.start, board.finish)
                if not path:
                    print(coordinate)
                    break
    else:
        board = Board(71, 71)
        for coordinate in coordinates[:1024]:
            board.add_obstacle(coordinate)

        graph = board.generate_graph()
        path = bfs(graph, board.start, board.finish)
        for coordinate in coordinates[1024:]:
            board.add_obstacle(coordinate)
            if coordinate in path:
                graph = board.generate_graph()
                path = bfs(graph, board.start, board.finish)
                if not path:
                    print(coordinate)
                    break


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
