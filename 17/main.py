import argparse
from dataclasses import dataclass
from typing import Optional

State = tuple[int, int, int] # B, C, i

@dataclass
class InstructionSet:
    a: int
    b: int
    c: int
    instructions: list[int]
    _counter: int = 0

    def run_program(self) -> list[int]:
        output: list[int] = []
        while self._counter < len(self.instructions):
            maybe_out = self._step()
            if maybe_out is not None:
                output.append(maybe_out)

        return output

    def _step(self) -> Optional[int]:
        opcode = self.instructions[self._counter]
        operand = self.instructions[self._counter + 1]

        if opcode == 0:
            self.a = self.a // (2**self._combo_value(operand))

        if opcode == 1:
            self.b = self.b ^ operand

        if opcode == 2:
            self.b = self._combo_value(operand) % 8

        if opcode == 3 and self.a != 0:
            self._counter = operand
            return None

        if opcode == 4:
            self.b = self.b ^ self.c

        if opcode == 5:
            output = self._combo_value(operand) % 8
            self._counter += 2
            return output

        if opcode == 6:
            self.b = self.a // (2**self._combo_value(operand))

        if opcode == 7:
            self.c = self.a // (2**self._combo_value(operand))

        self._counter += 2
        return None

    def _combo_value(self, code: int) -> int:
        if 0 <= code <= 3:
            return code

        if code == 4:
            return self.a

        if code == 5:
            return self.b

        if code == 6:
            return self.c

        raise ValueError("7 is reserved, or you have an incorrect value")

    def reset(self, a: Optional[int] = None, b:Optional[int] = None, c: Optional[int] = None):
        self._counter = 0
        if a:
            self.a = a
        if b:
            self.b = b
        if c:
            self.c = c


def read_file(file_path: str) -> InstructionSet:
    with open(file_path, "r", encoding="UTF-8") as file:
        a_line = file.readline()
        a = int(a_line.split(":")[1])
        b_line = file.readline()
        b = int(b_line.split(":")[1])
        c_line = file.readline()
        c = int(c_line.split(":")[1])
        file.readline()
        instruction_line = file.readline()
        instructions = [int(x) for x in instruction_line.split(":")[1].split(",")]

    return InstructionSet(a, b, c, instructions)


def part_1(file_path: str):
    instruction_set = read_file(file_path)
    print(instruction_set)
    print(",".join(str(x) for x in instruction_set.run_program()))


def part_2(file_path: str):
    instruction_set = read_file(file_path)
    b0 = instruction_set.b
    c0 = instruction_set.c
    prev_a = 0
    start = len(instruction_set.instructions) - 2
    while start >= 0:
        desired = instruction_set.instructions[start:]
        out: list[int] = []
        x = 0
        while out != desired:
            instruction_set.reset(prev_a * 8 + x, b0, c0)
            out = instruction_set.run_program()
            x += 1
        prev_a = prev_a * 8 + x - 1
        print(prev_a)
        start -= 1



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
