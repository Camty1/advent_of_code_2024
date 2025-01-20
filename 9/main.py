import argparse
from enum import Enum

class State(Enum):
    FULL = 0
    EMPTY = 1

    def get_next(self):
        return State((self.value + 1) % 2)


def read_file(
    file_path: str,
) -> list[int]:
    with open(file_path, "r", encoding="UTF-8") as file:
        text = file.read().strip()

    id_counter = 0
    memory = []
    state = State.FULL
    for char in text:
        num_blocks = int(char)
        if state == State.FULL:
            for _ in range(num_blocks):
                memory.append(id_counter)
            id_counter += 1
            state = state.get_next()
        else:
            for _ in range(num_blocks):
                memory.append(-1)
            state = state.get_next()

    return memory

def compact_memory(memory: list[int]):
    starting_index = 0
    for from_index in reversed(range(len(memory))):
        # Memory is not free
        if memory[from_index] != -1:
            for maybe_to_index in range(starting_index, from_index):
                if maybe_to_index >= from_index:
                    break
                if memory[maybe_to_index] == -1:
                    memory[maybe_to_index] = memory[from_index]
                    memory[from_index] = -1
                    break
            starting_index = maybe_to_index
        if maybe_to_index >= from_index:
            break

def memory_checksum(memory: list[int]) -> int:
    checksum = 0
    for position, file_id in enumerate(memory):
        if file_id == -1:
            continue
        checksum += position * file_id

    return checksum

def part_1(file_path: str):
    memory = read_file(file_path)
    compact_memory(memory)
    print(memory_checksum(memory))


def read_file_blocks(file_path: str) -> list[tuple[int, int]]:
    with open(file_path, "r", encoding="UTF-8") as file:
        text = file.read().strip()

    id_counter = 0
    memory_blocks: list[tuple[int, int]] = []
    state = State.FULL
    for char in text:
        num_blocks = int(char)
        if state == State.FULL:
            memory_blocks.append((id_counter, num_blocks))
            id_counter += 1
            state = state.get_next()
        else:
            memory_blocks.append((-1, num_blocks))
            state = state.get_next()

    return memory_blocks

def compact_memory_blocks(memory_blocks: list[tuple[int, int]]):
    blocks_from_end = 1
    while blocks_from_end < len(memory_blocks):
        current_block = memory_blocks[-blocks_from_end]
        block_id, block_size = current_block
        if block_id == -1:
            blocks_from_end += 1
            continue

        result = None
        for move_index, move_block in enumerate(memory_blocks):
            # Didn't find anything
            if move_block == current_block:
                break

            # Check if found something
            move_id, move_size = move_block
            if move_id == -1 and move_size >= block_size:
                result = (move_index, move_size)
                break

        # Found something
        if result:
            move_index, move_size = result
            # Pure swap
            if move_size == block_size:
                memory_blocks[move_index] = (block_id, block_size)
                memory_blocks[-blocks_from_end] = (-1, block_size)
            # Memory left over
            else:
                memory_blocks[move_index] = (-1, move_size - block_size)
                memory_blocks.insert(move_index, (block_id, block_size))
                memory_blocks[-blocks_from_end] = (-1, block_size)

        else:
            blocks_from_end += 1

def unblock_memory(memory_blocks: list[tuple[int, int]]) -> list[int]:
    memory = []
    for block in memory_blocks:
        block_id, block_size = block
        for _ in range(block_size):
            memory.append(block_id)

    return memory

def part_2(file_path: str):
    memory_blocks = read_file_blocks(file_path)
    compact_memory_blocks(memory_blocks)
    memory = unblock_memory(memory_blocks)
    print(memory_checksum(memory))

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
