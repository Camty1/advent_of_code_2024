import argparse
from collections import defaultdict

Towel = str
Pattern = str


def read_file(file_path: str) -> tuple[list[Towel], list[Pattern]]:
    with open(file_path, "r", encoding="UTF-8") as file:
        towel_line = file.readline()
        towels: list[Towel] = [towel.strip() for towel in towel_line.split(", ")]
        file.readline()

        patterns: list[Pattern] = []
        line = file.readline()
        while line:
            patterns.append(line.strip())
            line = file.readline()

    return towels, patterns


def has_match(towels: list[Towel], pattern: Pattern, max_stripes: int) -> bool:
    pattern_length = len(pattern)
    match_at_index = [False] * (pattern_length + max_stripes)
    match_at_index[pattern_length] = True
    for i in reversed(range(pattern_length)):
        for towel in towels:
            towel_length = len(towel)
            pattern_string = pattern[i : min(pattern_length, i + towel_length)]
            if towel == pattern_string and match_at_index[i + towel_length]:
                match_at_index[i] = True
                break

    return match_at_index[0]


def part_1(file_path: str):
    towels, patterns = read_file(file_path)
    max_stripes = max(len(x) for x in towels)
    running_sum = 0
    for pattern in patterns:
        running_sum += has_match(towels, pattern, max_stripes)

    print(running_sum)


def number_of_matches(towels: list[Towel], pattern: Pattern, max_stripes: int) -> int:
    pattern_length = len(pattern)
    match_at_index = [False] * (pattern_length + max_stripes)
    match_at_index[pattern_length] = True
    connection: dict[int, set[int]] = defaultdict(set)
    for i in reversed(range(pattern_length)):
        for towel in towels:
            towel_length = len(towel)
            pattern_string = pattern[i : min(pattern_length, i + towel_length)]
            if towel == pattern_string and match_at_index[i + towel_length]:
                match_at_index[i] = True
                connection[i + towel_length].add(i)

    if not match_at_index[0]:
        return 0

    score: dict[int, int] = {0: 1}

    def score_helper(index: int) -> int:

        if index in score:
            return score[index]

        element_score = 0
        for child in connection[index]:
            element_score += score_helper(child)

        score[index] = element_score
        return element_score

    return score_helper(pattern_length)


def part_2(file_path: str):
    towels, patterns = read_file(file_path)
    max_stripes = max(len(x) for x in towels)
    running_sum = 0
    for i, pattern in enumerate(patterns):
        print(f"{i+1}/{len(patterns)}")
        running_sum += number_of_matches(towels, pattern, max_stripes)

    print(running_sum)


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
