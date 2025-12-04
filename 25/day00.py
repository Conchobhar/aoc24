import bisect
from pathlib import Path
from typing import Any, List, Dict, Set, Tuple
from collections import defaultdict
from itertools import product, permutations, combinations
# product gets every pairing
#   permutations excludes (self, self)
#   combinations excludes ordering
from tqdm import tqdm

import aoc


day = Path(__file__).stem


def read_input(name:str):
    return (aoc.data_path / f'{name}.txt').open().read().strip().split('\n')


def part1(data) -> int:
    return ...


def part2(data) -> int:
    return ...


if __name__ == '__main__': 
    data_test = read_input(f'{day}_test')
    assert part1(data_test) == ..., part1(data_test)
    print(part1(read_input(day)))
    assert part2(data_test) == ..., part2(data_test)
    print(part2(read_input(day)))
