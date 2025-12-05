import argparse
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

import aoc


day = Path(__file__).stem


def read_input(name:str):
    return (aoc.data_path / f'{name}.txt').open().read().strip().split('\n')


def part1(input) -> int:
    return ...


def part2(input) -> int:
    return ...


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()
    if args.debug:
        aoc.Debug.set = True
        
    input_test = read_input(f'{day}_test')
    assert part1(input_test) == ...
    print(part1(read_input(day)))
    assert part2(input_test) == ...
    print(part2(read_input(day)))
