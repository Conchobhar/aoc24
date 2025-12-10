import bisect
import math
from pathlib import Path
from typing import Any, List, Dict, Set, Tuple
from collections import defaultdict
from itertools import product, permutations, combinations
# product gets every pairing
#   permutations excludes (self, self)
#   combinations excludes ordering
from tqdm import tqdm
import matplotlib.pyplot as plt

import aoc


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


@aoc.part
def part2(data):
    ps = []
    setin = set()
    plt.ion()  # Turn on interactive mode
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
    ax.set_xlim(-1, maxx+1)
    ax.set_ylim(-1, maxy+1)
    for p1, p2 in tqdm(zip(ps, ps[1:] + [ps[0]])):
        axis = 'x' if p1.x != p2.x else 'y'
        vmin, vmax = sorted([getattr(p1, axis), getattr(p2, axis)])
        ax.scatter(p1.x, p1.y, c='red', marker='s', s=800, alpha=0.5)
        ax.scatter(p2.x, p2.y, c='red', marker='s', s=800, alpha=0.5)
        plt.draw()
        setin.add(p1)
        for i in range(vmin+1, vmax):
            coords = (i, p1.y) if axis == 'x' else (p1.x, i)
            p = aoc.P(*coords)
            p.label = 'g'
            setin.add(p)
            ax.scatter(p.x, p.y, c='green', marker='s', s=800, alpha=0.5)
            plt.draw()
    print("setin", len(setin))
    p = aoc.P(0,0)  # assuming this is out
    setout = set([p])
    fill = set([p])

    while fill:
        p = fill.pop()
        new = {padj for padj in p.adjacent_8 if padj.in_bounds and (padj not in setin and padj not in setout)}
        fill |= new
        setout |= new
        print(f"{len(fill)=}, {len(setout)=}")
        ax.scatter(p.x, p.y, c='blue', marker='s', s=800, alpha=0.5)
        plt.draw()
        plt.pause(0.1)

    plt.ioff()  # Turn off interactive mode when done
    plt.show()

            # a = abs((p1.x - p2.x + 1) * (p1.y - p2.y + 1))
    return ...


if __name__ == '__main__': 
    data_test, data = get(day, test=True), get(day)
    part1(data_test, 50)
    part1(data)
    
    part2(data_test, 24)
    # part2(data)
