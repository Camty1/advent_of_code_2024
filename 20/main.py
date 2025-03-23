import argparse
from collections import defaultdict
from dataclasses import dataclass
from itertools import product
from typing import Optional


@dataclass(frozen=True)
class Position:
    x: int
    y: int


@dataclass
class race_map:
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
) -> race_map:
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
            if character in ["., S, E"]:
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

    return race_map(x_size, y_size, start, end, path_positions, obstacle_positions, graph)


def get_path(
    race_map: race_map,
) -> tuple[
    dict[Position, Optional[Position]],
    dict[Position, Optional[Position]],
    dict[Position, int],
]:
    next_pos: dict[Position, Optional[Position]] = {race_map.end: None}
    prev_pos: dict[Position, Optional[Position]] = {race_map.start: None}
    step: dict[Position, int] = {}

    queue: list[Position] = [race_map.start]
    visited: set[Position] = set()
    counter = 0
    while queue:
        current_pos = queue.pop()
        visited.add(current_pos)
        step[current_pos] = counter
        for neighbor in race_map.graph[current_pos]:
            if neighbor not in visited and neighbor not in queue:
                prev_pos[neighbor] = current_pos
                queue.append(neighbor)

        counter += 1

    current_pos = race_map.end
    while prev_pos[current_pos]:
        next_pos[prev_pos[current_pos]] = current_pos
        current_pos = prev_pos[current_pos]

    return next_pos, prev_pos, step

def read_map


def part_1(file_path: str):
    race_map = read_file(file_path)
    next_pos, prev_pos, step = get_path(race_map)
    


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
