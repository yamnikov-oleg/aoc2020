from dataclasses import dataclass
from enum import Enum
from typing import Iterator, List, Set


class OpCode(Enum):
    NOP = 'nop'
    ACC = 'acc'
    JMP = 'jmp'


@dataclass
class Op:
    opcode: OpCode
    operand: int = 0


def parse_op(line: str) -> Op:
    """
    Example:

    parse_op("acc -3")
    # Returns Op(opcode=OpCode.ACC, operand=-3)
    """
    # Split by words
    words = line.strip().split()
    # Remove empty words
    words = [w for w in words if w]

    if len(words) != 2:
        raise ValueError(f"Operation must consist of two words: {words}")

    # Can throw descriptive ValueError
    opcode = OpCode(words[0])

    try:
        operand = int(words[1])
    except ValueError:
        raise ValueError(f"Invalid operand: {words[1]}")

    return Op(opcode, operand)


class InfiniteLoopError(Exception):
    pass


@dataclass
class VM:
    accumulator: int = 0

    def execute(self, program: List[Op], onloop: str = 'terminate'):
        """
        Executes the program until it ends or until any operation is going
        to be executed second time.

        You can lookup the accumulator attribute after this method returns.

        :param onloop: What should the VM do if there is an infinite loop
            in the program? Valid values:
            'terminate' - the program will be silently terminated.
            'raise' - this method will raise InfiniteLoopError.
        """
        # The index of the currently executed operation
        op_pointer = 0
        # The set of indices of each operation which was executed at least once
        executed_ops: Set[int] = set()

        while op_pointer < len(program):
            if op_pointer in executed_ops:
                if onloop == 'terminate':
                    break
                elif onloop == 'raise':
                    raise InfiniteLoopError("infinite loop")
                else:
                    raise ValueError(f"Invalid onloop: {onloop!r}")

            op = program[op_pointer]
            executed_ops.add(op_pointer)

            if op.opcode == OpCode.NOP:
                op_pointer += 1

            elif op.opcode == OpCode.ACC:
                op_pointer += 1
                self.accumulator += op.operand

            elif op.opcode == OpCode.JMP:
                op_pointer += op.operand

            else:
                raise RuntimeError(f"Don't know how to execute {op}")


def iter_flipped_nop_jmp(program: List[Op]) -> Iterator[List[Op]]:
    """
    Generates a sequence of programs each of which differs from the input
    program by a single NOP instruction changed into JMP (with the operand
    unchanged) or by a single JMP instruction changed into NOP.
    """
    for op_index, op in enumerate(program):
        if op.opcode == OpCode.NOP:
            program_copy = list(program)
            op_copy = Op(OpCode.JMP, op.operand)
            program_copy[op_index] = op_copy
            yield program_copy
        elif op.opcode == OpCode.JMP:
            program_copy = list(program)
            op_copy = Op(OpCode.NOP, op.operand)
            program_copy[op_index] = op_copy
            yield program_copy
        else:
            # Other instructions are not flipped
            pass


def main():
    with open('./input.txt') as f:
        lines = f.readlines()
        program = [parse_op(line) for line in lines]

    vm = VM()
    vm.execute(program)
    print(f"Accumulator before the loop: {vm.accumulator}")

    for mutated_program in iter_flipped_nop_jmp(program):
        vm = VM()
        try:
            vm.execute(mutated_program, onloop='raise')
        except InfiniteLoopError:
            # Skip this one, we're searching for the program without loops
            continue

        print(f"Found a modification without a loop, accumulator: {vm.accumulator}")


if __name__ == "__main__":
    main()
