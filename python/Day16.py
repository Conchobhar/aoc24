import argparse
from functools import reduce
import os
from pathlib import Path
from typing import *
import bisect

import aoc
from aoc import P, Grid


day = Path(__file__).stem


def read_input(name:str):
    data = []
    for row in (aoc.data_path / f'{name}.txt').open().read().strip().split('\n'):
        data.append(list(row))
    return data

                
dir2delta = {
    'north': P(0, -1),
    'east': P(1, 0),
    'south': P(0, 1),
    'west': P(-1, 0)
}
dirs = list(dir2delta.keys())

class Maze(Grid):
    
        def __init__(self, data):
            super().__init__(data)
            self.start = self.get_point('S')
            self.rp = self.start
            self.end = self.get_point('E')
            self.dir = 'east'
            self.score = 0
    
        def get_point(self, char):
            for p in self.valid_points():
                if self[p] == char:
                    return p
        
        def print(self, p, d, c, hx):
            # Clear the screen and move the cursor to the top-left corner
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # Print the grid
            for y in range(self.limy):
                for x in range(self.limx):
                    if P(x, y) == p:
                        print('X', end='')
                    elif P(x, y) in hx:
                        print('O', end='')
                    else:
                        print(self[P(x, y)], end='')
                print()
            print(f"Direction: {d}")
            print(f"Cost: {c}")

        def worth_it(self, p:P, c:int):
            """Has another route visited here yet? If so only consider it
            if the cost to get there is <= the best cost for a different route.

            This updates the point2cost (p2c) record.
            """
            co = self.p2c.get(p)
            if not co or c-1000 <= co:
                self.p2c[p] = c
                return True
            return False

        def get_possible_next(self, p:P, d:str, c:int, hx:List[P]) -> List[Tuple]:
            """Consider possible moves:
                - forward
                - turn clockwise and forward
                - turn anti clockwise and forward
            Worth considering if moving there would not end up costing more than any other route
            that has previously been there.
            """
            possible = []
            p_ahead = (p + dir2delta[d])
            if self[p_ahead] in '.E' and p_ahead not in hx:
                if self.worth_it(p_ahead, c+1):
                    possible.append((p_ahead, d, c+1, hx+[p_ahead]))
            cwidx = (dirs.index(d) + 1) % 4
            cwd = dirs[cwidx]
            cwp = p + dir2delta[cwd]
            if self[cwp] in '.E':
                if self.worth_it(cwp, c+1001):
                    possible.append((cwp, dirs[cwidx], c+1001, hx+[cwp]))
            acwidx = (dirs.index(d) - 1) % 4
            acwd = dirs[acwidx]
            acwp = p + dir2delta[acwd]
            if self[acwp] in '.E':
                if self.worth_it(acwp, c+1001):
                    possible.append((acwp, dirs[acwidx], c+1001, hx+[acwp]))
            return possible


        def get_routes_with_best_score(self) -> List[Tuple]:
            """Consider how to get from p to ep by considering all available new moves
            
            We ignore a new move if we have a record of another route getting there with a lower
            cost.

            A route is a tuple of
                (Position, direction, accrued cost, position history)
            """
            # keep track of possible routes and finished rotes
            routes_queued = [(self.start, self.dir, 0, [self.start])]
            routes_finished = []
            self.p2c = {} # keep record of best cost for a given point. if possible route would hit a point with  a higher cost, skip it
            self.cost_min = float('inf')
            n=0
            while routes_queued:
                best_route = routes_queued.pop()
                aoc.prog_print(f"Step {n} {len(routes_queued)=}")
                possible_next = self.get_possible_next(*best_route)
                # insert possible_next into routes_queued in order by min cost
                for route in possible_next:
                    if route[0] == self.end and route[2] <= self.cost_min:
                        # if this completes the route, record min cost and filter routes_queued
                        # to remove any route that would cost more (but keep equal routes)
                        self.cost_min = route[2]  # only needs to be set once really
                        routes_queued = [r for r in routes_queued if r[2] <= self.cost_min]
                        bisect.insort(routes_finished, route, key=lambda x:-x[2])
                    else:
                        bisect.insort(routes_queued, route, key=lambda x:-x[2])
                n+=1
            print()
            # since best possible score will be found first, all finished routes will only be those
            # that share the best score.
            return routes_finished
        


def part1(m:Maze) -> int:
    return m.get_routes_with_best_score().pop()[2]


def part2(m:Maze) -> int:
    end_routes = m.get_routes_with_best_score()
    # collect all unique points from histories
    points = reduce(set.union, [set(r[3]) for r in end_routes])
    return len(points)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()
    if args.debug:
        aoc.Debug.set = True
        
    input_test = read_input(f'{day}_test')
    m = Maze(input_test)
    assert part1(m) == 7036
    print(part1(Maze(read_input(f'{day}'))))  # 147628
    assert part2(m) == 45
    print(part2(Maze(read_input(f'{day}'))))
