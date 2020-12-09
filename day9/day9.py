from typing import List, Iterable


def is_sum_of_two_numbers(number: int, pool: Iterable[int]) -> bool:
    """
    Returns True if the number is a sum of any two different numbers
    from the pool.
    """
    pool_set = set(pool)
    for summand in pool_set:
        if (number - summand) != summand and (number - summand) in pool_set:
            return True

    return False


def find_first_invalid_number(seq: List[int], lookbehind: int) -> int:
    """
    Returns the first number in the sequence which is not a sum of any
    two different numbers among the previous `lookbehind` numbers.

    Skips first `lookbehind` numbers from checking (the preamble).

    Raises ValueError if an invalid number was not found.
    """
    for index in range(lookbehind, len(seq)):
        sum_pool = seq[index-lookbehind:index]
        number = seq[index]
        if not is_sum_of_two_numbers(number, sum_pool):
            return number

    raise ValueError("All numbers are valid")


def find_contiguous_sum(seq: List[int], target: int) -> List[int]:
    """
    Returns a slice of the sequence which adds up to the target number.

    Raises ValueError if not such slice was found.
    """
    for start_index in range(len(seq)):
        for end_index in range(start_index + 2, len(seq)):
            range_sum = sum(seq[start_index:end_index])
            if range_sum < target:
                continue
            elif range_sum == target:
                return seq[start_index:end_index]
            elif range_sum > target:
                break

    raise ValueError("Could not find contiguous sum")


def main():
    with open('./input.txt') as f:
        lines = f.readlines()
        numbers = [int(l.strip()) for l in lines]

    first_invalid = find_first_invalid_number(numbers, 25)
    print(f"First invalid number: {first_invalid}")

    cont_sum = find_contiguous_sum(numbers, first_invalid)
    cont_sum.sort()
    weakness = cont_sum[0] + cont_sum[-1]
    print(f"The encryption weakness: {weakness}")


if __name__ == "__main__":
    main()
