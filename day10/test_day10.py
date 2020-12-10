from day10 import count_jolt_diffs, count_adapter_arrangements


def test_count_jolt_diffs():
    assert count_jolt_diffs([
        16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4,
    ]) == {1: 7, 2: 0, 3: 5}

    assert count_jolt_diffs([
        28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19,
        38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3,
    ]) == {1: 22, 2: 0, 3: 10}


def test_count_adapter_arrangements():
    assert count_adapter_arrangements([
        16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4,
    ]) == 8

    assert count_adapter_arrangements([
        28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19,
        38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3,
    ]) == 19208
