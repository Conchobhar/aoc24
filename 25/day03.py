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
    batts = []
    for bank in data:
        bb, bs = bank[-2], bank[-1]
        bsc = '1'
        for v in reversed(bank[:-2]):
            if v >= bb:
                bs = max(bb, bs, bsc)
                bb = v
            else:
                if v > bs:
                    bsc = v
        batts.append(int(bb+bs))
    return sum(batts)


def part2(data) -> int:
    batts = []
    for bank in data:
        rbank = list(((v,i) for i, v in enumerate(reversed(bank))))
        lb = rbank[:12]  # contain (idx, value) tuples for points
        si, ei = 11, len(rbank)
        for ib in reversed(range(12)):
            m = max(rbank[si:ei+1], key=lambda x: (x[0], x[1],))
            lb[ib] = m
            si = lb[ib-1][1]
            ei = m[1]-1
        s = ''.join([str(b[0]) for b in reversed(lb)])
        aoc.debug("val", s)
        batts.append(int(s))
    return sum(batts)


if __name__ == '__main__': 
    data_test = read_input(f'{day}_test')
    assert part1(data_test) == 357, part1(data_test)
    print(part1(read_input(day)))
    assert part2(data_test) == 3121910778619, part2 (data_test)
    print(part2(read_input(day)))
