import argparse
from collections import defaultdict
from time import time

import numpy as np


def read_file(file_path: str) -> list[int]:
    with open(file_path, "r", encoding="UTF-8") as file:
        text = file.read()

    return [int(x) for x in text.strip().split()]


def digits(num: int) -> int:
    return int(np.floor(np.log10(num)) + 1)


def update_stones(stones: list[int]):
    index = 0
    while index < len(stones):
        current_stone = stones[index]
        num_digits = digits(current_stone)
        if current_stone == 0:
            stones[index] = 1
            index += 1

        elif num_digits % 2 == 0:
            left = current_stone // (10 ** (num_digits // 2))
            right = current_stone % (10 ** (num_digits // 2))
            stones[index] = right
            stones.insert(index, left)
            index += 2

        else:
            stones[index] *= 2024
            index += 1


def part_1(file_path: str):
    stones = read_file(file_path)
    for _ in range(25):
        update_stones(stones)
    print(len(stones))


def graph_stone_count(stones: list[int], blinks: int) -> int:
    graph: dict[int, set[int]] = defaultdict(set)
    stone_stack = [(stone, 0) for stone in stones]
    final_stones = []
    while stone_stack:
        current_stone, depth = stone_stack.pop()

        if depth == blinks:
            final_stones.append(current_stone)
            continue

        if current_stone in graph:
            stone_stack.extend([(child, depth + 1) for child in graph[current_stone]])
            continue

        if current_stone == 0:
            graph[0].add(1)
            stone_stack.append((1, depth + 1))
            continue

        stone_str = str(current_stone)
        num_digits = len(stone_str)
        if num_digits % 2 == 0:
            left = int(stone_str[: num_digits // 2])
            right = int(stone_str[num_digits // 2 :])
            graph[current_stone].add(left)
            graph[current_stone].add(right)
            stone_stack.append((left, depth + 1))
            stone_stack.append((right, depth + 1))
            continue

        graph[current_stone].add(current_stone * 2024)
        stone_stack.append((current_stone * 2024, depth + 1))

    return len(final_stones)


def split(number: int, num_digits: int) -> tuple[int, int]:
    divisor = 10 ** (num_digits // 2)
    return (number // divisor, number % divisor)


def memoized_blink(stone_dict: dict[int, int]):
    dict_copy = stone_dict.copy()

    for stone, count in dict_copy.items():
        stone_dict[stone] -= count

        if stone == 0:
            stone_dict[1] += count
            continue

        num_digits = digits(stone)
        if num_digits % 2 == 0:
            left, right = split(stone, num_digits)
            stone_dict[left] += count
            stone_dict[right] += count
            continue

        stone_dict[2024 * stone] += count


def part_2(file_path: str):
    stones = read_file(file_path)
    stone_dict = defaultdict(int)
    for stone in stones:
        stone_dict[stone] = 1
    for i in range(75):
        start = time()
        memoized_blink(stone_dict)
        print(i + 1, sum(stone_dict.values()), time() - start)


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
