from dataclasses import dataclass
from typing import Dict, Iterator, Set, Tuple

Coords = Tuple[int, int, int]
Coords4 = Tuple[int, int, int, int]


@dataclass
class PocketDim:
    active_cubes: Set[Coords]

    def is_active(self, x: int, y: int, z: int) -> bool:
        return (x, y, z) in self.active_cubes

    def copy(self):
        return PocketDim(self.active_cubes.copy())

    def iter_neighbors(self, x: int, y: int, z: int) -> Iterator[Coords]:
        for nx in [x - 1, x, x + 1]:
            for ny in [y - 1, y, y + 1]:
                for nz in [z - 1, z, z + 1]:
                    if (nx, ny, nz) == (x, y, z):
                        continue

                    yield (nx, ny, nz)

    def step(self) -> 'PocketDim':
        """
        Returns a copy of this pocket dimension evolved by 1 step.
        """
        new_active_cubes = set()
        # Maps each inactive which can be potentially activated
        # to the number of active neighbors it has
        activation_candidates: Dict[Coords, int] = {}
        for x, y, z in self.active_cubes:
            neighbors_count = 0
            for nx, ny, nz in self.iter_neighbors(x, y, z):
                if self.is_active(nx, ny, nz):
                    neighbors_count += 1
                else:
                    activation_candidates.setdefault((nx, ny, nz), 0)
                    activation_candidates[(nx, ny, nz)] += 1

            if neighbors_count == 2 or neighbors_count == 3:
                new_active_cubes.add((x, y, z))

        for (x, y, z), neighbors_count in activation_candidates.items():
            if neighbors_count == 3:
                new_active_cubes.add((x, y, z))

        return PocketDim(new_active_cubes)


@dataclass
class PocketDim4:
    active_cubes: Set[Coords4]

    def is_active(self, x: int, y: int, z: int, w: int) -> bool:
        return (x, y, z, w) in self.active_cubes

    def copy(self):
        return PocketDim4(self.active_cubes.copy())

    def iter_neighbors(self, x: int, y: int, z: int, w: int) -> Iterator[Coords4]:
        for nx in [x - 1, x, x + 1]:
            for ny in [y - 1, y, y + 1]:
                for nz in [z - 1, z, z + 1]:
                    for nw in [w - 1, w, w + 1]:
                        if (nx, ny, nz, nw) == (x, y, z, w):
                            continue

                        yield (nx, ny, nz, nw)

    def step(self) -> 'PocketDim4':
        """
        Returns a copy of this pocket dimension evolved by 1 step.
        """
        new_active_cubes = set()
        # Maps each inactive which can be potentially activated
        # to the number of active neighbors it has
        activation_candidates: Dict[Coords4, int] = {}
        for x, y, z, w in self.active_cubes:
            neighbors_count = 0
            for nx, ny, nz, nw in self.iter_neighbors(x, y, z, w):
                if self.is_active(nx, ny, nz, nw):
                    neighbors_count += 1
                else:
                    activation_candidates.setdefault((nx, ny, nz, nw), 0)
                    activation_candidates[(nx, ny, nz, nw)] += 1

            if neighbors_count == 2 or neighbors_count == 3:
                new_active_cubes.add((x, y, z, w))

        for (x, y, z, w), neighbors_count in activation_candidates.items():
            if neighbors_count == 3:
                new_active_cubes.add((x, y, z, w))

        return PocketDim4(new_active_cubes)


def parse_pocket_dim(content: str) -> PocketDim:
    content = content.strip()

    active_cubes = set()
    for line_ix, line in enumerate(content.split('\n')):
        line = line.strip()
        for char_ix, char in enumerate(line):
            if char == '.':
                continue
            elif char == '#':
                active_cubes.add((char_ix, line_ix, 0))
            else:
                raise ValueError(f"Invalid pocket dimension char: {char!r}")

    return PocketDim(active_cubes)


def parse_pocket_dim4(content: str) -> PocketDim4:
    content = content.strip()

    active_cubes = set()
    for line_ix, line in enumerate(content.split('\n')):
        line = line.strip()
        for char_ix, char in enumerate(line):
            if char == '.':
                continue
            elif char == '#':
                active_cubes.add((char_ix, line_ix, 0, 0))
            else:
                raise ValueError(f"Invalid pocket dimension char: {char!r}")

    return PocketDim4(active_cubes)


def main():
    with open('./input.txt') as f:
        contents = f.read()
        original_dim = parse_pocket_dim(contents)
        original_dim4 = parse_pocket_dim4(contents)

    dim = original_dim
    for i in range(6):
        dim = dim.step()
    print(f"Active cubes after 6 steps: {len(dim.active_cubes)}")

    dim4 = original_dim4
    for i in range(6):
        dim4 = dim4.step()
    print(f"Active hyper-cubes after 6 steps: {len(dim4.active_cubes)}")


if __name__ == "__main__":
    main()
