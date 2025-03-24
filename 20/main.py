import argparse
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from itertools import product
from typing import Optional


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def manhattan_distance(self, other: "Position") -> int:
        return abs(other.x - self.x) + abs(other.y - self.y)

    def __add__(self, other: "Position") -> "Position":
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Position") -> "Position":
        return Position(self.x - other.x, self.y - other.y)


class Direction(Enum):
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3

    def steps(self) -> list[Position]:
        if self == Direction.RIGHT:
            return [Position(2, 0), Position(2, -1), Position(2, 1), Position(3, 0)]
        elif self == Direction.UP:
            return [Position(0, 2), Position(1, 2), Position(-1, 2), Position(0, 3)]
        elif self == Direction.LEFT:
            return [Position(-2, 0), Position(-2, 1), Position(-2, -1), Position(-3, 0)]
        else:
            return [Position(0, -2), Position(-1, -2), Position(1, -2), Position(0, -3)]



@dataclass
class RaceMap:
    x_size: int
    y_size: int
    start: Position
    end: Position
    path_positions: set[Position]
    obstacle_positions: set[Position]
    graph: dict[Position, set[Position]]

    def get_surroundings(self, position: Position) -> set[Position]:
        possible_deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        surroundings: set[Position] = set()
        for dx, dy in possible_deltas:
            x_valid = 0 <= position.x + dx < self.x_size
            y_valid = 0 <= position.y + dy < self.y_size
            if x_valid and y_valid:
                surroundings.add(Position(position.x + dx, position.y + dy))

        return surroundings


def read_file(
    file_path: str,
) -> RaceMap:
    with open(file_path, "r", encoding="UTF-8") as file:
        lines = file.readlines()

    x_size = len(lines[0]) - 1  # Remove newline character
    y_size = len(lines)
    start = None
    end = None
    path_positions: set[Position] = set()
    obstacle_positions: set[Position] = set()
    graph: dict[Position, set[Position]] = defaultdict(set)

    for y, line in enumerate(lines):
        for x, character in enumerate(line.strip()):
            pos = Position(x, y)
            if character in ".SE":
                path_positions.add(pos)
                if character == "S":
                    start = pos

                if character == "E":
                    end = pos

                if x > 0:
                    other_pos = Position(x - 1, y)
                    if other_pos in path_positions:
                        graph[pos].add(other_pos)
                        graph[other_pos].add(pos)

                if y > 0:
                    other_pos = Position(x, y - 1)
                    if other_pos in path_positions:
                        graph[pos].add(other_pos)
                        graph[other_pos].add(pos)

            else:
                obstacle_positions.add(pos)

    assert start and end

    return RaceMap(
        x_size, y_size, start, end, path_positions, obstacle_positions, graph
    )


def get_path(
    race_map: RaceMap,
) -> list[Position]:
    queue: list[Position] = [race_map.start]
    visited: list[Position] = []
    counter = 0
    while queue:
        current_pos = queue.pop()
        visited.append(current_pos)
        for neighbor in race_map.graph[current_pos]:
            if neighbor not in visited and neighbor not in queue:
                queue.append(neighbor)

        counter += 1

    return visited


def part_1(file_path: str):
    race_map = read_file(file_path)
    path = get_path(race_map)
    path_steps = {position: i for i, position in enumerate(path)}
    counter = 0
    for position, ordinal in path_steps.items():
        for direction in Direction:
            for step in direction.steps():
                new_pos = position + step
                if new_pos in path_steps:
                    delta = path_steps[new_pos] - ordinal
                    if delta >= 100:
                        counter += 1
                    break

    print(counter)






def part_2(file_path: str):
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
