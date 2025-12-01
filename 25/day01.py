import argparse
from pathlib import Path
from typing import *
from typing import Any
from collections import defaultdict
from itertools import product, permutations, combinations
# product gets every pairing
#   permutations excludes (self, self)
#   combinations excludes ordering
from tqdm import tqdm
from operator import add, sub

import aoc


day = Path(__file__).stem


class Safe:
    """Safe"""

    N = 100  # No. numbers on dial

    def __init__(self) -> None:
        self.p = 50  # starting position
        self.zero_count = 0  # times landed on zero
        self.zero_passes = 0  # times went past zero

    def turn(self, t:str):
        """Turn the dial
        cases
            n < N
                may cross zero once
            n == N
                will cross zero once
            n > N
                will cross zero >= 1
        """
        d, n = t[0], int(t[1:])
        op = add if d == 'R' else sub
        cycles = n // self.N  # how many complete cycles round will this take us
        p_next = op(self.p, n % self.N)  # only need to consider the remainder via mod
        will_pass_zero = self.p != 0 and (p_next <= 0 or p_next >= 100)
        self.zero_passes += cycles + (1 if will_pass_zero else 0)
        self.p =  p_next % self.N  # update position
        self.zero_count += 1 if self.p == 0 else 0  # update on-zero count
        aoc.debug(f"{d=}, {n=}, {self.p=}, {p_next=}, {self.zero_passes=}, {cycles=}, {will_pass_zero=},")


def read_input(name:str):
    return (aoc.data_path / f'{name}.txt').open().read().strip().split('\n')


def part1(data) -> int:
    s = Safe()
    for d in data:
        s.turn(d)
    return s.zero_count


def part2(data) -> int:
    s = Safe()
    for d in data:
        s.turn(d)
    return s.zero_passes


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()
    aoc.Debug.set = args.debug

    input_test = read_input(f'{day}_test')
    assert part1(input_test) == 3
    print(part1(read_input(day)))  # 964
    assert part2(input_test) == 6
    print(part2(read_input(day)))
