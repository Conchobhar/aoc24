import bisect
from pathlib import Path
from typing import Any, Generator, List, Dict, Set, Tuple
from collections import defaultdict
from itertools import product, permutations, combinations
# product gets every pairing
#   permutations excludes (self, self)
#   combinations excludes ordering
from tqdm import tqdm

import aoc



day = Path(__file__).stem

def chunk_string(s, n):
    for i in range(n, len(s), n):
        yield s[i:i+n]


class Validator:
    """Validator"""

    def __init__(self, d):
        self.invalid = []
        self.d = d

    @property
    def values(self) -> Generator[int]:
        for r in self.d:
            lo, hi = r.split('-')
            yield from range(int(lo), int(hi)+1)


    def get_simple_invalids(self):
        for v in self.values:
            sv = str(v)
            lsv = len(sv)
            if sv[0:lsv//2] == sv[lsv//2:]:
                self.invalid.append(v)

    def get_invalids(self):
        """Iterate over all valid repeating window sizes
        For a given window, check all chunks it looks over are the same
        Otherwise, increase the window
        """
        for v in self.values:
            sv = str(v)
            lsv = len(sv)
            w = 1
            while w < lsv:
                s = sv[0:w]
                if lsv % w == 0:  # check for this window size if it fits without remainder into the string, else skip to next
                    if all(s == chunk for chunk in chunk_string(sv, w)):  # if all views are the same, id is invalid
                        self.invalid.append(v)
                        break
                w += 1


def read_input(name:str):
    d = (aoc.data_path / f'{name}.txt').open().read().strip()
    return d.split(',')


def part1(data) -> int:
    val = Validator(data)
    val.get_simple_invalids()
    v =  sum(val.invalid)
    return v


def part2(data) -> int:
    val = Validator(data)
    val.get_invalids()
    v = sum(val.invalid)
    print(v)
    return v


if __name__ == '__main__':
    data_test = read_input(f'{day}_test')
    assert part1(data_test) == 1227775554
    print(part1(read_input(day)))  # 30323879646
    assert part2(data_test) == 4174379265
    print(part2(read_input(day)))  # 43872163557
