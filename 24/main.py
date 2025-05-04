import argparse
from collections import defaultdict
from dataclasses import dataclass
from enum import IntEnum, auto
from pprint import pprint
from typing import Optional, Union


class Operator(IntEnum):
    AND = auto()
    OR = auto()
    XOR = auto()

    @classmethod
    def from_str(cls, input_str: str) -> "Operator":
        return getattr(cls, input_str.upper())

    def __call__(self, a: int, b: int) -> int:
        if self.name == "AND":
            return a & b

        if self.name == "OR":
            return a | b

        return a ^ b


@dataclass(frozen=True)
class UniqueOperator:
    operator: Operator
    id: int


class UniqueOperatorFactory:
    _num_and = 0
    _num_or = 0
    _num_xor = 0

    def get_unique_operator(self, operator: Operator) -> UniqueOperator:
        if operator == Operator.AND:
            unique_operator = UniqueOperator(operator, self._num_and)
            self._num_and += 1
            return unique_operator

        if operator == Operator.OR:
            unique_operator = UniqueOperator(operator, self._num_or)
            self._num_or += 1
            return unique_operator

        unique_operator = UniqueOperator(operator, self._num_xor)
        self._num_xor += 1
        return unique_operator


unique_operator_factory = UniqueOperatorFactory()

Vertex = Union[str, UniqueOperator]


def read_file(
    file_path: str,
) -> tuple[
    dict[Vertex, Union[Vertex, set[Vertex]]],
    dict[UniqueOperator, tuple[str, str]],
    dict[str, int],
]:
    graph: dict[Vertex, Union[Vertex, set[Vertex]]] = {}
    operator_inputs: dict[UniqueOperator, tuple[str, str]] = {}
    values: dict[str, int] = {}
    with open(file_path, "r", encoding="UTF-8") as file:
        line = file.readline()
        reading_initial_values = True
        while line:
            if reading_initial_values:
                if not line.strip():
                    reading_initial_values = False
                else:
                    key, value_str = line.split(":")
                    values[key] = int(value_str)
            else:
                a, operator_str, b, _, out = line.strip().split()
                operator = Operator.from_str(operator_str)
                unique_operator = unique_operator_factory.get_unique_operator(operator)
                if a not in graph:
                    graph[a] = set()
                graph[a].add(unique_operator)

                if b not in graph:
                    graph[b] = set()
                graph[b].add(unique_operator)

                operator_inputs[unique_operator] = (a, b)
                graph[unique_operator] = out

            line = file.readline()

        return graph, operator_inputs, values


def topological_sort(graph: dict[Vertex, Union[Vertex, set[Vertex]]]) -> list[Vertex]:

    visited: set[Vertex] = set()
    order: list[Vertex] = []

    def dfs(vertex: Vertex):
        visited.add(vertex)
        if vertex in graph:
            if isinstance(vertex, str):
                for neighbor in graph[vertex]:
                    if neighbor not in visited:
                        dfs(neighbor)
            else:
                if graph[vertex] not in visited:
                    dfs(graph[vertex])

        order.insert(0, vertex)

    for vertex in graph:
        if vertex not in visited:
            dfs(vertex)

    return order


def part_1(file_path: str):
    graph, operator_inputs, values = read_file(file_path)

    topological_order = topological_sort(graph)

    for vertex in topological_order:
        if isinstance(vertex, str):
            assert vertex in values
            continue

        # Is an operator
        a_label, b_label = operator_inputs[vertex]
        output_label = graph[vertex]
        assert isinstance(output_label, str)
        a = values[a_label]
        b = values[b_label]
        values[output_label] = vertex.operator(a, b)

    print(0, end="")
    x_keys = sorted([x for x in values if x[0] == "x"], reverse=True)
    x_value = 0
    for x_key in x_keys:
        x_value = (x_value << 1) | values[x_key]
        print(values[x_key], end="")
    print()

    print(0, end="")
    y_keys = sorted([x for x in values if x[0] == "y"], reverse=True)
    y_value = 0
    for y_key in y_keys:
        y_value = (y_value << 1) | values[y_key]
        print(values[y_key], end="")
    print()

    z_keys = sorted([x for x in values if x[0] == "z"], reverse=True)
    z_value = 0
    for z_key in z_keys:
        z_value = (z_value << 1) | values[z_key]
        print(values[z_key], end="")
    print()

    for i in range(45, -1, -1):
        print(i%10, end="")
    print()

    print(x_value + y_value)
    print(z_value)


def reverse_graph(
    graph: dict[Vertex, Union[Vertex, set[Vertex]]]
) -> dict[Vertex, set[Vertex]]:
    new_graph: dict[Vertex, set[Vertex]] = defaultdict(set)
    for source, target in graph.items():
        if isinstance(target, set):
            for target_vertex in target:
                new_graph[target_vertex].add(source)
        else:
            new_graph[target].add(source)

    return new_graph


def part_2(file_path: str):
    graph, operator_inputs, values = read_file(file_path)

    topological_order = topological_sort(graph)

    for vertex in topological_order:
        if isinstance(vertex, str):
            assert vertex in values
            continue

        # Is an operator
        a_label, b_label = operator_inputs[vertex]
        output_label = graph[vertex]
        assert isinstance(output_label, str)
        a = values[a_label]
        b = values[b_label]
        values[output_label] = vertex.operator(a, b)

    x_keys = sorted([x for x in values if x[0] == "x"], reverse=True)
    x_value = 0
    for x_key in x_keys:
        x_value = (x_value << 1) | values[x_key]

    y_keys = sorted([x for x in values if x[0] == "y"], reverse=True)
    y_value = 0
    for y_key in y_keys:
        y_value = (y_value << 1) | values[y_key]

    z_keys = sorted([x for x in values if x[0] == "z"], reverse=True)
    z_value = 0
    for z_key in z_keys:
        z_value = (z_value << 1) | values[z_key]

    carry = None
    for i in range(45):
        x = f"x{i:02}"
        y = f"y{i:02}"
        z = f"z{i:02}"
        print(x, y)
        if graph[x] != graph[y]:
            print("BONGO")
            break
        xor_gate = None
        and_gate = None
        for unique_operator in graph[x]:
            if unique_operator.operator == Operator.XOR:
                xor_gate = unique_operator
            else:
                and_gate = unique_operator

        assert xor_gate
        assert and_gate
        xor_output = graph[xor_gate]
        and_output = graph[and_gate]
        if carry:
            assert graph[carry] == graph[xor_output], f"{carry}, {xor_output}"
            xor_gate = None
            and_gate = None
            for unique_operator in graph[carry]:
                if unique_operator.operator == Operator.XOR:
                    xor_gate = unique_operator
                else:
                    and_gate = unique_operator

            assert xor_gate
            assert and_gate
            digit_output = graph[xor_gate]
            assert digit_output == z, f"{digit_output}, {z}"
            carry_and_output = graph[and_gate]

            assert graph[carry_and_output] == graph[and_output]

            or_gate_set = graph[and_output]
            assert len(or_gate_set) == 1
            or_gate = or_gate_set.pop()
            print(or_gate)
            carry = graph[or_gate]

        else:
            carry = and_output
            digit_output = xor_output
            assert digit_output == z
            print(x, y, and_output)


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
