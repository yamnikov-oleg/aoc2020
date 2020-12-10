from typing import Dict, List


def count_jolt_diffs(seq: List[int]) -> Dict[int, int]:
    """
    Given a list of numbers, sorts it and returns a count for each time
    a difference between two consequent numbers is 1, 2 or 3.

    Inserts a zero and a number bigger than the sequence's maximum by 3
    beforehand.

    Raises ValueError if there is a difference different from 1, 2 or 3.
    """
    count = {1: 0, 2: 0, 3: 0}

    # Make a copy
    seq = list(seq)
    seq.append(0)
    seq.sort()
    seq.append(seq[-1] + 3)

    for i in range(len(seq) - 1):
        number1 = seq[i]
        number2 = seq[i + 1]

        diff = number2 - number1
        if diff < 1 or diff > 3:
            raise ValueError(
                f"Different between {number1} and {number2} "
                f"is {diff}"
            )

        count[diff] += 1

    return count


def count_adapter_arrangements(seq: List[int]) -> int:
    """
    Returns the number of arrangements this sequence of adapters can have.

    count_adapter_arrangements([16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4])  # => 8
    """
    cache = {}

    def _count_adapter_arrangements(subseq: List[int]) -> int:
        """
        Recursive function which counts arrangements of a sorted subsequence
        of adapters. The first (input) and final (output) jolt values must be
        included if they need to be counted.

        Uses memoization. Stores the results in `cache` using the first element
        of subseq as a key.

        _count_adapter_arrangements([0, 1, 4, 5, 6, 7, 10, 11, 12, 15, 16, 19, 22])  # => 8
        _count_adapter_arrangements([7, 10, 11, 12, 15, 16, 19, 22])  # => 2
        """
        cache_key = subseq[0]
        if cache_key in cache:
            return cache[cache_key]

        # Recursion termination condition.
        # There is only one arrangement for a single port.
        if len(subseq) == 1:
            return 1

        # To count the number of all possible arrangements, we compare
        # the initial value of the sequence (the reference) to each next value.
        #
        #   [4, 5, 6, 7, 10, 11, 12, 15, 16, 19, 22]
        #   4 is used as a reference and compared to 5, 6, 7 etc.
        #
        # If these adapters can be connected together (i.e. the difference
        # between their joltages is <=3), we recursively count how many
        # arrangments can the sequence have starting with the second adapter
        # of our choice.
        #
        #   [4, 5, 6, 7, 10, 11, 12, 15, 16, 19, 22]
        #   4 can be connected to 5. Add all arrangements of [5, 6, ...] to the count.
        #   4 can be connected to 6. Add all arrangements of [6, 7, ...] to the count.
        #   4 can be connected to 7 too. Add all arrangements of [7, 10, ...] to the count.
        #   4 can not be connected to 10. Stop here.
        #
        ref_value = subseq[0]
        count = 0
        for next_index, next_value in enumerate(subseq):
            # Skip the first value - it's the reference
            if next_index == 0:
                continue

            diff = next_value - ref_value
            if diff <= 3:
                count += _count_adapter_arrangements(subseq[next_index:])
            else:
                break

        cache[cache_key] = count

        return count

    # Make a copy
    seq = list(seq)
    seq.append(0)
    seq.sort()
    seq.append(seq[-1] + 3)

    return _count_adapter_arrangements(seq)


def main():
    with open('./input.txt') as f:
        lines = f.readlines()
        numbers = [int(l.strip()) for l in lines]

    diff_count = count_jolt_diffs(numbers)
    print(f"Diff counts: {diff_count}")
    print(f"Part 1 answer: {diff_count[1] * diff_count[3]}")

    arrangements_count = count_adapter_arrangements(numbers)
    print(f"Possible arrangements: {arrangements_count}")


if __name__ == "__main__":
    main()
