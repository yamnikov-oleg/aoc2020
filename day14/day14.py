import re
from dataclasses import dataclass, field
from typing import DefaultDict, Dict, List


@dataclass
class Mask:
    # A mask in which bits that have to be overwritten to 0 are set to 0.
    # Other bits are to 1.
    # Applied using bitwise AND.
    zeroes: int = 0xFFFFFFFFF  # 36 bits by default
    # A mask in which bits that have to be overwritten to 1 are set to 1.
    # Other bits are to 0.
    # Applied using bitwise OR.
    ones: int = 0

    # Numbers of floating (X) bits in the mask.
    # 0 is the number of units bit - the right-most bit.
    # 35 is the number of the left-most bit in a 36-bit mask.
    floating_bits: List[int] = field(default_factory=list)

    def apply(self, number: int) -> int:
        return (number & self.zeroes) | self.ones

    def apply_v2(self, address: int) -> List[int]:
        # Set the ones
        address = address | self.ones

        def flip_bits(address: int, bits: List[int]) -> List[int]:
            """
            Returns all possible combinations of floating bits in the address.
            """
            if len(bits) == 0:
                return [address]

            target_bit = bits[0]
            address_zero = address & ~(1 << target_bit)
            address_one = address | (1 << target_bit)
            return [*flip_bits(address_zero, bits[1:]), *flip_bits(address_one, bits[1:])]

        return sorted(flip_bits(address, self.floating_bits))


def parse_mask(line: str) -> Mask:
    line = line.strip()

    zeroes = 0
    ones = 0
    floating_bits = []
    for index, char in enumerate(line):
        if char == '1':
            zeroes = 2 * zeroes + 1
            ones = 2 * ones + 1
        elif char == '0':
            zeroes = 2 * zeroes
            ones = 2 * ones
        elif char == 'X':
            zeroes = 2 * zeroes + 1
            ones = 2 * ones

            bit_number = len(line) - index - 1
            floating_bits.insert(0, bit_number)
        else:
            raise ValueError(f"Invalid mask char: {char!r}")

    return Mask(zeroes=zeroes, ones=ones, floating_bits=floating_bits)


@dataclass
class VM:
    mask: Mask = field(default_factory=Mask)
    memory: Dict[int, int] = field(default_factory=lambda: DefaultDict(int))


class Instruction:
    """
    Base class for all instructions.
    """
    def execute(self, vm: VM) -> None:
        """
        Executes the instruction on the given VM.
        Modifies VM in place.
        """
        raise NotImplementedError("execute")

    def execute_v2(self, vm: VM) -> None:
        """
        Executes the instruction on the given VM using v2 decoder emulation.
        Modifies VM in place.
        """
        raise NotImplementedError("execute_v2")


@dataclass
class SetMaskInstruction(Instruction):
    """
    Updates the mask of a VM to a given value.
    """
    mask: Mask

    def execute(self, vm: VM) -> None:
        """
        Sets the mask of the VM.
        """
        vm.mask = self.mask

    def execute_v2(self, vm: VM) -> None:
        """
        Sets the mask of the VM.
        """
        vm.mask = self.mask


@dataclass
class SetMemoryInstruction(Instruction):
    """
    Updates memory cells of a VM by the given address to the given value.
    """
    address: int
    value: int

    def execute(self, vm: VM) -> None:
        """
        Sets the memory value of the VM.
        """
        masked_value = vm.mask.apply(self.value)
        vm.memory[self.address] = masked_value

    def execute_v2(self, vm: VM) -> None:
        """
        Sets memory values in the VM.
        """
        for address in vm.mask.apply_v2(self.address):
            vm.memory[address] = self.value


def parse_instruction(line: str) -> Instruction:
    line = line.strip()

    set_mask_re = re.compile(r'^mask = ([X01]+)$')
    match = set_mask_re.match(line)
    if match:
        return SetMaskInstruction(mask=parse_mask(match.group(1)))

    set_memory_re = re.compile(r'^mem\[(\d+)\] = (\d+)$')
    match = set_memory_re.match(line)
    if match:
        return SetMemoryInstruction(address=int(match.group(1)), value=int(match.group(2)))

    raise ValueError(f"Invalid instruction {line!r}")


def main():
    with open("./input.txt") as f:
        lines = f.readlines()
        program = [parse_instruction(line) for line in lines]

    vm = VM()
    for instruction in program:
        instruction.execute(vm)

    memory_values_sum = sum(vm.memory.values())
    print(f"Some of values in memory: {memory_values_sum}")

    vm = VM()
    for instruction in program:
        instruction.execute_v2(vm)

    memory_values_sum = sum(vm.memory.values())
    print(f"Some of values in memory (v2): {memory_values_sum}")


if __name__ == "__main__":
    main()
