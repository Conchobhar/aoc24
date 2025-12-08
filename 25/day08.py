import bisect
from functools import reduce
import operator
from pathlib import Path
import string
from typing import Any, List, Dict, Set, Tuple
from collections import defaultdict
from itertools import islice, product, permutations, combinations
# product gets every pairing
#   permutations excludes (self, self)
#   combinations excludes ordering
from tqdm import tqdm
fset = frozenset

import aoc


day = Path(__file__).stem


def get(day:int, test=False):
    name = f'{day}' + ('_test' if test else '')
    return (aoc.data_path / f'{name}.txt').open().read().strip().split('\n')


class P3:

    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.c: Circut = None

    def dist(self, other):
        return (self.x-other.x)**2 + (self.y-other.y)**2 + (self.z-other.z)**2

    def __repr__(self): 
        # Map hash to 3-letter code
        h = abs(hash(self))  # ensure positive
        letters = string.ascii_uppercase
        code = ''.join(letters[(h // (26 ** i)) % 26] for i in range(3))
        return f'P([{code}]'
    
        # return f'P({self.x}, {self.y}, {self.z})'

    def stable_hash(self):
        # Use a stable hash (e.g., tuple hash or custom)
        return (self.x * 73856093) ^ (self.y * 19349663) ^ (self.z * 83492791)
    
    def __hash__(self) -> int:
        return self.stable_hash()
    
    def __lt__(self, other):
        return (self.x, self.y, self.z) < (other.x, other.y, other.z)
    
    def __eq__(self, other):
        return (self.x, self.y, self.z) == (other.x, other.y, other.z)
    

class Circut:

    cid = 0

    def __init__(self, l=None) -> None:
        l = [] if l is None else l
        self.ps = fset(l)
        self.cid = self.getcid()

    def getcid(self):
        """Assign unique enumerated ID"""
        cid = Circut.cid
        Circut.cid += 1
        return cid

    def __repr__(self) -> str:
        return f"Circut(cid={self.cid}, {[p.__repr__() for p in self.ps]})"
    
    def combine(self, other: "Circut"):
        """Merge two circuts, all points from other get assigned this circut, which gains others points"""
        for p in other.ps:
            p.c = self
        self.ps = fset(list([*self.ps, *other.ps]))

@aoc.part
def part1(data) -> int:
    size = 10 if len(data) == 20 else 1000  # test vs actual problem
    ps = []  # all points
    pd = {}  # point 2 other points 2 dist
    d2pair = []  # ordered dist 2 point tuples
    d2pair_seen = set()
    cs = {}
    for r in tqdm(data):
        p = P3(*map(int, r.split(',')))
        p.c = Circut([p])
        ps.append(p)
        pd[p] = {}
        for po in pd:
            if po != p:
                d = p.dist(po)
                pd[p][po] = d
                pair = tuple(sorted((p, po)))
                if pair not in d2pair_seen:
                    bisect.insort(d2pair, (d, pair), key=lambda x: x[0])
                    d2pair_seen.add(pair)
    for d, (p1, p2) in tqdm(d2pair[:size]):  # for pairs in sorted order of distance
        aoc.debug(p1, p2)
        if p2.c.cid in cs:
            del cs[p2.c.cid]
        p1.c.combine(p2.c)
        cs[p1.c.cid] = p1.c
    answer = [len(c.ps) for c in cs.values() if len(c.ps) > 1]
    return reduce(operator.mul ,sorted(answer, reverse=True)[:3])


@aoc.part
def part2(data) -> int:
    ps = []  # all points
    pd = {}  # point 2 other points 2 dist
    d2pair = []  # ordered dist 2 point tuples
    d2pair_seen = set()
    cs = {}
    for r in tqdm(data):
        p = P3(*map(int, r.split(',')))
        p.c = Circut([p])
        ps.append(p)
        pd[p] = {}
        for po in pd:
            if po != p:
                d = p.dist(po)
                pd[p][po] = d
                pair = tuple(sorted((p, po)))
                if pair not in d2pair_seen:
                    bisect.insort(d2pair, (d, pair), key=lambda x: x[0])
                    d2pair_seen.add(pair)
    for d, (p1, p2) in tqdm(d2pair):  # for pairs in sorted order of distance
        aoc.debug(p1, p2)
        if p2.c.cid in cs:
            del cs[p2.c.cid]
        p1.c.combine(p2.c)
        if len(p1.c.ps) == len(ps):
            return p1.x * p2.x
        cs[p1.c.cid] = p1.c
    # answer = [len(c.ps) for c in cs.values() if len(c.ps) > 1]
    # return reduce(operator.mul ,sorted(answer, reverse=True)[:3])


if __name__ == '__main__': 
    data_test, data = get(day, test=True), get(day)
    part1(data_test, 40)
    part1(data, 97384)
    
    part2(data_test, 25272)
    part2(data, 9003685096)
