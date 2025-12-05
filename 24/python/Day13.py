import argparse
from functools import cache
from pathlib import Path
from typing import *
from typing import Any
import numpy as np
from collections import defaultdict
from itertools import product, permutations, combinations
# product gets every pairing
#   permutations excludes (self, self)
#   combinations excludes ordering
from tqdm import tqdm
import bisect

import aoc


day = Path(__file__).stem


class System:

    def __init__(self,ax,ay,bx,by,tx,ty) -> None:
        self.ax = ax
        self.ay = ay
        self.bx = bx
        self.by = by
        self.tx = tx
        self.ty = ty

    @cache
    def solve(self) -> Tuple[float, float]:
        inmat = np.array([[self.ax, self.bx], [self.ay, self.by]])
        outmat = np.array([self.tx, self.ty])
        return np.linalg.solve(inmat, outmat)
    
    @property
    def a(self) -> float:
        return self.solve()[0].round(3)
    
    @property
    def b(self) -> float:
        return self.solve()[1].round(3)

    def solvable(self):
        '''test solutions from solve are ints to 3 decimal places'''
        return self.a.is_integer() and self.b.is_integer()
    
    def tokens(self) -> int:
        if self.solvable():
            return int(self.a)*3 + int(self.b)*1
        else:
            raise ValueError('System is not solvable')
        


def read_input(name:str) -> List[System]:
    systems = []
    for system in (aoc.data_path / f'{name}.txt').open().read().strip().split('\n\n'):
        a, b, total = system.split('\n')
        ax, ay = [int(v.strip()[2::]) for v in a[10::].split(',')]
        bx, by = [int(v.strip()[2::]) for v in b[10::].split(',')]
        tx, ty = [int(v.strip()[2::]) for v in total[7::].split(',')]
        systems.append(System(ax,ay,bx,by,tx,ty))
    return systems


def part1(systems) -> int:
    solutions = []
    for s in systems:
        if s.solvable():
            solutions.append( s.tokens())
    return sum(solutions)


def part2(systems) -> int:
    solutions = []
    for s in systems:
        if s.solvable():
            solutions.append( s.tokens())
    return sum(solutions)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()
    if args.debug:
        aoc.Debug.set = True

    input_test = read_input(f'{day}_test1')
    s1 = input_test[0]
    assert s1.solvable()
    # s1.tokens() == 280
    assert part1(input_test) == 480
    print(part1(read_input(day)))
    input_part2 = read_input(f'{day}')
    input_testpart2 = read_input(f'{day}_test1')

    for s in input_part2+input_testpart2:
        s.tx += 10000000000000
        s.ty += 10000000000000
    assert [s.solvable() for s in input_testpart2] == [False, True, False, True]
    print(part2(input_part2))  # 36942521895712  too low
