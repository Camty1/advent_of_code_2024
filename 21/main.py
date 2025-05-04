import argparse
from dataclasses import dataclass
from itertools import permutations

Button = str


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def manhattan_distance(self, other: "Position") -> int:
        return abs(other.x - self.x) + abs(other.y - self.y)

    def __add__(self, other: "Position") -> "Position":
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Position") -> "Position":
        return Position(self.x - other.x, self.y - other.y)

    @classmethod
    def from_button(cls, button: Button) -> "Position":
        assert button in "<>v^"
        if button == "<":
            return Position(-1, 0)

        if button == ">":
            return Position(1, 0)

        if button == "^":
            return Position(0, 1)

        return Position(0, -1)


numeral_graph: dict[Button, set[tuple[Button, Button]]] = {
    "A": {("0", "<"), ("3", "^")},
    "0": {("A", ">"), ("2", "^")},
    "1": {("2", ">"), ("4", "^")},
    "2": {("0", "v"), ("1", "<"), ("3", ">"), ("5", "^")},
    "3": {("A", "v"), ("2", "<"), ("6", "^")},
    "4": {("1", "v"), ("5", ">"), ("7", "^")},
    "5": {("2", "v"), ("4", "<"), ("6", ">"), ("8", "^")},
    "6": {("3", "v"), ("5", "<"), ("9", "^")},
    "7": {("4", "v"), ("8", ">")},
    "8": {("5", "v"), ("7", "<"), ("9", ">")},
    "9": {("6", "v"), ("8", "<")},
}

directional_graph: dict[Button, set[tuple[Button, Button]]] = {
    "A": {("^", "<"), (">", "v")},
    "^": {("A", ">"), ("v", "v")},
    ">": {("A", "^"), ("v", "<")},
    "v": {("^", "^"), ("<", "<"), (">", ">")},
    "<": {("v", ">")},
}

button_positions: dict[Button, Position] = {
    "A": Position(0, 0),
    "0": Position(-1, 0),
    "1": Position(-2, 1),
    "2": Position(-1, 1),
    "3": Position(0, 1),
    "4": Position(-2, 2),
    "5": Position(-1, 2),
    "6": Position(0, 2),
    "7": Position(-2, 3),
    "8": Position(-1, 3),
    "9": Position(0, 3),
    "^": Position(-1, 0),
    "<": Position(-2, -1),
    "v": Position(-1, -1),
    ">": Position(0, -1),
}

invalid_positions = [Position(-2, 0)]

known_shortest: dict[tuple[int, Button, Button], list[Button]] = {}


def read_file(file_path: str) -> list[list[Button]]:
    with open(file_path, "r", encoding="UTF-8") as file:
        lines = file.readlines()

    return [list(line.strip()) for line in lines]


def get_movements(combination: list[Button]) -> list[Button]:
    current_position = Position(0, 0)
    buttons_to_press = combination.copy()
    movements = []
    while buttons_to_press:
        next_button = buttons_to_press.pop(0)
        next_button_position = button_positions[next_button]
        delta = next_button_position - current_position
        while delta != Position(0, 0):
            while delta.x > 0:
                maybe_new_position = current_position + Position(1, 0)
                if maybe_new_position in invalid_positions:
                    break
                movements.append(">")
                current_position = maybe_new_position
                delta = next_button_position - current_position

            while delta.y > 0:
                maybe_new_position = current_position + Position(0, 1)
                if maybe_new_position in invalid_positions:
                    break
                movements.append("^")
                current_position = maybe_new_position
                delta = next_button_position - current_position

            while delta.y < 0:
                maybe_new_position = current_position + Position(0, -1)
                if maybe_new_position in invalid_positions:
                    break
                movements.append("v")
                current_position = maybe_new_position
                delta = next_button_position - current_position

            while delta.x < 0:
                maybe_new_position = current_position + Position(-1, 0)
                if maybe_new_position in invalid_positions:
                    break
                movements.append("<")
                current_position = maybe_new_position
                delta = next_button_position - current_position

        movements.append("A")

        current_position = next_button_position

    return movements


def get_paths(start: Button, end: Button) -> list[list[Button]]:
    start_position = button_positions[start]
    end_position = button_positions[end]
    delta = end_position - start_position
    x_moves = ["<" if delta.x < 0 else ">"] * abs(delta.x)
    y_moves = ["v" if delta.y < 0 else "^"] * abs(delta.y)
    moves = x_moves + y_moves
    all_paths_set = {tuple(x) for x in permutations(moves)}
    all_paths = [list(x) for x in all_paths_set]

    valid_paths: list[list[Button]] = []
    for path in all_paths:
        current_position = start_position
        valid = True
        for button in path:
            delta = Position.from_button(button)
            current_position += delta
            if current_position in invalid_positions:
                valid = False
                break

        if valid:
            valid_paths.append(path + ["A"])

    return valid_paths


def get_steps(
    sequence: list[Button], include_start: bool = True
) -> list[tuple[Button, Button]]:
    if include_start:
        return list(zip(["A"] + sequence[:-1], sequence))

    return list(zip(sequence[:-1], sequence[1:]))


def recursive_no_memo(
    sequence: list[Button], depth: int = 0, max_depth: int = 2
) -> int:
    steps = get_steps(sequence)
    final_len = 0
    for start, end in steps:
        paths = get_paths(start, end)
        if depth == max_depth:
            final_len += len(paths[0])
            continue

        shortest_path_len = None
        for path in paths:
            candidate_sequence_len = recursive_no_memo(path, depth + 1, max_depth)
            if not shortest_path_len or candidate_sequence_len < shortest_path_len:
                shortest_path_len = candidate_sequence_len

        assert shortest_path_len
        final_len += shortest_path_len

    return final_len


def part_1(file_path: str):
    keypad_combos = read_file(file_path)

    running_sum = 0
    for combination in keypad_combos:
        steps = recursive_no_memo(combination)
        value = int("".join(combination[:-1]))
        complexity = value * steps
        print(value, steps, complexity)
        running_sum += complexity

    print(running_sum)

known: dict[tuple[int, Button, ...], int] = {}

def recursive_memo(
    sequence: list[Button], depth: int = 0, max_depth: int = 2
) -> int:
    steps = get_steps(sequence)
    final_len = 0
    for start, end in steps:
        step_key = (depth, start, end)
        if step_key in known:
            final_len += known[step_key]
            continue

        paths = get_paths(start, end)
        if depth == max_depth:
            final_len += len(paths[0])
            continue

        shortest_path_len = None
        for path in paths:
            candidate_sequence_len = recursive_memo(path, depth + 1, max_depth)
            if not shortest_path_len or candidate_sequence_len < shortest_path_len:
                shortest_path_len = candidate_sequence_len

        assert shortest_path_len
        known[step_key] = shortest_path_len
        final_len += shortest_path_len

    return final_len


def part_2(file_path: str):
    keypad_combos = read_file(file_path)

    running_sum = 0
    for combination in keypad_combos:
        steps = recursive_memo(combination, max_depth=25)
        value = int("".join(combination[:-1]))
        complexity = value * steps
        print(value, steps, complexity)
        running_sum += complexity

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
