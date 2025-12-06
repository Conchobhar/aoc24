import time
import heapq
import argparse
from pathlib import Path
from functools import wraps
from typing import List, Set, Any
import numpy as np

data_path = Path(__file__).absolute().parents[0] / 'data'

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output')
args = parser.parse_args()


class Debug:
    """Debug"""
    set = False


def aoc_print(s: str, status: bool = None):
    GREEN_TEXT = "\033[92m"
    RED_TEXT = "\033[91m"
    GREY_TEXT = "\033[90m"
    RESET = "\033[0m"
    if status is True:
        color = GREEN_TEXT
    elif status is False:
        color = RED_TEXT
    else:
        color = GREY_TEXT
    print(f"{color}{s}{RESET}")


def part(func):
    @wraps(func)
    def wrapper(*args):
        if len(args) == 1:
            data = args[0]
            expected = ...
        else:
            data, expected = args
        start = time.time()
        result = func(data)
        end = time.time()
        aoc_print(f"{func.__name__} took {end - start:.6f} seconds")
        exp = '...' if expected is ... else repr(expected)
        status = None if expected is ... else result == expected
        aoc_print(f"{func.__name__} result: {result}, expected: {exp}", status)
        return result
    return wrapper


if args.debug:
    Debug.set = True

def prog_print(s:str):
    print(f"{s}", end='\r', flush=True)


def debug(*args):
    if Debug.set:
        print(*args)


class P:
    """Define a 2D point
    
    Limits for x and y are class attribs defining the range of the grid the points are used in.
    These are set by the revelent problem.
    """

    limx = None
    limy = None

    @classmethod
    def valid_points(cls):
        """Generate all valid points in the grid."""
        if cls.limx is None or cls.limy is None:
            raise ValueError("Need to set class attribs limx and limy.")
        for x in range(cls.limx):
            for y in range(cls.limy):
                yield P(x, y)

    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y

    def __add__(self, other):
        return P(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return P(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return P(-self.x, -self.y)

    def __repr__(self): 
        return f'P({self.x}, {self.y})'
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)
    
    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)
    
    def __getitem__(self, idx:int) -> int:
        return (self.x, self.y)[idx]
    
    def dist(self, other):
        return (self.x-other.x)**2 + (self.y-other.y)**2
    
    def l1(self, other):
        return abs(self.x-other.x) + abs(self.y-other.y)
    
    @property
    def adjacent_4(self) -> Set['P']:
        """Get all 4 adjacent (but not necessarily in bounds) points to this one."""
        return set(self + d for d in deltas_4)    
    
    @property
    def adjacent_8(self) -> Set['P']:
        """Get all 4 adjacent (but not necessarily in bounds) points to this one."""
        return set(self + d for d in deltas_8)

    @property
    def in_bounds(self) -> bool:
        if self.limx is None or self.limy is None:
            raise ValueError("Need to set class attribs limx and limy.")
        return (0 <= self.x < self.limx) and (0 <= self.y < self.limy)


deltas_4 = [P(0, 1), P(1, 0), P(0, -1), P(-1, 0)]
deltas_8 = [P(0, 1), P(1, 0), P(0, -1), P(-1, 0), P(1, 1), P(1, -1), P(-1, 1), P(-1, -1)]


class Grid:
    """2D grid as a List of Lists"""

    def __init__(self, g:List[List[Any]]) -> None:
        self.g = g
        self.limy, self.limx = len(g), len(g[0])
        P.limx = self.limx
        P.limy = self.limy

    def __getitem__(self, p:P) -> Any:
        return self.g[p.y][p.x]
    
    def get_oob(self, p:P) -> Any:
        if p.in_bounds:
            return self[p]
        return None
    
    def __setitem__(self, p:P, v:Any) -> None:
        self.g[p.y][p.x] = v

    def __str__(self) -> str:
        return f'Grid(limx={self.limx}, limy={self.limy})'
    
    def valid_points(self):
        """Generate all valid points in the grid."""
        if self.limx is None or self.limy is None:
            raise ValueError("Need to set class attribs limx and limy.")
        for x in range(self.limx):
            for y in range(self.limy):
                yield P(x, y)
    
    def print(self):
        for row in self.g:
            print(''.join(row))


class NPGrid:
    """2D grid as a numpy array"""
    def __init__(self, xlim, ylim, dtype=int):
        self.xlim = xlim
        self.ylim = ylim
        self.g = np.zeros((xlim, ylim), dtype=dtype)
    
    def __getitem__(self, p:P) -> Any:
        return self.g[p.y, p.x]
    
    def __setitem__(self, p:P, v:Any):
        self.g[p.y, p.x] = v

    @property
    def pprint(self, center:P=None):
        """If center is provided, print centered on it"""
        for y in range(self.ylim):
            print(''.join(str(self[P(x, y)]) for x in range(self.xlim)))


    def in_bounds(self, p:P) -> bool:
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
                npos = pos + d
                if self.in_bounds(npos) and self[npos] == 0:
                    npdist = npos.dist(end)
                    heapq.heappush(q, (steps-npdist,steps+1, npos, npdist))
        return -1
