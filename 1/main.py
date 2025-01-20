import argparse
from collections import defaultdict


def read_file(file_path: str) -> tuple[list[int], list[int]]:
    with open(file_path, "r", encoding="UTF-8") as file:
        lines = file.readlines()

    left, right = [], []
    for line in lines:
        parts = line.split()
        left.append(int(parts[0]))
        right.append(int(parts[1]))

    return left, right


def sort_and_sum(left: list[int], right: list[int]) -> int:
    sorted_left = sorted(left)
    sorted_right = sorted(right)

    running_sum = 0
    for l_val, r_val in zip(sorted_left, sorted_right):
        running_sum += abs(l_val - r_val)

    return running_sum


def part_1(file_path: str):
    left, right = read_file(file_path)
    output = sort_and_sum(left, right)
    print(output)


def calculate_similarity_score(left: list[int], right: list[int]) -> int:
    entries: dict[int, int] = defaultdict(int)
    for value in right:
        entries[value] += 1

    similarity_score = 0
    for value in left:
        if value in entries:
            similarity_score += value * entries[value]

    return similarity_score


def part_2(file_path: str):
    left, right = read_file(file_path)
    output = calculate_similarity_score(left, right)
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
