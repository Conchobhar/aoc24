import argparse
from pathlib import Path
from typing import *

import aoc
from aoc import P, deltas


day = Path(__file__).stem


def read_input(name:str) -> List[List[str]]:
    data = (aoc.data_path / f'{name}.txt').open().read().strip()
    return [list(row) for row in data.split('\n')]


class Region:

    def __init__(self, sym:str, id_point:P, points_edge:Set[P]=set(), points_inner:Set[P]=set()) -> None:
        self.sym = sym
        self.id_point = id_point
        self.points_edge = points_edge
        self.points_inner = points_inner
        self.edges_accounted_for = None
        self.edge_groups = None

    def __iter__(self):
        return iter(self.points_edge | self.points_inner)

    @property
    def perimeter(self) -> int:
        c = 0
        for p in self:
            for d in deltas:
                np = p + d
                if np not in self:
                    c += 1
        return c
    
    @property
    def area(self) -> int:
        return len([x for x in self])
    
    def follow_edge(self, edge:Tuple[P, P], last:P=P(-1,-1)) -> Set[P]:
        """Given an edge, find all adjacent edges not already discovered"""
        ep, ed  = edge
        s = set([edge])
        edges = set()
        for dep in deltas:
            np = ep+dep
            if np != last and np in self.points_edge:
                # now need to find if this new point shares an edge with the same delta as the previous point
                # i.e. is alligned
                for dnp in deltas:
                    if np+dnp not in self.points_edge and dnp == ed:
                        edge = (np, dnp)
                        self.edges_accounted_for.add(edge)
                        edges = self.follow_edge(edge, ep)
                        break # will only be one if any
        return s | edges

    
    def discover_edges(self):
        """an edge is a pair of (point, delta)
        Explore from every point by following alligned edges to collect all sets of edge points.
        """
        self.edges_accounted_for = set()
        self.edge_groups = []
        for p in self.points_edge:  # look over all points that will have >= 1 edges
            for d in deltas:
                if p+d not in self:  # then this (p,d) is an edge for our region
                    edge = (p, d)
                    if edge not in self.edges_accounted_for:  # havent seen in a prev self.follow_edge()
                        self.edges_accounted_for.add(edge)
                        se = self.follow_edge(edge)
                        self.edge_groups.append(se)
    
    def __repr__(self) -> str:
        return f'{self.sym} {len(self.points_edge)=} {len(self.points_inner)=}'


class Garden:

    def __init__(self, data:List[List[str]]) -> None:
        """Defne a garden with a 2D array of data.

        Initaliszing a garden redefines the limits of the Point class as a convenience
        
        """
        P.limx = len(data[0])
        P.limy = len(data)
        self.m = data
        self.regions:Dict[Tuple, Region] = {}  # (sym, upperleftmost point) to {points}
        self.allocated:Set[P] = set()

    def __getitem__(self, p:P) -> str:
        return self.m[p.y][p.x]

    def fill_region(self, p:P, d:P, sym) -> Tuple[Set[P], Set[P]]:
        pe, pi = set(), set()
        is_edge = False
        for d in deltas:
            if d != -d:  # dont look back
                np = p + d
                if  np.in_bounds and self[np] == sym:
                    if np not in self.allocated:
                        self.allocated.add(np)
                        fpe, fpi = self.fill_region(np, d, sym)
                        pe |= fpe
                        pi |= fpi
                else:
                    is_edge = True
        pe.add(p) if is_edge else pi.add(p)
        return pe, pi
        

    def discover_regions(self):
        for p in P.valid_points():
            if p not in self.allocated:  # new region
                sym = self[p]
                points_edge, points_inner = self.fill_region(p, P(0, 0), sym)
                region = Region(sym, p, points_edge, points_inner)
                self.regions[(sym, p)] = region


def part1(input) -> int:
    c = 0
    g = Garden(input)
    g.discover_regions()
    for rp in g.regions.values():
        c += rp.perimeter * rp.area
    return c


def part2(input) -> int:
    c = 0
    g = Garden(input)
    g.discover_regions()
    for rp in g.regions.values():
        rp.discover_edges()
        c += rp.area * len(rp.edge_groups)
    return c


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()
    if args.debug:
        aoc.Debug.set = True

    input_test1 = read_input(f'{day}_test1')
    g = Garden(input_test1)
    g.discover_regions()
    assert len(g.regions) == 5

    assert part1(input_test1) == 140
    print(part1(read_input(day)))  # 1450422
    assert part2(input_test1) == 80
    print(part2(read_input(day)))  # 906606
