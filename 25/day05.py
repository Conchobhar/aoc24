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

class Ranger:

    def __init__(self, data) -> None:
        ranges = set() # set of non overlaping ranges
        for d in data:
            l, u = [int(x) for x in d.split('-')]
            r = range(l, u+1)
            ranges_new = set()
            for ar in ranges:
                if r.start > ar.stop or r.stop < ar.start:
                    ranges_new.add(ar)
                    continue # non overlapping
                r = range(min(r.start, ar.start), max(r.stop, ar.stop))
            ranges_new.add(r)
            ranges = ranges_new
        self.ranges = ranges

    def contains_simple(self, i):
        for r in self.ranges:
            if i in r:
                aoc.debug(f"{i=} is True")
                return True
        aoc.debug(f"{i=} is False")
        return False


def read_input(name:str):
    rs, ids = (aoc.data_path / f'{name}.txt').open().read().strip().split('\n\n')
    return rs.split('\n'), [int(x) for x in ids.split('\n')]


def part1(rs, ids) -> int:
    ranger = Ranger(rs)
    return sum(ranger.contains_simple(i) for i in ids)


def part2(rs, _) -> int:
    ranger = Ranger(rs)
    return sum([r.stop-r.start for r in ranger.ranges])


if __name__ == '__main__': 
    data_test = read_input(f'{day}_test')
    assert part1(*data_test) == 3, part1(*data_test)
    print(part1(*read_input(day)))  # 664
    assert part2(*data_test) == 14, part2(*data_test)
    print(part2(*read_input(day)))  # 350780324308385
