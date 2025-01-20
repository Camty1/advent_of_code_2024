import argparse
from collections import defaultdict
from itertools import combinations


def read_file(
    file_path: str,
) -> tuple[dict[str, list[tuple[int, int]]], tuple[int, int]]:
    with open(file_path, "r", encoding="UTF-8") as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]

    all_antennae: list[tuple[int, int]] = []
    antennae_by_freq: dict[str, list[tuple[int, int]]] = defaultdict(list)
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char != ".":
                all_antennae.append((row, col))
                antennae_by_freq[char].append((row, col))

    return antennae_by_freq, (len(lines), len(lines[0]))


def add(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    result = tuple(a_component + b_component for a_component, b_component in zip(a, b))
    assert len(result) == 2
    return result


def sub(tip: tuple[int, int], tail: tuple[int, int]) -> tuple[int, int]:
    result = tuple(
        tip_component - tail_component
        for tip_component, tail_component in zip(tip, tail)
    )
    assert len(result) == 2
    return result


def negate(a: tuple[int, int]) -> tuple[int, int]:
    result = tuple(-x for x in a)
    assert len(result) == 2
    return result


def on_board(maybe_antinode: tuple[int, int], board_size: tuple[int, int]) -> bool:
    return (0 <= maybe_antinode[0] < board_size[0]) and (
        0 <= maybe_antinode[1] < board_size[1]
    )


def find_num_antinodes(
    antennae_by_freq: dict[str, list[tuple[int, int]]],
    board_size: tuple[int, int],
) -> int:
    antinodes: set[tuple[int, int]] = set()
    for antennae in antennae_by_freq.values():
        for antenna_1, antenna_2 in combinations(antennae, 2):
            displacement = sub(antenna_2, antenna_1)
            maybe_antinode = add(antenna_2, displacement)
            if on_board(maybe_antinode, board_size):
                antinodes.add(maybe_antinode)

            neg_displacement = negate(displacement)
            maybe_antinode = add(antenna_1, neg_displacement)
            if on_board(maybe_antinode, board_size):
                antinodes.add(maybe_antinode)

    return len(antinodes)


def part_1(file_path: str):
    antennae_by_freq, board_size = read_file(file_path)
    print(find_num_antinodes(antennae_by_freq, board_size))


def find_num_resonant_antinodes(
    antennae_by_freq: dict[str, list[tuple[int, int]]],
    board_size: tuple[int, int],
) -> int:
    antinodes: set[tuple[int, int]] = set()
    for antennae in antennae_by_freq.values():
        for antenna_1, antenna_2 in combinations(antennae, 2):
            antinodes.add(antenna_1)
            antinodes.add(antenna_2)
            displacement = sub(antenna_2, antenna_1)
            maybe_antinode = add(antenna_2, displacement)
            while on_board(maybe_antinode, board_size):
                antinodes.add(maybe_antinode)
                maybe_antinode = add(maybe_antinode, displacement)

            neg_displacement = negate(displacement)
            maybe_antinode = add(antenna_1, neg_displacement)
            while on_board(maybe_antinode, board_size):
                antinodes.add(maybe_antinode)
                maybe_antinode = add(maybe_antinode, neg_displacement)

    return len(antinodes)


def part_2(file_path: str):
    antennae_by_freq, board_size = read_file(file_path)
    print(find_num_resonant_antinodes(antennae_by_freq, board_size))


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
