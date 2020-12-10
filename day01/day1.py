def main():
    with open('./input.txt') as f:
        # Split the file into lines
        lines = f.read().split('\n')
        # Remove empty lines
        lines = [line.strip() for line in lines if line.strip()]
        # Convert each line to an int
        numbers = [int(line) for line in lines]

    for n1 in numbers:
        for n2 in numbers:
            if n1 + n2 == 2020:
                print("{n1} + {n2} = 2020; {n1} * {n2} = {mult}".format(
                    n1=n1, n2=n2, mult=n1*n2))

    for n1 in numbers:
        for n2 in numbers:
            for n3 in numbers:
                if n1 + n2 + n3 == 2020:
                    print("{n1} + {n2} + {n3} = 2020; {n1} * {n2} * {n3} = {mult}".format(
                    n1=n1, n2=n2, n3=n3, mult=n1*n2*n3))


if __name__ == "__main__":
    main()
