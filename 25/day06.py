import bisect
from pathlib import Path
from typing import Any, List, Dict, Set, Tuple
from collections import defaultdict
from itertools import product, permutations, combinations
# product gets every pairing
#   permutations excludes (self, self)
#   combinations excludes ordering
from tqdm import tqdm
import operator
from functools import reduce

import aoc


day = Path(__file__).stem


sym2op = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}


class Math:

    def __init__(self, values, sym) -> None:
        self.values = [int(v) for v in values]
        self.op = sym2op[sym]

    def solve(self):
        return reduce(self.op, self.values)
        

class Cephalomath1:

    def __init__(self, data: List[List[str]]):
        self.maths:List[Math] = []
        cols = list(zip(*data))
        for col in cols:
            self.maths.append(Math(col[0:-1], col[-1]))

    def solve(self):
        return sum(m.solve() for m in self.maths)

def get(day:int, test=False):
    name = f'{day}' + ('_test' if test else '')
    data = (aoc.data_path / f'{name}.txt').open().read().split('\n')
    return data


@aoc.part
def part1(data, expected = ...) -> int:
    data = [r.strip().split() for r in data]
    c = Cephalomath1(data)
    return c.solve()


@aoc.part
def part2(data, expected = ...) -> int:
    ncol = len(data[0])
    values, syms = data[0:-1], data[-1]
    p = ncol-1
    s = 0

    while p > 0:
        vs = []
        sym = ' '
        while sym == ' ':
            v = int(''.join([r[p] for r in values]))
            vs.append(v)
            sym = syms[p]
            p -= 1
        s += reduce(sym2op[sym], vs)
        p -= 1
    return s


if __name__ == '__main__': 
    data_test, data = get(day, test=True), get(day)
    part1(data_test, expected = 4277556)
    part1(data, expected = 5667835681547) 
    
    part2(data_test, expected = 3263827)
    part2(data, expected=9434900032651)
