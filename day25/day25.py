from itertools import count


def transform_subject(subject_number: int, loop_size: int) -> int:
    value = 1
    for i in range(loop_size):
        value *= subject_number
        value %= 20201227
    return value


def find_loop_size(public_key: int) -> int:
    subject_number = 7
    value = 1
    for loop_size in count(1):
        value *= subject_number
        value %= 20201227

        if value == public_key:
            return loop_size


def make_encryption_key(remote_public_key: int, own_loop_size: int) -> int:
    return transform_subject(remote_public_key, own_loop_size)


def main():
    DOOR_PUBLIC_KEY = 9789649
    CARD_PUBLIC_KEY = 3647239

    door_loop_size = find_loop_size(DOOR_PUBLIC_KEY)
    enc_key = make_encryption_key(CARD_PUBLIC_KEY, door_loop_size)
    print(f"Encryption key: {enc_key}")


if __name__ == "__main__":
    main()
