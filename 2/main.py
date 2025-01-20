import argparse

import numpy as np


def read_file(file_path: str) -> list[list[int]]:
    with open(file_path, "r", encoding="UTF-8") as file:
        lines = file.readlines()

    return [[int(x) for x in line.split()] for line in lines]


def is_safe(report: np.ndarray) -> bool:
    delta = report[1:] - report[:-1]
    sign = np.sign(delta)
    return (
        (1 <= np.abs(delta)).all()
        and (np.abs(delta) <= 3).all()
        and (sign == sign[0]).all()
    )


def get_num_safe_reports(reports: list[list[int]]) -> int:
    num_safe = 0
    for report in reports:
        report_np = np.array(report)
        if is_safe(report_np):
            num_safe += 1

    return num_safe


def part_1(file_path: str):
    reports = read_file(file_path)
    output = get_num_safe_reports(reports)
    print(output)


def get_num_safe_reports_damped(reports: list[list[int]]) -> int:
    num_safe = 0
    for report in reports:
        if is_safe(np.array(report)):
            num_safe += 1
            continue
        for i in range(len(report)):
            if is_safe(np.array(report[:i] + report[i+1:])):
                num_safe += 1
                break
    return num_safe


def part_2(file_path: str):
    reports = read_file(file_path)
    output = get_num_safe_reports_damped(reports)
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
