import argparse
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    @classmethod
    def from_char(cls, char: str) -> Optional["Direction"]:
        chars = ["^", ">", "v", "<"]
        try:
            index = chars.index(char)
            return cls(index)
        except ValueError:
            return None


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

    def is_left_of(self, other_position: "Position") -> bool:
        return (self.y == other_position.y) and (self.x + 1 == other_position.x)


@dataclass
class RobotMap:
    robot_position: Position
    box_positions: set[Position]
    wall_positions: set[Position]
    map_width: int = 0
    map_height: int = 0

    def __post_init__(self):
        self.map_width = max(pos.x for pos in self.wall_positions) + 1
        self.map_height = max(pos.y for pos in self.wall_positions) + 1

    def check_move(self, direction: Direction):
        current_position = self.robot_position

        boxes_to_move: set[Position] = set()
        while (
            current_position == self.robot_position
            or current_position in self.box_positions
        ):
            if current_position in self.box_positions:
                boxes_to_move.add(current_position)

            current_position = current_position.move(direction)

        if current_position not in self.wall_positions:
            self.robot_position = self.robot_position.move(direction)
            self.box_positions -= boxes_to_move
            for box in boxes_to_move:
                self.box_positions.add(box.move(direction))

    def sum_gps(self) -> int:
        running_sum = 0
        for box in self.box_positions:
            running_sum += 100 * box.y + box.x

        return running_sum

    def print(self):
        for y in range(self.map_height):
            for x in range(self.map_width):
                position = Position(x, y)
                if position == self.robot_position:
                    print("@", end="")
                    continue

                if position in self.box_positions:
                    print("O", end="")
                    continue

                if position in self.wall_positions:
                    print("#", end="")
                    continue

                print(".", end="")

            print()


def read_file(file_path: str) -> tuple[RobotMap, list[Direction]]:
    with open(file_path, "r", encoding="UTF-8") as file:
        lines = file.readlines()

    split_line = lines.index("\n")
    map_lines = lines[:split_line]
    direction_lines = lines[split_line + 1 :]

    robot_position: Optional[Position] = None
    box_positions: set[Position] = set()
    wall_positions: set[Position] = set()
    for y, line in enumerate(map_lines):
        for x, char in enumerate(line):
            if char == "O":
                box_positions.add(Position(x, y))

            if char == "@":
                robot_position = Position(x, y)

            if char == "#":
                wall_positions.add(Position(x, y))

    assert robot_position
    robot_map = RobotMap(robot_position, box_positions, wall_positions)

    direction_str = "".join(
        [direction_line.strip() for direction_line in direction_lines]
    )
    direction_list: list[Direction] = []
    for char in direction_str:
        direction = Direction.from_char(char)
        if direction:
            direction_list.append(direction)

    return robot_map, direction_list


def part_1(file_path: str):
    robot_map, direction_list = read_file(file_path)
    for direction in direction_list:
        robot_map.check_move(direction)

    print(robot_map.sum_gps())


@dataclass
class WideRobotMap:

    robot_position: Position
    left_box_positions: set[Position]
    right_box_positions: set[Position]
    box_pairs: dict[Position, Position]
    wall_positions: set[Position]
    map_width: int = 0
    map_height: int = 0

    def __post_init__(self):
        self.map_width = max(pos.x for pos in self.wall_positions) + 1
        self.map_height = max(pos.y for pos in self.wall_positions) + 1

    def check_move(self, direction: Direction):
        boxes_to_move: set[Position] = set()
        position_queue: list[Position] = [self.robot_position]
        hit_wall = False
        while position_queue:
            current_position = position_queue.pop(0)
            new_position = current_position.move(direction)
            if (
                new_position in self.left_box_positions
                or new_position in self.right_box_positions
                and new_position not in position_queue
            ):
                position_queue.append(new_position)
                boxes_to_move.add(new_position)
                other_half = self.box_pairs[new_position]
                if other_half not in position_queue and other_half not in boxes_to_move:
                    position_queue.append(other_half)
                    boxes_to_move.add(other_half)

                continue

            if new_position in self.wall_positions:
                hit_wall = True
                break

        if not hit_wall:
            self.robot_position = self.robot_position.move(direction)

            old_box_pairs: set[tuple[Position, Position]] = set()
            while boxes_to_move:
                box_half = boxes_to_move.pop()
                # If this is a key error, then something is wrong
                other_half = self.box_pairs[box_half]
                boxes_to_move.remove(other_half)
                if box_half.is_left_of(other_half):
                    old_box_pairs.add((box_half, other_half))
                else:
                    old_box_pairs.add((other_half, box_half))

            new_box_pairs: set[tuple[Position, Position]] = set()
            for left, right in old_box_pairs:
                self.box_pairs.pop(left)
                self.box_pairs.pop(right)
                self.left_box_positions.remove(left)
                self.right_box_positions.remove(right)

                new_left = left.move(direction)
                new_right = right.move(direction)
                new_box_pairs.add((new_left, new_right))

            for left, right in new_box_pairs:
                self.left_box_positions.add(left)
                self.right_box_positions.add(right)
                self.box_pairs[left] = right
                self.box_pairs[right] = left

    def sum_gps(self) -> int:
        running_sum = 0
        for box in self.left_box_positions:
            running_sum += 100 * box.y + box.x

        return running_sum

    def print(self):
        for y in range(self.map_height):
            for x in range(self.map_width):
                position = Position(x, y)
                if position == self.robot_position:
                    print("@", end="")
                    continue

                if position in self.left_box_positions:
                    print("[", end="")
                    continue

                if position in self.right_box_positions:
                    print("]", end="")
                    continue

                if position in self.wall_positions:
                    print("#", end="")
                    continue

                print(".", end="")

            print()


def read_file_wide(file_path: str) -> tuple[WideRobotMap, list[Direction]]:
    with open(file_path, "r", encoding="UTF-8") as file:
        lines = file.readlines()

    split_line = lines.index("\n")
    map_lines = lines[:split_line]
    direction_lines = lines[split_line + 1 :]

    robot_position: Optional[Position] = None
    left_box_positions: set[Position] = set()
    right_box_positions: set[Position] = set()
    wall_positions: set[Position] = set()
    box_pairs: dict[Position, Position] = {}
    for y, line in enumerate(map_lines):
        for x, char in enumerate(line):
            if char == "O":
                left = Position(2 * x, y)
                right = Position(2 * x + 1, y)
                left_box_positions.add(left)
                right_box_positions.add(right)
                box_pairs[left] = right
                box_pairs[right] = left

            if char == "@":
                robot_position = Position(2 * x, y)

            if char == "#":
                wall_positions.add(Position(2 * x, y))
                wall_positions.add(Position(2 * x + 1, y))

    assert robot_position
    robot_map = WideRobotMap(
        robot_position,
        left_box_positions,
        right_box_positions,
        box_pairs,
        wall_positions,
    )

    direction_str = "".join(
        [direction_line.strip() for direction_line in direction_lines]
    )
    direction_list: list[Direction] = []
    for char in direction_str:
        direction = Direction.from_char(char)
        if direction:
            direction_list.append(direction)

    return robot_map, direction_list


def part_2(file_path: str):
    robot_map, direction_list = read_file_wide(file_path)
    for direction in direction_list:
        robot_map.check_move(direction)

    print(robot_map.sum_gps())


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
