import argparse
from collections import defaultdict
from copy import deepcopy
from itertools import product
from enum import Enum
from typing import Self


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    @staticmethod
    def turn(direction: Self):
        return Direction((direction.value + 1) % 4)


def read_file(
    file_path: str,
) -> tuple[list[tuple[int, int]], tuple[int, int], tuple[int, int]]:
    with open(file_path, "r", encoding="UTF-8") as file:
        lines = file.readlines()

    obstacles = []
    starting_pos = None
    for row, line in enumerate(lines):
        for col, char in enumerate(line.strip()):
            if char == "#":
                obstacles.append((row, col))
            if char == "^":
                assert not starting_pos
                starting_pos = (row, col)

    assert starting_pos
    return obstacles, starting_pos, (len(lines), len(lines[0].strip()))


def get_next_pos(pos: tuple[int, int], direction: Direction) -> tuple[int, int]:
    if direction == Direction.UP:
        return (pos[0] - 1, pos[1])

    if direction == Direction.RIGHT:
        return (pos[0], pos[1] + 1)

    if direction == Direction.DOWN:
        return (pos[0] + 1, pos[1])

    return (pos[0], pos[1] - 1)


def pos_on_board(pos: tuple[int, int], board_size: tuple[int, int]):
    return 0 <= pos[0] < board_size[0] and 0 <= pos[1] < board_size[1]


def get_num_visited(
    obstacles: list[tuple[int, int]],
    starting_pos: tuple[int, int],
    board_size: tuple[int, int],
) -> int:

    current_pos = starting_pos
    current_direction = Direction.UP
    visited: set[tuple[int, int]] = set()
    on_board = True
    while on_board:
        visited.add(current_pos)
        maybe_next_pos = get_next_pos(current_pos, current_direction)
        while maybe_next_pos in obstacles:
            current_direction = Direction.turn(current_direction)
            maybe_next_pos = get_next_pos(current_pos, current_direction)
        next_pos = maybe_next_pos
        on_board = pos_on_board(next_pos, board_size)
        current_pos = next_pos

    return len(visited)


def part_1(file_path: str):
    obstacles, starting_pos, board_size = read_file(file_path)
    output = get_num_visited(obstacles, starting_pos, board_size)
    print(output)


def get_path(
    obstacles: list[tuple[int, int]],
    starting_pos: tuple[int, int],
    board_size: tuple[int, int],
) -> list[tuple[tuple[int, int], Direction]]:

    current_pos = starting_pos
    current_direction = Direction.UP
    visited: list[tuple[tuple[int, int], Direction]] = []
    on_board = True
    while on_board:
        visited.append((current_pos, current_direction))
        maybe_next_pos = get_next_pos(current_pos, current_direction)
        while maybe_next_pos in obstacles:
            current_direction = Direction.turn(current_direction)
            visited.append((current_pos, current_direction))
            maybe_next_pos = get_next_pos(current_pos, current_direction)
        next_pos = maybe_next_pos
        on_board = pos_on_board(next_pos, board_size)
        current_pos = next_pos

    return visited


def get_num_loops(
    obstacles: list[tuple[int, int]],
    starting_pos: tuple[int, int],
    board_size: tuple[int, int],
) -> int:

    loop_obstacles = []
    for row, col in product(range(board_size[0]), range(board_size[1])):
        print(row, col)
        current_pos = starting_pos
        current_direction = Direction.UP
        visited: dict[tuple[int, int], list[Direction]] = defaultdict(list)
        new_obstacle = (row, col)
        obstacles.append(new_obstacle)
        first_iter = True
        while pos_on_board(current_pos, board_size):
            if current_pos in visited and current_direction in visited[current_pos] and not first_iter:
                loop_obstacles.append(new_obstacle)
                break

            # Add current_pos and current_direction to visited
            visited[current_pos].append(current_direction)

            maybe_next_pos = get_next_pos(current_pos, current_direction)
            if maybe_next_pos in obstacles:
                current_direction = Direction.turn(current_direction)
            else:
                current_pos = maybe_next_pos

            if first_iter:
                first_iter = False

        obstacles.remove(new_obstacle)

    return len(loop_obstacles)


def part_2(file_path: str):
    obstacles, starting_pos, board_size = read_file(file_path)
    output = get_num_loops(obstacles, starting_pos, board_size)
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
