import pytest

from day8 import (VM, InfiniteLoopError, Op, OpCode, iter_flipped_nop_jmp,
                  parse_op)


def test_parse_op():
    assert parse_op("nop +0") == Op(OpCode.NOP, 0)
    assert parse_op("acc +3") == Op(OpCode.ACC, 3)
    assert parse_op("acc -3") == Op(OpCode.ACC, -3)
    assert parse_op("jmp -99") == Op(OpCode.JMP, -99)


def test_execute_until_loop():
    program = [
        Op(OpCode.NOP),
        Op(OpCode.ACC, 1),
        Op(OpCode.JMP, 4),
        Op(OpCode.ACC, 3),
        Op(OpCode.JMP, -3),
        Op(OpCode.ACC, -99),
        Op(OpCode.ACC, 1),
        Op(OpCode.JMP, -4),
        Op(OpCode.ACC, 6),
    ]
    vm = VM()
    vm.execute(program)
    assert vm.accumulator == 5


def test_execute_raise_on_loop():
    program = [
        Op(OpCode.NOP),
        Op(OpCode.ACC, 1),
        Op(OpCode.JMP, 4),
        Op(OpCode.ACC, 3),
        Op(OpCode.JMP, -3),
        Op(OpCode.ACC, -99),
        Op(OpCode.ACC, 1),
        Op(OpCode.JMP, -4),
        Op(OpCode.ACC, 6),
    ]
    vm = VM()
    with pytest.raises(InfiniteLoopError):
        vm.execute(program, onloop='raise')


def test_execute_no_loop():
    program = [
        Op(OpCode.NOP),
        Op(OpCode.ACC, 1),
        Op(OpCode.JMP, 4),
        Op(OpCode.ACC, 3),
        Op(OpCode.JMP, -3),
        Op(OpCode.ACC, -99),
        Op(OpCode.ACC, 1),
        Op(OpCode.NOP, -4),
        Op(OpCode.ACC, 6),
    ]
    vm = VM()
    # Should not raise
    vm.execute(program, onloop='raise')


def test_iter_flipped_nop_jmp():
    program = [
        Op(OpCode.NOP),
        Op(OpCode.ACC, 1),
        Op(OpCode.JMP, 4),
        Op(OpCode.ACC, 3),
        Op(OpCode.JMP, -3),
    ]
    flipped_clones = list(iter_flipped_nop_jmp(program))

    assert len(flipped_clones) == 3
    assert flipped_clones[0] == [
        Op(OpCode.JMP, 0),
        Op(OpCode.ACC, 1),
        Op(OpCode.JMP, 4),
        Op(OpCode.ACC, 3),
        Op(OpCode.JMP, -3),
    ]
    assert flipped_clones[1] == [
        Op(OpCode.NOP),
        Op(OpCode.ACC, 1),
        Op(OpCode.NOP, 4),
        Op(OpCode.ACC, 3),
        Op(OpCode.JMP, -3),
    ]
    assert flipped_clones[2] == [
        Op(OpCode.NOP),
        Op(OpCode.ACC, 1),
        Op(OpCode.JMP, 4),
        Op(OpCode.ACC, 3),
        Op(OpCode.NOP, -3),
    ]
