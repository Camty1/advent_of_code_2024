import argparse
import re

import numpy as np

CHAR_TO_INT = {"X": 1, "M": 2, "A": 3, "S": 4}


def read_file(file_path: str) -> list[str]:
    with open(file_path, "r", encoding="UTF-8") as file:
        lines = file.readlines()

    matrix = []
    for line in lines:
        matrix.append([CHAR_TO_INT[x] for x in line.strip()])

    return np.array(matrix)


def find_num_matches(game_matrix: np.ndarray) -> int:
    num_matches = 0
    num_rows, num_cols = game_matrix.shape
    ascending = np.array([1, 2, 3, 4])
    descending = ascending[::-1]
    for row in range(num_rows):
        for col in range(num_cols - 3):
            selection = game_matrix[row, col : col + 4]
            if (selection == ascending).all() or (selection == descending).all():
                num_matches += 1

    for row in range(num_rows - 3):
        for col in range(num_cols):
            selection = game_matrix[row : row + 4, col]
            if (selection == ascending).all() or (selection == descending).all():
                num_matches += 1

    for row in range(num_rows - 3):
        for col in range(num_cols - 3):
            selection = game_matrix[row : row + 4, col : col + 4]
            regular_diag = selection.diagonal()
            anti_diag = np.fliplr(selection).diagonal()
            if (regular_diag == ascending).all() or (regular_diag == descending).all():
                num_matches += 1

            if (anti_diag == ascending).all() or (anti_diag == descending).all():
                num_matches += 1

    return num_matches


def part_1(file_path: str):
    game_matrix = read_file(file_path)
    output = find_num_matches(game_matrix)
    print(output)


def get_xs(game_matrix: np.ndarray) -> int:
    num_matches = 0
    num_rows, num_cols = game_matrix.shape
    ascending = np.array([2, 3, 4])
    descending = ascending[::-1]

    for row in range(num_rows - 2):
        for col in range(num_cols - 2):
            selection = game_matrix[row : row + 3, col : col + 3]
            regular_diag = selection.diagonal()
            anti_diag = np.fliplr(selection).diagonal()
            if (
                ((regular_diag == ascending).all()
                or (regular_diag == descending).all())
                and ((anti_diag == ascending).all()
                or (anti_diag == descending).all())
            ):
                num_matches += 1

    return num_matches


def part_2(file_path: str):
    game_matrix = read_file(file_path)
    output = get_xs(game_matrix)
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
