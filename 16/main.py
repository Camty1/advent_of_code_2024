import argparse
import heapq
import sys
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from itertools import product
from typing import Optional

STEP_WEIGHT = 1
ROTATE_WEIGHT = 1000
INF = sys.maxsize


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    @classmethod
    def rotate_cw(cls, direction: "Direction") -> "Direction":
        return Direction((direction.value - 1) % 4)

    @classmethod
    def rotate_ccw(cls, direction: "Direction") -> "Direction":
        return Direction((direction.value + 1) % 4)


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def move(self, direction: Direction) -> "Position":
        if direction == Direction.UP:
            return Position(self.x, self.y - 1)

        if direction == Direction.RIGHT:
            return Position(self.x + 1, self.y)

        if direction == Direction.DOWN:
            return Position(self.x, self.y + 1)

        if direction == Direction.LEFT:
            return Position(self.x - 1, self.y)

        return self


@dataclass(frozen=True)
class MapSize:
    width: int
    height: int


class PositionType(Enum):
    WALL = 0
    OPEN = 1
    START = 2
    END = 3

    @classmethod
    def from_char(cls, char: str) -> Optional["PositionType"]:
        chars = ["#", ".", "S", "E"]
        try:
            index = chars.index(char)
            return PositionType(index)

        except ValueError:
            return None


def read_file(file_path: str) -> tuple[list[list[PositionType]], MapSize]:
    with open(file_path, "r", encoding="UTF-8") as file:
        lines = file.readlines()

    position_types: list[list[PositionType]] = []
    for line in lines:
        row: list[PositionType] = []
        for char in line:
            position_type = PositionType.from_char(char)
            if position_type:
                row.append(position_type)

        position_types.append(row)

    return position_types, MapSize(len(position_types[0]), len(position_types))


@dataclass(frozen=True)
class State:
    position: Position
    direction: Direction


@dataclass(frozen=True)
class Movement:
    next_state: State
    weight: int


MazeGraph = dict[State, set[Movement]]


def graph_from_position_types(
    position_types: list[list[PositionType]], map_size: MapSize
) -> tuple[MazeGraph, Position, Position]:
    maze_graph: MazeGraph = defaultdict(set)
    start_position: Optional[Position] = None
    end_position: Optional[Position] = None
    for x, y in product(range(map_size.width), range(map_size.height)):
        position_type = position_types[y][x]
        if position_type != PositionType.WALL:
            current_position = Position(x, y)

            # Rotation
            for direction in Direction:
                current_state = State(current_position, direction)

                # Clockwise rotation
                cw = Direction.rotate_cw(direction)
                cw_state = State(current_position, cw)
                cw_movement = Movement(cw_state, ROTATE_WEIGHT)
                maze_graph[current_state].add(cw_movement)

                # Counterclockwise rotation
                ccw = Direction.rotate_ccw(direction)
                ccw_state = State(current_position, ccw)
                ccw_movement = Movement(ccw_state, ROTATE_WEIGHT)
                maze_graph[current_state].add(ccw_movement)

            # Translation
            # Up and down
            if y > 0:
                other_position_type = position_types[y - 1][x]
                if other_position_type != PositionType.WALL:
                    current_up_state = State(current_position, Direction.UP)
                    other_position = Position(x, y - 1)
                    other_up_state = State(other_position, Direction.UP)
                    up_movement = Movement(other_up_state, STEP_WEIGHT)
                    maze_graph[current_up_state].add(up_movement)

                    current_down_state = State(current_position, Direction.DOWN)
                    other_down_state = State(other_position, Direction.DOWN)
                    down_movement = Movement(current_down_state, STEP_WEIGHT)
                    maze_graph[other_down_state].add(down_movement)

            # Left and right
            if x > 0:
                other_position_type = position_types[y][x - 1]
                if other_position_type != PositionType.WALL:
                    current_left_state = State(current_position, Direction.LEFT)
                    other_position = Position(x - 1, y)
                    other_left_state = State(other_position, Direction.LEFT)
                    left_movement = Movement(other_left_state, STEP_WEIGHT)
                    maze_graph[current_left_state].add(left_movement)

                    current_right_state = State(current_position, Direction.RIGHT)
                    other_right_state = State(other_position, Direction.RIGHT)
                    right_movement = Movement(current_right_state, STEP_WEIGHT)
                    maze_graph[other_right_state].add(right_movement)

        if position_type == PositionType.START:
            start_position = Position(x, y)

        if position_type == PositionType.END:
            end_position = Position(x, y)

    assert start_position and end_position

    return maze_graph, start_position, end_position


def get_scores_djikstra(
    maze_graph: MazeGraph, start_position: Position
) -> tuple[dict[State, int], dict[State, set[State]]]:
    score: dict[State, int] = {state: INF for state in maze_graph}
    start_state = State(start_position, Direction.RIGHT)
    score[start_state] = 0
    queue: list[tuple[int, int, State]] = [(0, id(start_state), start_state)]
    prev: dict[State, set[State]] = {state: set() for state in maze_graph}
    visited: set[State] = set()

    while queue:
        _, _, node = heapq.heappop(queue)
        if node in visited:
            continue
        visited.add(node)

        for movement in maze_graph[node]:
            neighbor = movement.next_state
            weight = movement.weight
            new_score = score[node] + weight
            if new_score < score[neighbor]:
                score[neighbor] = new_score
                prev[neighbor] = set()
                prev[neighbor].add(node)
                heapq.heappush(queue, (new_score, id(neighbor), neighbor))

            elif new_score == score[neighbor]:
                prev[neighbor].add(node)

    return score, prev


def part_1(file_path: str):
    position_types, map_size = read_file(file_path)
    maze_graph, start_position, end_position = graph_from_position_types(
        position_types, map_size
    )
    score, _ = get_scores_djikstra(maze_graph, start_position)
    print(min(score[State(end_position, direction)] for direction in Direction))


def get_best_path_positions(
    score: dict[State, int], prev: [State, set[State]], end_position: Position
) -> int:

    queue: list[State] = []
    min_score = INF
    for direction in Direction:
        state = State(end_position, direction)
        maybe_min_score = score[state]
        if maybe_min_score < min_score:
            min_score = maybe_min_score
            queue = [state]

        elif maybe_min_score == min_score:
            queue.append(state)

    best_path_positions: set[Position] = set()

    while queue:
        state = queue.pop()
        best_path_positions.add(state.position)

        for parent in prev[state]:
            if parent not in queue:
                queue.append(parent)

    return len(best_path_positions)


def part_2(file_path: str):
    position_types, map_size = read_file(file_path)
    maze_graph, start_position, end_position = graph_from_position_types(
        position_types, map_size
    )
    score, prev = get_scores_djikstra(maze_graph, start_position)
    print(get_best_path_positions(score, prev, end_position))


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
