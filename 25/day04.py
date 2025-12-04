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
    return [list(row) for row in (aoc.data_path / f'{name}.txt').open().read().strip().split('\n')]


def part1(data) -> int:
    g = aoc.Grid(data)
    t = 0
    for p in g.valid_points():
        if g[p] == '@':
            s = sum(g.get_oob(p+dp) == '@' for dp in aoc.deltas_8)
            if s < 4:
                t += 1
    return t


def part2(data) -> int:
    g = aoc.Grid(data)
    t = 0
    ptc = set(g.valid_points())
    while ptc:
        p = ptc.pop()
        if g[p] == '@':
            s = sum(g.get_oob(p+dp) == '@' for dp in aoc.deltas_8)
            if s < 4:
                t += 1
                g[p] = 'x'
                points_to_recheck = {ap for ap in p.adjacent_8 if ap.in_bounds and ap not in ptc}
                ptc |= points_to_recheck
    return t


if __name__ == '__main__': 
    data_test = read_input(f'{day}_test')
    assert part1(data_test) == 13, part1(data_test)
    print(part1(read_input(day)))
    assert part2(data_test) == 43, part2(data_test)
    print(part2(read_input(day)))
