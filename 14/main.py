import argparse
import re
from collections import defaultdict
from dataclasses import dataclass
from itertools import product
from math import prod
from operator import gt, lt

import numpy as np
from PIL import Image, ImageColor


@dataclass
class State:
    pos: np.ndarray
    vel: np.ndarray


@dataclass
class BoardSize:
    x: int
    y: int


def read_file(file_path: str) -> list[State]:
    with open(file_path, "r", encoding="UTF-8") as file:
        lines = file.readlines()

    states: list[State] = []
    for line in lines:
        vectors = re.findall(r"-?\d+,-?\d+", line)
        states.append(
            State(
                *[
                    np.array([int(x) for x in vector.split(",")], dtype=int)
                    for vector in vectors
                ]
            )
        )

    return states


def step(states: list[State], board_size: BoardSize, steps: int = 1):

    for state in states:
        state.pos += steps * state.vel
        state.pos[0] %= board_size.x
        state.pos[1] %= board_size.y


def get_safety_factor(states: list[State], board_size: BoardSize) -> int:
    quadrant_scores: dict[int, int] = defaultdict(int)
    x_divider = board_size.x // 2
    y_divider = board_size.y // 2
    for state in states:
        for quadrant, (x_op, y_op) in enumerate(product([lt, gt], repeat=2)):
            if x_op(state.pos[0], x_divider) and y_op(state.pos[1], y_divider):
                quadrant_scores[quadrant] += 1

    return prod(quadrant_scores[i] for i in range(4))


def part_1(file_path: str):
    states: list[State] = read_file(file_path)
    if "sample" in file_path:
        board_size = BoardSize(11, 7)
    else:
        board_size = BoardSize(101, 103)

    num_steps = 100
    step(states, board_size, num_steps)

    print(get_safety_factor(states, board_size))


def get_color(count: int) -> np.ndarray:
    colors = ["#2c3e50", "#e74c3c", "#ecf0f1", "#e67e22", "#3498db", "#f1c40f"]
    return np.array(ImageColor.getcolor(colors[count], "RGB"))

def save_board(states: list[State], board_size: BoardSize) -> Image:
    positions: dict[tuple[int, int], int] = defaultdict(int)
    for state in states:
        positions[tuple(state.pos)] += 1

    image = np.zeros((board_size.x, board_size.y, 3), dtype=np.uint8)
    for y in range(board_size.y):
        for x in range(board_size.x):
            image[x, y, :] = get_color(positions[(x, y)])

    return Image.fromarray(image)


def part_2(file_path: str):
    states: list[State] = read_file(file_path)
    if "sample" in file_path:
        board_size = BoardSize(11, 7)
    else:
        board_size = BoardSize(101, 103)

    for i in range(10000):
        image = save_board(states, board_size)
        image.save(f"frames/{i}.png")
        print(i)
        step(states, board_size)


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
