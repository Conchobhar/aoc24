from pathlib import Path
from typing import *
from typing import Any
from collections import defaultdict
from itertools import product, permutations, combinations
# product gets every pairing
#   permutations excludes (self, self)
#   combinations excludes ordering

from tqdm import tqdm
import bisect

data_path = Path(__file__).absolute().parents[1] / 'data'
day = Path(__file__).stem


def prog_print(s:str):
    print(f"{s}", end='\r', flush=True)


def debug(s:str):
    if DEBUG:
        print(s)


def read_input(name:str) -> List[str]:
    return (data_path / f'{name}.txt').open().read().strip().split('\n')


def part1(input) -> int:
    return ...


def part2(input) -> int:
    return ...


if __name__ == '__main__':
    DEBUG = False
    input_test = read_input(f'{day}_test')
    assert part1(input_test) == ...
    print(part1(read_input(day)))
    assert part2(input_test) == ...
    print(part2(read_input(day)))
