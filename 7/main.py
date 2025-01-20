import argparse


def read_file(
    file_path: str,
) -> list[tuple[int, list[int]]]:
    with open(file_path, "r", encoding="UTF-8") as file:
        lines = file.readlines()

    values: list[tuple[int, list[int]]] = []
    for line in lines:
        split_line = line.split(":")
        solution = int(split_line[0])
        sequence_str = split_line[1].strip()
        sequence = [int(x) for x in sequence_str.split()]

        values.append((solution, sequence))

    return values


def sum_valid_equations(values: list[tuple[int, list[int]]]) -> int:
    running_sum = 0
    for solution, sequence in values:
        possible_combinations = 2 ** (len(sequence) - 1)
        for i in range(possible_combinations):
            maybe_solution = sequence[0]
            operators = f"{i:0{len(sequence)-1}b}"
            for j, operator in enumerate(operators):
                # plus
                if operator == '0':
                    maybe_solution += sequence[j + 1]
                else:
                    maybe_solution *= sequence[j + 1]

            if maybe_solution == solution:
                running_sum += solution
                break

    return running_sum


def part_1(file_path: str):
    values = read_file(file_path)
    output = sum_valid_equations(values)
    print(output)

def num_to_ternary(num: int, length: int = 0) -> str:
    string = ""
    if num == 0:
        return "0".zfill(length)
    if num == 1:
        return "1".zfill(length)
    while num >= 1:
        r = num % 3
        string = f"{r}{string}"
        num = num // 3

    return string.zfill(length)

def sum_valid_equations_concat(values: list[tuple[int, list[int]]]) -> int:
    running_sum = 0
    for solution, sequence in values:
        possible_combinations = 3 ** (len(sequence) - 1)
        for i in range(possible_combinations):
            maybe_solution = sequence[0]
            operators = num_to_ternary(i, len(sequence) - 1)
            for j, operator in enumerate(operators):
                # plus
                if operator == '0':
                    maybe_solution += sequence[j + 1]
                elif operator == '1':
                    maybe_solution *= sequence[j + 1]
                else:
                    maybe_solution_str = str(maybe_solution)
                    maybe_solution_str += str(sequence[j+1])
                    maybe_solution = int(maybe_solution_str)

            if maybe_solution == solution:
                running_sum += solution
                break

    return running_sum


def part_2(file_path: str):
    values = read_file(file_path)
    output = sum_valid_equations_concat(values)
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
