import argparse
from functools import reduce
from operator import mul
from pathlib import Path
import time
from typing import *
from typing import Any
from collections import defaultdict
from itertools import product, permutations, combinations
# product gets every pairing
#   permutations excludes (self, self)
#   combinations excludes ordering
from tqdm import tqdm
import bisect
import numpy as np
from matplotlib import pyplot as plt
import aoc
from aoc import P


day = Path(__file__).stem


def read_input(name:str) -> List[str]:
    """Input is like
    p=0,4 v=3,-3
    p=6,3 v=-1,-3
    """
    data = (aoc.data_path / f'{name}.txt').open().read().strip()
    rows = []
    for line in data.splitlines():
        p, v = line.split()
        p = P(*map(int, p.strip('p=').split(',')))
        v = P(*map(int, v.strip('v=').split(',')))
        rows.append((p, v))
    return rows


class Drones:

    def __init__(self, input: List[Tuple[P, P]]):
        self.parr = np.array([(p.x, p.y) for p, v in input])
        self.varr = np.array([(v.x, v.y) for p, v in input])
        self.parr_init = self.parr.copy()

    def evolve(self, nsteps):
        for n in range(nsteps):
            self.parr += self.varr
            self.parr %= [P.xlim, P.ylim]
        if np.all(self.parr == self.parr_init):
            print(f"Found repeat at {n}")

    def sym_score(self):
        """Some easy measures of order within the grid

        In practice center was the most useful, immediately revealing the step when plotted over steps
        """
        # reflection is the sum of the x-coordinates of the drones after reflection about the y-axis
        # idea is this should minimize with a highly symmetric image
        reflection = int(sum(self.parr - (P.xlim//2, 0))[0])
        # center is the sum of the Manhattan distances of the drones from the center of the grid
        # this should also minimize if the image is focused in the centre of the grid
        center = int(sum(sum(abs(self.parr - (P.xlim//2, P.ylim//2)))))
        return reflection, center
    
    def as_points(self):
        return [P(x, y) for x, y in self.parr]
    
    def print(self, save=False, dir='', n=0):
        grid = np.zeros([P.ylim, P.xlim], dtype=int)
        for p in self.parr:
            grid[p[1], p[0]] += 1
        # save imshow out to file for inspection
        plt.imshow(grid)
        if save:
            if not dir:
                plt.savefig(f'outs/out{n}.png')
            else:
                plt.savefig(f'{dir}/out{n}.png')
        print(grid)

    def __repr__(self):
        return f'Drones: {len(self)}'

    def __str__(self):
        return f'Drones: {len(self)}'

    def __len__(self):
        return len(self.parr)

    def __contains__(self, item):
        return item in self.parr


def part1(input) -> int:
    q = defaultdict(int)
    d = Drones(input)
    d.evolve(100)
    for p in d.as_points():
        if p.x < P.xlim // 2:
            if p.y < P.ylim // 2:
                q['tl'] += 1
            elif p.y > P.ylim // 2:
                q['bl'] += 1
        elif p.x > P.xlim // 2:
            if p.y < P.ylim // 2:
                q['tr'] += 1
            elif p.y > P.ylim // 2:
                q['br'] += 1
    d.print()
    return reduce(mul, q.values())


def part2(input):
    d = Drones(input)
    o = {}
    nsteps = 10000
    for step in range(1, nsteps):
        d.evolve(1)
        reflection, center = d.sym_score()
        o[step] = reflection, center
        if center < 15000:  # heuristic
            print(f"{step=}, {d.sym_score()=}")
            d.print(save=True, dir='python/', n=step)
    with open(f'out_{nsteps}.csv', 'w') as f:  # inspect in notebook
        for k, (v1, v2) in o.items():
            f.write(f'{k},{v1},{v2}\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()
    if args.debug:
        aoc.Debug.set = True
    P.ylim, P.xlim = 7, 11
    input_test = read_input(f'{day}_test')
    assert part1(input_test) == 12
    P.xlim, P.ylim = 101, 103
    print(part1(read_input(day)))
    part2(read_input(day))  # step 7569
