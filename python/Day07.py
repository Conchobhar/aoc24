from pathlib import Path
from typing import *
from typing import Any
from tqdm import tqdm

from itertools import repeat
import operator as ops

data_path = Path(__file__).absolute().parents[1] / 'data'
day = Path(__file__).stem

DEBUG = False


def debug(s:str):
    if DEBUG:
        print(s)


def read_input(name:str) -> Dict[int, List[int]]:
    d = {}
    for row in (data_path / f'{name}.txt').open().read().split('\n'):
        k, ns = row.split(':')
        ns = [int(v) for v in ns.strip().split(' ')]
        d[int(k)] = ns
    return d


class Concater:

    def __init__(self) -> None:
        pass

    def __call__(self, a:int, b:int) -> int:
        """Need to adhere to left to right evaluation. Since Combiner reverses input,
        we need to flip the order here as well
        """
        return int(str(b) + str(a))
    
    @property
    def __name__(self):
        return '||'


class Combiner:

    ops = (ops.add, ops.mul, Concater())

    def __init__(self, y:int, ns:List[int]):
        self.y = y
        # ops are applied left to right for problem, so we need to
        # reverse the list to work with the implementation
        self.ns = list(reversed(ns))

    def __repr__(self):
        return f'{self.y} {self.ns}'
    
    def __str__(self):
        return f'{self.y} {self.ns}'
    
    def _reduce(self, l:List[int], d=0):
        rs = []
        if len(l) > 1:
            for op in self.ops:
                debug("  "*d + f"{l[0]} {op.__name__} ...")
                for v in self._reduce(l[1:]):
                    r = op(l[0], v)
                    rs.append(r)
        else:
            rs = l
        return rs
    
    def find_solutions(self) -> List[int]:
        return self._reduce(self.ns)

    def has_solution(self) -> bool:
        return self.y in self.find_solutions()


def part1(d:Dict) -> int:
    s = 0
    for k, ns in tqdm(d.items()):
        c = Combiner(k, ns)
        if c.has_solution():
            s += k
    return s


def part2(d:Dict) -> int:
    s = 0
    for k, ns in tqdm(d.items()):
        c = Combiner(k, ns)
        if c.has_solution():
            s += k
    return s


if __name__ == '__main__':
    input_test = read_input(f'{day}_test')
    assert part1(input_test) == 3749
    print(part1(read_input(day)))
    assert part2(input_test) == 11387
    print(part2(read_input(day)))
