import argparse
from copy import deepcopy
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
from aoc import P


day = Path(__file__).stem


def read_input(name:str) -> List[str]:
    data = (aoc.data_path / f'{name}.txt').open().read().strip()
    grid, instructions = data.split('\n\n')
    return [[y for y in x] for x in grid.split('\n')], instructions.replace('\n', '')


def read_input_wide(name:str) -> List[str]:
    data = (aoc.data_path / f'{name}.txt').open().read().strip()
    grid, instructions = data.split('\n\n')
    ngrid = []
    for row in [[y for y in x] for x in grid.split('\n')]:
        nrow = []
        for v in row:
            match v:
                case '#':
                    nrow.extend(['#']*2)
                case '.':
                    nrow.extend(['.']*2)
                case 'O':
                    nrow.extend(['[', ']'])
                case '@':
                    nrow.extend(['@', '.'])
        ngrid.append(nrow)
    return ngrid, instructions.replace('\n', '')


i2delta = {
    '>': P(1, 0),
    '<': P(-1, 0),
    '^': P(0, -1),
    'v': P(0, 1),
}

class Grid:

    m = {
        '#': 'wall',
        'O': 'box',
        '@': 'robot',
        '.': 'empty',
    }

    def __init__(self, g:List[List[str]], ins:str) -> None:
        self.g = g
        self.ins = ins
        self.finished = False
        self.idxstep = 0
        self.last_dp = None
        self.last_ins = None
        P.limy, P.limx = len(g), len(g[0])
        for y, row in enumerate(self.g):
            for x, v in enumerate(row):
                if v == '@':
                    self.rp = P(x, y)
                    break

    def __getitem__(self, p:P) -> str:
        return self.g[p.y][p.x]
    
    def __setitem__(self, p:P, v:str) -> None:
        self.g[p.y][p.x] = v
    
    def print(self):
        print(f"Step {self.idxstep} of {len(self.ins)} - last_dp: {self.last_dp} {self.last_ins}")
        for r in g.g:
            print(r)

    def step(self):
        if self.finished:
            print("Already finished")
            return
        ins = self.ins[self.idxstep]
        dp = i2delta[ins]
        self.last_dp = dp
        self.last_ins = ins
        self.idxstep += 1
        if self.move(self.rp, dp):
            self.rp = self.rp + dp
        if self.idxstep >= len(self.ins):
            self.finished = True

    def move(self, sp:P, dp:P) -> bool:
        """Updates grid, returns outcome move possibility."""
        np = sp + dp
        if np.in_bounds:
            match self[np]:
                case '#':
                    can_move = False
                case '.':
                    can_move = True
                case 'O':
                    can_move = self.move(np, dp)
        if can_move:
            sym = self[sp] 
            self[sp] = '.'
            self[np] = sym
        return can_move
    
    @property
    def box_gps_coords(self):
        for p in P.valid_points():
            if self[p] == 'O':
                yield (p.x, p.y*100)


class GridWide:

    m = {
        '#': 'wall',
        'O': 'box',
        '@': 'robot',
        '.': 'empty',
    }

    def __init__(self, g:List[List[str]], ins:str) -> None:
        self.g = g
        self.ins = ins
        self.finished = False
        self.idxstep = 0
        self.last_dp = None
        self.last_ins = None
        P.limy, P.limx = len(g), len(g[0])
        for y, row in enumerate(self.g):
            for x, v in enumerate(row):
                if v == '@':
                    self.rp = P(x, y)
                    break

    def __getitem__(self, p:P) -> str:
        return self.g[p.y][p.x]
    
    def __setitem__(self, p:P, v:str) -> None:
        self.g[p.y][p.x] = v
    
    def print(self):
        print(f"Step {self.idxstep} of {len(self.ins)} - last_dp: {self.last_dp} {self.last_ins}")
        print([' '] + [str(i)[-1] for i in range(len(self.g[0]))])
        for ic, r in enumerate(self.g):
            print([str(ic)] + r)

    def apply_moves(self, moves:List[Tuple[P, P]], dp:P):
        ng = deepcopy(self.g)
        for sp in moves:
            ng[sp.y][sp.x] = '.'
        for sp in moves:
            np = sp + dp
            ng[np.y][np.x] = self.g[sp.y][sp.x]
        self.g = ng

    def step(self):
        if self.finished:
            print("Already finished")
            return
        ins = self.ins[self.idxstep]
        dp = i2delta[ins]
        self.last_dp = dp
        self.last_ins = ins
        self.idxstep += 1
        can_move, moves = self.consider_move(self.rp, dp)
        if can_move:
            self.apply_moves(moves, dp)
            self.rp = self.rp + dp
        if self.idxstep >= len(self.ins):
            self.finished = True

    def consider_move(self, sp:P, dp:P) -> Tuple[bool, List[Tuple[P, P]]]:
        """Consider required moves, returns:
            (are all moves possible, moves)
        """
        np = sp + dp
        moving_in_y = dp in [P(0, 1), P(0, -1)]
        moves = [sp]  # list of points that will be moved by d
        can_move = False
        if np.in_bounds:
            match self[np]:
                case '#':
                    can_move = False
                case '.':
                    can_move = True
                case '[':
                    if moving_in_y:
                        can_move_l, moves_l = self.consider_move(np, dp)
                        can_move_r, moves_r = self.consider_move(np+P(1,0), dp)
                        can_move = can_move_l and can_move_r
                        moves = moves + moves_l + moves_r
                    else:
                        can_move, moves_b = self.consider_move(np, dp)
                        moves = moves + moves_b
                case ']':
                    if moving_in_y:
                        can_move_l, moves_r = self.consider_move(np, dp)
                        can_move_r, moves_l = self.consider_move(np+P(-1,0), dp)
                        can_move = can_move_l and can_move_r
                        moves = moves + moves_l + moves_r
                    else:
                        can_move, moves_b = self.consider_move(np, dp)
                        moves = moves + moves_b
        return can_move, moves
    
    @property
    def box_gps_coords(self):
        for p in P.valid_points():
            if self[p] == '[':
                yield (p.x, p.y*100)

def part1(g:Grid) -> int:
    while not g.finished:
        g.step()
    return sum([x+y for x, y in g.box_gps_coords])


def part2(g:GridWide) -> int:
    while not g.finished:
        aoc.prog_print(f"Step {g.idxstep} of {len(g.ins)}")
        g.step()
    print()
    return sum([x+y for x, y in g.box_gps_coords])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()
    if args.debug:
        aoc.Debug.set = True
        
    grid_test, instructions_test = read_input(f'{day}_test_small')
    g = Grid(grid_test, instructions_test)
    assert g.rp == P(2, 2)
    g.step()
    assert g.rp == P(2, 2)
    g.step()
    assert g.rp == P(2, 1) and g.last_ins == '^'
    gtest = Grid(grid_test, instructions_test)
    assert part1(gtest) == 2028
    gtest_large = Grid(*read_input(f'{day}_test_large'))
    assert part1(gtest_large) == 10092
    print(part1(Grid(*read_input(day))))

    assert part2(GridWide(*read_input_wide(f'{day}_test_large'))) == 9021
    print(part2(GridWide(*read_input_wide(f'{day}'))))
