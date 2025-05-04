import argparse
from itertools import product

Pin = int
Height = int
Key = tuple[Height, Height, Height, Height, Height]
Lock = tuple[Height, Height, Height, Height, Height]
MAX_HEIGHT = 5
NUM_PINS = 5

height_combos: list[tuple[Height, Height]] = [
    (x, y)
    for x in range(MAX_HEIGHT + 1)
    for y in range(MAX_HEIGHT + 1)
    if x + y <= MAX_HEIGHT
]


def read_file(file_path: str) -> tuple[list[Key], list[Lock]]:
    with open(file_path, "r", encoding="UTF-8") as file:
        text = file.read()

    raw_keys_and_locks = text.split("\n\n")
    keys: list[Key] = []
    locks: list[Lock] = []

    for key_or_lock in raw_keys_and_locks:
        rows = key_or_lock.split()
        pin_heights: list[int] = []
        # Key
        if key_or_lock[0] == ".":
            for pin in range(NUM_PINS):
                height = MAX_HEIGHT
                for row_idx, row in enumerate(reversed(rows[1:-1])):
                    if row[pin] == ".":
                        height = row_idx
                        break
                pin_heights.append(height)

            tuple_pin_heights = tuple(pin_heights)
            assert len(tuple_pin_heights) == NUM_PINS
            keys.append(tuple_pin_heights)

        # Lock
        elif key_or_lock[0] == "#":
            for pin in range(NUM_PINS):
                height = MAX_HEIGHT
                for row_idx, row in enumerate(rows[1:-1]):
                    if row[pin] == ".":
                        height = row_idx
                        break
                pin_heights.append(height)

            tuple_pin_heights = tuple(pin_heights)
            assert len(tuple_pin_heights) == NUM_PINS
            locks.append(tuple_pin_heights)

        else:
            assert False, "PANIC!!!"

    return keys, locks


def part_1(file_path: str):
    keys, locks = read_file(file_path)
    keys_by_pin_by_height: dict[Pin, dict[Height, set[int]]] = {
        pin: {height: set() for height in range(MAX_HEIGHT + 1)}
        for pin in range(NUM_PINS)
    }
    for key_idx, key in enumerate(keys):
        for pin, pin_height in enumerate(key):
            keys_by_pin_by_height[pin][pin_height].add(key_idx)

    locks_by_pin_by_height: dict[Pin, dict[Height, set[int]]] = {
        pin: {height: set() for height in range(MAX_HEIGHT + 1)}
        for pin in range(NUM_PINS)
    }
    for lock_idx, lock in enumerate(locks):
        for pin, pin_height in enumerate(lock):
            locks_by_pin_by_height[pin][pin_height].add(lock_idx)

    currently_valid_combos: set[tuple[int, int]] = {
        (x, y) for x in range(len(keys)) for y in range(len(locks))
    }

    for pin in range(NUM_PINS):
        pin_valid_combos: set[tuple[int, int]] = set()
        for key_height, lock_height in height_combos:
            pin_valid_combos = pin_valid_combos.union(
                set(
                    product(
                        keys_by_pin_by_height[pin][key_height],
                        locks_by_pin_by_height[pin][lock_height],
                    )
                )
            )
        currently_valid_combos = currently_valid_combos.intersection(pin_valid_combos)

    print(len(currently_valid_combos))


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
