import os

template = """import argparse


def part_1(file_path: str):
    pass

def part_2(file_path: str):
    pass

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
"""

for day in range(25):
    file_path = f"{day + 1}/main.py"
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="UTF-8") as file:
            file.write(template)
