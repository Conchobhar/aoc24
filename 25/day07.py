import bisect
from pathlib import Path
from typing import Any, List, Dict, Set, Tuple
from collections import defaultdict
from itertools import product, permutations, combinations
# product gets every pairing
#   permutations excludes (self, self)
#   combinations excludes ordering
from tqdm import tqdm

import aoc


day = Path(__file__).stem


def get(day:int, test=False):
    name = f'{day}' + ('_test' if test else '')
    return [list(r) for r in (aoc.data_path / f'{name}.txt').open().read().strip().split('\n')]


@aoc.part
def part1(data) -> int:
    head = data.pop(0)
    beam = [0,] * len(head)
    beam[head.index('S')] = 1
    sc = 0
    for row in data:
        beam_next = beam.copy()
        for i, v in enumerate(row):
            if v == '^':
                if beam[i] == 1:
                    sc += 1
                    beam_next[i-1], beam_next[i+1] = 1, 1
                    beam_next[i] = 0
        beam = beam_next

    return sc


@aoc.part
def part2(data) -> int:
    head = data.pop(0)
    beam = [0,] * len(head)
    beam[head.index('S')] = 1
    for row in data:
        beam_next = beam.copy()
        for i, v in enumerate(row):
            if v == '^':
                if beam[i] > 0:
                    # no. worlds created is current no. worlds on this cell *2
                    #   half go to i-1, half to i+1
                    beam_next[i-1] += beam_next[i]
                    beam_next[i+1] += beam_next[i]
                    beam_next[i] = 0
        aoc.debug([' ' if x == 0 else str(x) for x in beam_next])
        beam = beam_next

    return sum(beam)


if __name__ == '__main__': 
    data_test, data = get(day, test=True), get(day)
    part1(data_test.copy(), 21)
    part1(data.copy(), 1543)
    
    part2(data_test, 40)
    part2(data, 3223365367809)
