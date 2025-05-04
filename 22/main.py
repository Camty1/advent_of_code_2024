import argparse
from collections import defaultdict

import numpy as np


def read_file(file_path: str) -> list[int]:
    with open(file_path, "r", encoding="UTF-8") as file:
        lines = file.readlines()

    return [int(x) for x in lines]


def mix(secret_number: int, other: int) -> int:
    return secret_number ^ other


def prune(secret_number: int) -> int:
    return secret_number % 16777216


def generate_next(secret_number: int) -> int:
    a = prune(mix(secret_number, 64 * secret_number))
    b = prune(mix(a, a // 32))
    return prune(mix(b, 2048 * b))


def part_1(file_path: str):
    secret_numbers = read_file(file_path)
    running_sum = 0
    for secret_number in secret_numbers:
        for i in range(2000):
            secret_number = generate_next(secret_number)

        print(secret_number)
        running_sum += secret_number

    print(running_sum)


def part_2(file_path: str):
    secret_numbers = read_file(file_path)

    num_monkeys = len(secret_numbers)
    num_steps = 2000
    price_array = np.zeros((num_monkeys, num_steps + 1))
    print(price_array.shape)
    for row, secret_number in enumerate(secret_numbers):
        monkey_prices = [secret_number % 10]
        for i in range(num_steps):
            secret_number = generate_next(secret_number)
            monkey_prices.append(secret_number % 10)

        price_array[row, :] = np.array(monkey_prices)

    price_changes = price_array[:, 1:] - price_array[:, :-1]
    price_array = price_array[:, 1:]
    profits: dict[tuple[int, int, int, int], int] = defaultdict(int)

    for i in range(num_monkeys):
        print(i)
        already_bought = defaultdict(bool)
        keys = zip(
            price_changes[i, 0:-3],
            price_changes[i, 1:-2],
            price_changes[i, 2:-1],
            price_changes[i, 3:],
        )
        prices = price_array[i, 3:]
        for key, price in zip(keys, prices):
            profits[key] += price * (not already_bought[key])
            already_bought[key] = True

    print(max(profits.items(), key=lambda x: x[1]))





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
