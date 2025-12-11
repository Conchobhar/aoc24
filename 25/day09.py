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
    ps = []
    setin = set()
    if aoc.Debug.set:
        plt.ion()
        fig, ax = plt.subplots()
    maxx, maxy = 0, 0
    for r in data:
        p = aoc.P(*map(int, r.split(',')))
        ps.append(p)
        p.label = 'r'
        setin.add(p)
        maxx, maxy = max(maxx, p.x), max(maxy, p.y)
    aoc.P.limx = maxx+1
    aoc.P.limy = maxy+1
    if aoc.Debug.set:
        ax.set_xlim(-1, maxx+1)
        ax.set_ylim(-1, maxy+1)
    for p1, p2 in tqdm(zip(ps, ps[1:] + [ps[0]])):
        axis = 'x' if p1.x != p2.x else 'y'
        vmin, vmax = sorted([getattr(p1, axis), getattr(p2, axis)])
        if aoc.Debug.set:
            ax.scatter(p1.x, p1.y, c='red', marker='s', s=800, alpha=0.5)
            ax.scatter(p2.x, p2.y, c='red', marker='s', s=800, alpha=0.5)
            plt.draw()
        setin.add(p1)
        for i in range(vmin+1, vmax):
            coords = (i, p1.y) if axis == 'x' else (p1.x, i)
            p = aoc.P(*coords)
            p.label = 'g'
            setin.add(p)
            if aoc.Debug.set:
                ax.scatter(p.x, p.y, c='green', marker='s', s=800, alpha=0.5)
            plt.draw()
    print("setin", len(setin))
    p = aoc.P(0,0)  # assuming this is out
    p = min(ps, key=lambda p: p.x)
    p.x -= 1
    assert p.in_bounds
    print("reference point for start of shell:", p)
    setout = set([p]) #shell around setin
    fill = set([p])

    while fill:
        p = fill.pop()
        new = {padj for padj in p.adjacent_4 if padj.in_bounds and (
            padj not in setout and 
            padj not in setin and
            any([
            padjadj in setin for padjadj in padj.adjacent_8
        ]))}
        fill |= new
        setout |= new
        
        # bar_len = 40
        # total = aoc.P.limx * aoc.P.limy - len(setin)
        # progress = len(fill) / max(total, 1)
        # filled = int(bar_len * min(progress, 1.0))
        # bar = '[' + '#' * filled + '-' * (bar_len - filled) + ']'
        # # Pad counts to fixed width
        # fill_count = f"{len(fill):>{len(str(total))}}"
        # total_count = f"{total:>{len(str(total))}}"
        # print(f"Fill: {fill_count}/{total_count} {bar}", end='\r', flush=True)

        if aoc.Debug.set:
            ax.scatter(p.x, p.y, c='blue', marker='s', s=800, alpha=0.5)
            plt.draw()
            plt.pause(0.1)

    print("Finished populating setout")

    # a2pair = {}
    area = 0
    # ans = {P(9,5), P(2,3)}
    for p1,p2 in tqdm(combinations(ps, 2)):
        for pn in (get_perimeter_points(p1, p2)):
            # gpp= list((get_perimeter_points(p1, p2)))
            # p1.plot(), p2.plot()
            # for p in gpp:
            #     p.plot()
            if pn in setout:
                break
        else:
            a = abs((p1.x - p2.x + 1) * (p1.y - p2.y + 1))
            area = max(area, a)

    if aoc.Debug.set:
        plt.ioff()
        plt.show()
    return area


if __name__ == '__main__': 
    data_test, data = get(day, test=True), get(day)
    # part1(data_test, 50)
    # part1(data)
    aoc.Debug.set = True
    
    part2(data_test, 24)
    # part2(data)


    # P.limx, P.limy = 10 , 10
    # p1 = P(2, 2)
    # p2 = P(6,6)
    # for p in get_perimeter_points(p1, p2):
    #     p.plot()
