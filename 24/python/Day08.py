from pathlib import Path
from typing import *
from collections import defaultdict
from itertools import combinations
import operator as ops

data_path = Path(__file__).absolute().parents[1] / 'data'
day = Path(__file__).stem

DEBUG = False


def debug(s:str):
    if DEBUG:
        print(s)


def read_input(name:str) -> List[List[str]]:
    return [list(row) for row in (data_path / f'{name}.txt').open().read().strip().split('\n')]


class P:

    limx = None
    limy = None

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return P(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return P(self.x - other.x, self.y - other.y)

    def __repr__(self): 
        return f'P({self.x}, {self.y})'
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)
    
    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)
    
    @property
    def in_bounds(self) -> bool:
        return (0 <= self.x < self.limx) and (0 <= self.y < self.limy)


class ARR:
    # for debugging
    arr=None

    def __init__(self, arr):
        self.arr = arr

    @property
    def pa(self):
        # print array
        for row in self.arr:
            print(''.join(row))

    def pp(self, ps:List[P]):
        # print points
        for row in self.arr:
            print(''.join(['X' if P(x,y) in ps else v for x,v in enumerate(row)]))


class A:

    def __init__(self, sym:str, p:P):
        self.sym = sym
        self.p = p

    def __repr__(self):
        return f'A({self.sym} {self.p.x} {self.p.y})'
    
    def __hash__(self) -> int:
        return hash((self.sym, self.p.x, self.p.y))
    

def get_antipodes(a1:A, a2:A, harmonics=False) -> Tuple[P, P]:
    d12 = a1.p - a2.p
    if not harmonics:
        return (a1.p + d12, a2.p - d12)
    else:
        aps = set({a1.p, a2.p})
        for a, op in ((a1, ops.add), (a2, ops.sub)):
            ap = a.p
            while True:
                ap = op(ap, d12)
                if not ap.in_bounds:
                    break
                aps.add(ap)
        return aps


def part1(arr:List[str], harmoincs=False) -> int:
    """Total unique antipodes"""
    P.limx = len(arr[0])
    P.limy = len(arr)
    antennas = []
    sym2a = defaultdict(set)
    for y, row in enumerate(arr):
        for x, v in enumerate(row):
            if v != '.':
                antenna = A(v, P(x,y))
                antennas.append(antenna)
                sym2a[v] |= {antenna}
    antipodes = set()
    for sym, symas in sorted(sym2a.items(), key=lambda x: x[1]):
        for pair in combinations(symas, 2):
            aps = {*get_antipodes(*pair, harmonics=harmoincs)}
            for ap in aps:
                if ap.in_bounds:
                    arr[ap.y][ap.x] = '#' if arr[ap.y][ap.x] == '.' else '!'
            antipodes |= aps
    antipodes_within = sorted([p for p in antipodes if p.in_bounds])  # sort for debugging
    return len(antipodes_within)


def part2(arr:List[str]) -> int:
    return part1(arr, harmoincs=True)


if __name__ == '__main__':
    input_test = read_input(f'{day}_test')
    a = ARR(input_test)
    assert part1(input_test) == 14
    print(part1(read_input(day)))
    assert part2(input_test) == 34  # 29
    print(part2(read_input(day)))
