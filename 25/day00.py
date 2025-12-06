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


def get(day:int, test=False):
    name = f'{day}' + ('_test' if test else '')
    return (aoc.data_path / f'{name}.txt').open().read().strip().split('\n')


@aoc.part
def part1(data, expected = None) -> int:

    answer = ...
    return answer


@aoc.part
def part2(data, expected = None) -> int:

    answer = ...
    return answer


if __name__ == '__main__': 
    data_test, data = get(day, test=True), get(day)
    part1(data_test, expected = ...)
    part1(data)
    
    part2(data_test, expected = ...)
    part2(data)
