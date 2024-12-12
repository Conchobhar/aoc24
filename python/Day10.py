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

data_path = Path(__file__).absolute().parents[1] / 'data'
day = Path(__file__).stem
enum = enumerate


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
    
    @property
    def in_bounds(self) -> bool:
        return (0 <= self.x < self.limx) and (0 <= self.y < self.limy)
    

# up down left and right
deltas = [P(0, 1), P(1, 0), P(0, -1), P(-1, 0)]

class Topo:

    def __init__(self, m=List[List[int]]) -> None:
        self.m = m
        P.limx = len(m)
        P.limy = len(m[0])
        self._trailheads: Set[P] = None # set of (y, x) coord pairs
        self.th2peaks: Dict[P, Set[P]] = defaultdict(set)
        self.routes = {}
        # route is a tuple of poiints (P1, P2, ..., Pn)

    @property
    def trailheads(self):
        if not self._trailheads:
            self._trailheads = set()
            for ir, row in enum(self.m):
                for ic, c in enum(row):
                    if c == 0:
                        self._trailheads |= {P(ic, ir)}
        return self._trailheads
    
    def _explore_from_point(self, th:P, p:P, delta:P, depth=0) -> List[Tuple[P]]:
        """
        th - initial trailhead
        p - current point
        delta - direction of travel
        depth - recursion depth

        returns a list of distinct routes from th to a peak
        """
        p = p + delta
        vi = self.m[p.y][p.x]
        debug(f"{' '*depth} {p=} {vi=}")
        if depth > 20:
            raise Exception('Balrogs')
        if vi == 9:
            debug(f"found at {p=}")
            self.th2peaks[th] |= {p}
            return [(p,)]
        routes = []
        for d in deltas:
            if not (p+d).in_bounds or d == -delta:  # dont go back
                continue
            vd = self.m[p.y+d.y][p.x+d.x]
            if vd-vi == 1:
                debug(" "*depth + f"looking at {p+d=}")
                r = self._explore_from_point(th, p, d, depth+1)
                for route in r:
                    routes.append((p, *route))
        return routes
    
    def get_score(self, th:P) -> int:
        ps = self._explore_from_point(th, th, P(0, 0))
        return len(set(ps))
    
    def get_scores(self) -> int:
        return [self.get_score(th) for th in self.trailheads]
    
    def explore_routes(self):
        for th in self.trailheads:
            self.routes[th] = self._explore_from_point(th, th, P(0, 0))

    def get_ratings(self) -> int:
        self.th2rating = {}
        return sum([len(r) for th, r in self.th2rating.items()])


def debug(s:str):
    if DEBUG:
        print(s)


def read_input(name:str) -> List[str]:
    return [[int(x) if x != '.' else -2 for x in row] for row in (data_path / f'{name}.txt').open().read().strip().split('\n') ]


def part1(input) -> int:
    t = Topo(input)
    t.get_scores()
    return sum([len(peaks) for th, peaks in t.th2peaks.items()])


def part2(input) -> int:
    t = Topo(input)
    t.explore_routes()
    return sum([len(rs) for th, rs in t.routes.items()])


if __name__ == '__main__':
    DEBUG = False
    input_test = read_input(f'{day}_test')
    input_test_a = read_input(f'{day}_test_a')
    t = Topo(input_test_a)
    t.get_scores()

    assert part1(input_test) == 36
    print(part1(read_input(day)))
    assert part2(input_test) == 81
    print(part2(read_input(day)))
