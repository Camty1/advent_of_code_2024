import argparse
import heapq
import re
from collections import namedtuple
from itertools import product

import numpy as np

Game = namedtuple("Game", ["a", "b", "prize"])
Vector = namedtuple("Vector", ["x", "y"])
Press = namedtuple("Press", ["a", "b"])


def read_file(file_path: str) -> list[Game]:
    with open(file_path, "r", encoding="UTF-8") as file:
        lines = file.readlines()

    a = None
    b = None
    prize = None
    games: list[Game] = []
    for line_number, line in enumerate(lines):
        part = line_number % 4
        if part == 3:
            a = None
            b = None
            prize = None
            continue

        number_str = re.sub(r"[^\d,]", "", line)
        if part == 0:
            a = np.array([int(x) for x in number_str.split(",")])

        if part == 1:
            b = np.array([int(x) for x in number_str.split(",")])

        if part == 2:
            prize = np.array([int(x) for x in number_str.split(",")])
            games.append(Game(a=a, b=b, prize=prize))

    return games


def read_file_vector(file_path: str, shift: int = 0) -> list[Game]:
    with open(file_path, "r", encoding="UTF-8") as file:
        lines = file.readlines()

    a = None
    b = None
    prize = None
    games: list[Game] = []
    for line_number, line in enumerate(lines):
        part = line_number % 4
        if part == 3:
            a = None
            b = None
            prize = None
            continue

        number_str = re.sub(r"[^\d,]", "", line)
        if part == 0:
            a = Vector(*[int(x) for x in number_str.split(",")])

        if part == 1:
            b = Vector(*[int(x) for x in number_str.split(",")])

        if part == 2:
            prize = Vector(*[int(x) + shift for x in number_str.split(",")])
            games.append(Game(a=a, b=b, prize=prize))

    return games


def solve_games(games: list[Game]) -> int:
    button_cost = np.array([3, 1])
    cost = 0
    for game in games:
        try:
            moves = np.linalg.solve(np.column_stack([game.a, game.b]), game.prize)
            rounded_moves = np.rint(moves)
            if (np.sign(rounded_moves) >= 0).all() and np.isclose(
                moves, rounded_moves
            ).all():
                cost += int(np.dot(button_cost, rounded_moves))

        # Matrix is singular
        except np.linalg.LinAlgError:
            print(game)

    return cost


def solve_games_dp(games: list[Game]) -> int:
    total_cost = 0
    games = [Game(a=Vector(x=5, y=2), b=Vector(x=3, y=4), prize=Vector(x=21, y=14))]
    for game in games:
        prev = np.full((game.prize.x + 1, game.prize.y + 1), "", dtype=object)
        c = np.full((game.prize.x + 1, game.prize.y + 1), np.inf)
        for x, y in product(range(game.prize.x + 1), range(game.prize.y + 1)):
            if x == 0 and y == 0:
                c[0, 0] = 0
                continue

            prev_x_a = x - game.a.x
            prev_y_a = y - game.a.y
            prev_x_b = x - game.b.x
            prev_y_b = y - game.b.y

            c_a = c[prev_x_a, prev_y_a]
            c_b = c[prev_x_b, prev_y_b]

            if c_a + 3 <= c_b + 1:
                c[x, y] = c_a + 3
                if c_a != np.inf:
                    prev[x, y] = prev[prev_x_a, prev_y_a] + "a"
            else:
                c[x, y] = c_b + 1
                if c_b != np.inf:
                    prev[x, y] = prev[prev_x_b, prev_y_b] + "b"

        if c[-1, -1] != np.inf:
            total_cost += c[-1, -1]

        print(c)
        print(prev)
    return total_cost


def press_to_pos(press: Press, game: Game) -> Vector:
    return Vector(
        x=press.a * game.a.x + press.b * game.b.x,
        y=press.a * game.a.y + press.b * game.b.y,
    )


def overshoot(pos: Vector, prize: Vector) -> bool:
    return pos.x > prize.x or pos.y > prize.y


def equal(a: Vector, b: Vector) -> bool:
    return a.x == b.x and a.y == b.y


def solve_games_djikstra(games: list[Game]):
    total_cost = 0
    for game in games:
        cost: dict[Press, int] = {Press(0, 0): 0}
        prev: dict[Press, Press] = {}
        visited: set[Press] = set()

        priority_queue: list[tuple[int, Press]] = []
        heapq.heappush(priority_queue, (0, Press(0, 0)))

        while priority_queue:
            current_cost, node = heapq.heappop(priority_queue)
            visited.add(node)
            current_pos = press_to_pos(node, game)
            if equal(current_pos, game.prize):
                total_cost += current_cost
                break

            press_a = Press(a=node.a + 1, b=node.b)
            if (
                not overshoot(press_to_pos(press_a, game), game.prize)
                and press_a not in visited
            ):
                new_cost = current_cost + 3
                if press_a in cost:
                    if new_cost < cost[press_a]:
                        priority_queue.remove((cost[press_a], press_a))
                        heapq.heapify(priority_queue)
                        heapq.heappush(priority_queue, (new_cost, press_a))
                        cost[press_a] = new_cost
                        prev[press_a] = node

                else:
                    heapq.heappush(priority_queue, (new_cost, press_a))
                    cost[press_a] = new_cost
                    prev[press_a] = node

            press_b = Press(a=node.a, b=node.b + 1)
            if (
                not overshoot(press_to_pos(press_b, game), game.prize)
                and press_b not in visited
            ):
                new_cost = current_cost + 1
                if press_b in cost:
                    if new_cost < cost[press_b]:
                        priority_queue.remove((cost[press_b], press_b))
                        heapq.heapify(priority_queue)
                        heapq.heappush(priority_queue, (new_cost, press_b))
                        cost[press_b] = new_cost
                        prev[press_b] = node

                else:
                    heapq.heappush(priority_queue, (new_cost, press_b))
                    cost[press_b] = new_cost
                    prev[press_b] = node

    return total_cost


def solve_games_systems(games: list[Game]) -> int:
    total_cost = 0

    for game in games:
        a: Vector = game.a
        b: Vector = game.b
        prize: Vector = game.prize
        a_coeff: int = a.x * b.y - b.x * a.y
        prize_coeff: int = prize.x * b.y - b.x * prize.y

        # A is negative
        if np.sign(a_coeff) != np.sign(prize_coeff):
            continue

        # A is not an integer
        if abs(prize_coeff) % abs(a_coeff) != 0:
            continue

        a_value = prize_coeff // a_coeff

        # B is negative
        if prize.x - a_value * a.x < 0:
            continue

        # B is not an integer
        if abs(prize.x - a_value * a.x) % abs(b.x) != 0:
            continue

        b_value = (prize.x - a_value * a.x) // b.x

        total_cost += 3 * a_value + b_value


    return total_cost


def part_1(file_path: str):
    games = read_file_vector(file_path)
    print(solve_games_systems(games))


def solve_games_shifted(games: list[Game], shift: int = 10000000000000) -> int:
    button_cost = np.array([3, 1])
    cost = 0
    for game in games:
        try:
            moves = np.linalg.solve(
                np.column_stack([game.a, game.b]), game.prize + shift
            )
            rounded_moves = np.rint(moves)
            if (np.sign(rounded_moves) >= 0).all() and np.isclose(
                moves, rounded_moves
            ).all():
                cost += int(np.dot(button_cost, rounded_moves))
                print(game, moves, rounded_moves)

        # Matrix is singular
        except np.linalg.LinAlgError:
            continue

    return cost


def part_2(file_path: str):
    games = read_file_vector(file_path, shift=10000000000000)
    print(solve_games_systems(games))


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
