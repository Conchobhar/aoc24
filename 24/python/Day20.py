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
import bisect

import aoc
from aoc import P, deltas


day = Path(__file__).stem


def read_input(name:str):
    data = (aoc.data_path / f'{name}.txt').open().read().strip().split('\n')
    return [list(row) for row in data]

class Racepos:

    def __init__(self, p:P, step:int):
        self.p = p
        self.step = step

    def __lt__(self, other):
        return self.step < other.step
    
    def __eq__(self, other):
        return self.p == other.p
    
    def __hash__(self):
        return hash(self.p)
    
    def __repr__(self):
        return f'RP({self.p}, {self.step})'
    
    def __str__(self):
        return f'RP({self.p}, {self.step})'
    

class Racetrack(aoc.NPGrid):

    """2D grid with only a single route between start and end."""

    def __init__(self, data):
        super().__init__(len(data[0]), len(data), dtype=str)
        for y, row in enumerate(data):
            for x, value in enumerate(row):
                self[P(x, y)] = value
                if value == 'S':
                    self.start = P(x, y)
                if value == 'E':
                    self.end = P(x, y)

    def get_path(self) -> Dict[P, int]:
        """There is only one path in racetrack.
        Store as map fro points to steps required to get there."""
        step = 0
        rp = Racepos(self.start, step)
        racepositions = {rp.p: step}
        lp = rp.p
        while rp.p != self.end:
            for d in deltas:
                np = rp.p + d
                if self.in_bounds(np) and self[np] != '#' and np != lp:
                    nrp = Racepos(np, rp.step+1)
                    break
            racepositions[nrp.p] = nrp.step
            lp = rp.p
            rp = nrp
        return racepositions
    
    def print_points(self, points):
        g = self.g.copy()
        for idx, p in enumerate(points):
            g[p.y][p.x] = str(idx)
        for y in range(self.ylim):
            print(''.join(str(g[x, y]) for x in range(self.xlim)))



def part1(rt:Racetrack, saved:int) -> int:
    path = rt.get_path()
    cheats = []  # Tuples of (wall_pos, rp_pos, steps_saved)
    for p, p_step in path.items():
        # if any adj wall is adj to a rp with higher step, add it to cheat
        for d1 in deltas:
            np1 = p + d1
            if rt.in_bounds(np1) and rt[np1] == '#':
                for d2 in deltas:
                    if d2 != -d1:
                        np2 = np1 + d2
                        if np2_step := path.get(np2):
                            if np2_step > (path[p] + 2):
                                cheats.append((np1, np2, np2_step - p_step - 2))
    return len([c for c in cheats if c[-1] >= saved])
                    

def part2(rt:Racetrack, saved:int) -> int:
    """A cheat is from every rp to every rp after it if the distance is <= steps saved by assuming
    no collision for 20 steps.
    """
    path = rt.get_path()
    pathl = list(path)
    cheats = []
    for idx, rp in enumerate(pathl):
        aoc.prog_print(f'{idx}')
        for rp2 in pathl[idx+1:]:
            dist = rp.l1(rp2)
            if dist <= 20:  # cheat possible
                steps_saved = (path.get(rp2) - path.get(rp) - dist)
                if dist < steps_saved:
                    cheats.append((rp, rp2, dist, steps_saved))
    return len([c for c in cheats if c[-1] >= saved])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()
    if args.debug:
        aoc.Debug.set = True
        
    input_test = read_input(f'{day}_test')
    rt = Racetrack(input_test)
    rtp = rt.get_path()
    assert rtp[rt.end] == 84
    assert part1(rt, 64) == 1
    print(part1(Racetrack(read_input(day)), 100))
    assert part2(rt, 10) == 2139
    print(part2(Racetrack(read_input(day)), 100))  # 985737
