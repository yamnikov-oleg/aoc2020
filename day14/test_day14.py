import pytest

from day14 import (VM, Instruction, Mask, SetMaskInstruction,
                   SetMemoryInstruction, parse_instruction, parse_mask)


def test_parse_mask():
    assert parse_mask("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X") == Mask(
        zeroes=0b111111111111111111111111111111111101,
        ones=0b000000000000000000000000000001000000,
        floating_bits=[0, 2, 3, 4, 5, *range(7, 36)],
    )


def test_mask_apply():
    mask = parse_mask("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X")
    assert mask.apply(11) == 73
    assert mask.apply(101) == 101
    assert mask.apply(0) == 64


@pytest.mark.parametrize("mask,address,result", [
    ("000000000000000000000000000000X1001X", 42, [26, 27, 58, 59]),
    ("00000000000000000000000000000000X0XX", 26, [16, 17, 18, 19, 24, 25, 26, 27]),
])
def test_mask_apply_v2(mask, address, result):
    assert parse_mask(mask).apply_v2(address) == result


@pytest.mark.parametrize("line,instruction", [
    (
        "mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X",
        SetMaskInstruction(mask=parse_mask("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X")),
    ),
    (
        "mem[8] = 11",
        SetMemoryInstruction(address=8, value=11),
    ),
])
def test_parse_instruction(line: str, instruction: Instruction):
    assert parse_instruction(line) == instruction


def test_set_mask_instruction():
    vm = VM()
    instruction = SetMaskInstruction(mask=parse_mask("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X"))
    instruction.execute(vm)

    assert vm.mask == parse_mask("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X")


def test_set_mask_instruction_v2():
    vm = VM()
    instruction = SetMaskInstruction(mask=parse_mask("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X"))
    instruction.execute_v2(vm)

    assert vm.mask == parse_mask("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X")


def test_set_memory_instruction():
    vm = VM(mask=parse_mask("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X"))
    instruction = SetMemoryInstruction(address=8, value=11)
    instruction.execute(vm)

    assert vm.memory == {8: 73}


def test_set_memory_instruction_v2():
    vm = VM(mask=parse_mask("000000000000000000000000000000X1001X"))
    instruction = SetMemoryInstruction(address=42, value=100)
    instruction.execute_v2(vm)

    assert vm.memory == {26: 100, 27: 100, 58: 100, 59: 100}
