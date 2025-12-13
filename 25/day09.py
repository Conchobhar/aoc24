import bisect
import math
from pathlib import Path
import time
from typing import Any, Generator, Iterator, List, Dict, Set, Tuple
from collections import defaultdict
from itertools import product, permutations, combinations
# product gets every pairing
#   permutations excludes (self, self)
#   combinations excludes ordering
from tqdm import tqdm
import matplotlib.pyplot as plt

import aoc
from aoc import P


day = Path(__file__).stem


def get(day:str, test=False):
    name = f'{day}' + ('_test' if test else '')
    return (aoc.data_path / f'{name}.txt').open().read().strip().split('\n')


@aoc.part
def part1(data):
    ps = []
    seen = set()
    for r in data:
        ps.append(aoc.P(*map(int, r.split(','))))
    a2pair = {}
    for p1 in ps:
        for p2 in ps:
            if p1 == p2 or p2 in seen:
                continue
            a = abs((p1.x - p2.x + 1) * (p1.y - p2.y + 1))
            a2pair[a] = tuple(sorted((p1, p2)))
        seen.add(p1)
    return max(a2pair)


def get_perimeter_points(p1: P, p2: P) -> Iterator[P]:
    xmin, xmax = sorted([p1.x, p2.x])
    ymin, ymax = sorted([p1.y, p2.y])
    # Top and bottom edges
    for x in range(xmin, xmax + 1):
        yield P(x, ymin)
        yield P(x, ymax)
    # Left and right edges (excluding corners to avoid duplicates)
    for y in range(ymin + 1, ymax):
        yield P(xmin, y)
        yield P(xmax, y)


@aoc.part
def part2(data):
    ps = []  # sequential corner points
    setin = set()  # points in bounds
    if aoc.Debug.set:
        plt.ion()
    maxx, maxy = 0, 0
    for r in data:  # collect initial points
        p = aoc.P(*map(int, r.split(',')))
        ps.append(p)
        p.label = 'r'
        setin.add(p)
        maxx, maxy = max(maxx, p.x), max(maxy, p.y)
    aoc.P.limx = maxx+2
    aoc.P.limy = maxy+2
    for p1, p2 in tqdm(zip(ps, ps[1:] + [ps[0]])):  # for all sequential pairs ...
        axis = 'x' if p1.x != p2.x else 'y'
        vmin, vmax = sorted([getattr(p1, axis), getattr(p2, axis)])
        if aoc.Debug.set:
            p1.plot(c='red')
            p2.plot(c='red')
        setin.add(p1)
        for i in range(vmin+1, vmax):  # ... get points between each pair
            coords = (i, p1.y) if axis == 'x' else (p1.x, i)
            p = aoc.P(*coords)
            p.label = 'g'
            setin.add(p)
            if aoc.Debug.set:
                p.plot(c='green')
    print("setin", len(setin))

    # define a point adjacted our polygon that we know must be outside the shape
    p = min(ps, key=lambda p: p.x)
    p = P(p.x-1, p.y) # assuming this is out
    assert p.in_bounds
    setout = set([p]) # shell around setin
    explore_from = set([p])
    while explore_from:
        p = explore_from.pop()
        new = {padj for padj in p.adjacent_4 if padj.in_bounds and (
            padj not in setout and 
            padj not in setin and
            any([
            padjadj in setin for padjadj in padj.adjacent_8
        ]))}
        explore_from |= new
        setout |= new
        
        # track progress
        bar_len = 40
        total = len(setin) + len(ps)
        progress = len(setout) / max(total, 1)
        filled = int(bar_len * min(progress, 1.0))
        bar = '[' + '#' * filled + '-' * (bar_len - filled) + ']'
        setout_count = f"{len(setout):>{len(str(total))}}"
        total_count = f"{total:>{len(str(total))}}"
        print(f"Setout: {setout_count}/{total_count} {bar}", end='\r', flush=True)

        if aoc.Debug.set:
            p.plot(c='blue')
    
    print("Checking rectangles...")
    area = 0
    total = math.comb(len(ps), 2)
    for p1,p2 in tqdm(combinations(ps, 2), total=total):
        for pn in (get_perimeter_points(p1, p2)):
            if pn in setout:
                break
        else:
            a = abs((p1.x - p2.x + 1) * (p1.y - p2.y + 1))
            area = max(area, a)

    if aoc.Debug.set:
        plt.ioff()
        plt.show()
    return area


@aoc.part
def part2(data):
    """Each pair of sequential points defines an orthogonal range
    p1,p2
    p2,p3

    if a given possible rectangle has any of its sides cross through any of these ranges, its invalid
    """
    ps = []  # sequential corner points
    setin = set()  # points in bounds
    if aoc.Debug.set:
        plt.ion()
    maxx, maxy = 0, 0
    for r in data:  # collect initial points
        p = aoc.P(*map(int, r.split(',')))
        ps.append(p)
        p.label = 'r'
        setin.add(p)
        maxx, maxy = max(maxx, p.x), max(maxy, p.y)
    aoc.P.limx = maxx+2
    aoc.P.limy = maxy+2

    def crosses(l1, l2):
        c1, r1min, r1max = l1
        c2, r2min, r2max = l2
        if r2min < c1 < r2max:
            if r1min < c2 < r1max:
                return True
        return False
    
    def pair_doesnt_intersect_any(p1, p2):
        # p1.plot(), p2.plot()
        h = min(p1.x, p2.x)+1, max(p1.x, p2.x)-1
        v = min(p1.y, p2.y)+1, max(p1.y, p2.y)-1
        d1y = 1 if p1.y < p2.y else -1
        d2y = 1 if d1y == -1 else 1
        d1x = 1 if p1.x < p2.x else -1
        d2x = 1 if d1x == -1 else 1
        square = {
            'h': [(p1.y+d1y, *h), (p2.y+d2y, *h)],
            'v': [(p1.x+d1x, *v), (p2.x+d2x, *v)]
        }
        allignment = 'v' if ps[0].x == ps[1].x else 'h'
        flip = {'v': 'h', 'h': 'v'}
        for bp1, bp2 in zip(ps, ps[1:] + [ps[0]]):
            # bp1.plot(c='b'), bp2.plot(c='b')
            if allignment == 'h':
                bline = (bp1.y, min(bp1.x, bp2.x), max(bp1.x,bp2.x))
            else:
                bline = (bp1.x, min(bp1.y, bp2.y), max(bp1.y,bp2.y))
            lines = square[flip[allignment]]
            for line in lines:
                if crosses(bline, line):
                    return False
            allignment = flip[allignment]
        return True

    pair2area = {}
    for p1,p2 in tqdm(combinations(ps, 2), total=math.comb(len(ps), 2)):
        a = abs((p1.x - p2.x + 1) * (p1.y - p2.y + 1))
        if pair_doesnt_intersect_any(p1,p2):
            pair2area[(p1,p2)] = a

    maxpair2area = max(pair2area.items(), key=lambda x:x[1])
    print(maxpair2area)
    return maxpair2area[1]

if __name__ == '__main__': 
    data_test, data = get(day, test=True), get(day)
    aoc.Debug.set = True
    # part1(data_test, 50)
    # part1(data, 4763932976)
    
    part2(data_test, 24)
    part2(data)  # 1501258700, to low
    
