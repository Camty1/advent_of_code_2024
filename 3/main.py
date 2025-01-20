import argparse
import re

import numpy as np


def read_file(file_path: str) -> list[str]:
    with open(file_path, "r", encoding="UTF-8") as file:
        text = file.read()
    pattern = r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)"
    return re.findall(pattern, text)


def get_pairs(instructions: list[str]) -> list[tuple[int, int]]:
    pairs: list[tuple[int, int]] = []
    for instruction in instructions:
        if instruction[0] == "m":
            values_str = instruction[4:-1]
            pair = tuple(int(x) for x in values_str.split(","))
            if len(pair) == 2:
                pairs.append(pair)

    return pairs


def multiply_pairs(pairs: list[tuple[int, int]]) -> int:
    return sum(x[0] * x[1] for x in pairs)


def part_1(file_path: str):
    instructions = read_file(file_path)
    pairs = get_pairs(instructions)
    output = multiply_pairs(pairs)
    print(output)


def get_enabled_pairs(instructions: list[str]) -> list[tuple[int, int]]:
    pairs: list[tuple[int, int]] = []
    enabled = True
    for instruction in instructions:
        if instruction == "do()":
            enabled = True
        elif instruction == "don't()":
            enabled = False
        else:
            if enabled:
                values_str = instruction[4:-1]
                pair = tuple(int(x) for x in values_str.split(","))
                if len(pair) == 2:
                    pairs.append(pair)

    return pairs



def part_2(file_path: str):
    instructions = read_file(file_path)
    pairs = get_enabled_pairs(instructions)
    output = multiply_pairs(pairs)
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
