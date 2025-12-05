import argparse
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
import heapq

import aoc
from aoc import P, deltas


day = Path(__file__).stem


def read_input(name:str):
    data = (aoc.data_path / f'{name}.txt').open().read().strip().split('\n')
    return [list(map(int, l.split(','))) for l in data]

class NPGrid:

    def __init__(self, blocks, xlim, ylim):
        self.xlim = xlim
        self.ylim = ylim
        self.grid = np.zeros((xlim, ylim), dtype=int)
        self.blocks = blocks
        self.nblock = 0
    
    def __getitem__(self, p:P):
        return self.grid[p.x, p.y]
    
    def __setitem__(self, p:P, v:int):
        self.grid[p.x, p.y] = v

    @property
    def pprint(self):
        for y in range(self.ylim):
            print(''.join(str(self.grid[x, y]) for x in range(self.xlim)))

    def in_bounds(self, p:P):
        return 0 <= p.x < self.xlim and 0 <= p.y < self.ylim

    def get_shortest_path(self, start=None, end=None):
        """Djikstras - follow all possible paths, priority queue exploring the path with minimised priority score
        which is steps taken + manhattan distance to end point. If a path takes a step but is also 1 closer to
        the end, it maintains its priority. This means we can  find the shortest path but not spend time exploring every
        path.
        """
        start = P(0, 0) if start is None else start
        end = P(self.xlim-1, self.ylim-1) if end is None else end
        # q is (priority=steps-npdist, dist, pos, steps,)
        dist = start.dist(end)
        q = [(0-dist,0, start, dist,)]
        visited = set()
        while q:
            priority, steps, pos, dist = heapq.heappop(q)
            if pos == end:
                return steps
            if pos in visited:
                continue
            visited.add(pos)
            for d in deltas:
                np = pos + d
                if self.in_bounds(np) and self[np] == 0:
                    npdist = np.dist(end)
                    heapq.heappush(q, (steps-npdist,steps+1, np, npdist))
        return -1

    def set_blocks(self, n:int):
        if n > self.nblock:
            # adding
            for i, (x, y) in enumerate(self.blocks[self.nblock:n]):
                self.grid[x, y] = 1
                if i == n-1:
                    break
        else:
            # removing
            for i, (x, y) in enumerate(self.blocks[n:self.nblock]):
                self.grid[x, y] = 0
                if i == n-1:
                    break
        self.nblock = n


def part1(g:NPGrid, nblocks:int) -> int:
    g.set_blocks(nblocks)
    return g.get_shortest_path()


def part2(g:NPGrid) -> Tuple[int, int]:
    nblocks = len(g.blocks)
    lb, ub = 0, nblocks
    while True:
        guess = (ub + lb) // 2
        g.set_blocks(guess)
        sp  = g.get_shortest_path()
        aoc.debug(f'{ub=}, {lb=}, {guess=}, {sp}')
        if sp == -1:
            ub = guess
        else:
            lb = guess
            if guess == ub - 1:
                break
    return g.blocks[guess]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()
    if args.debug:
        aoc.Debug.set = True

    input_test = read_input(f'{day}_test')
    assert part1(NPGrid(input_test, 7, 7), nblocks=12) == 22
    print(part1(NPGrid(read_input(f'{day}'), 71, 71), nblocks=1024))  # 226
    assert part2(NPGrid(input_test, 7, 7)) == [6,1]
    print(part2(NPGrid(read_input(f'{day}'), 71, 71)))  # [60, 46]
