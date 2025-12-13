import bisect
import itertools
from pathlib import Path
from typing import Any, List, Dict, Set, Tuple
from collections import Counter, defaultdict
from itertools import product, permutations, combinations
# product gets every pairing
#   permutations excludes (self, self)
#   combinations excludes ordering
from tqdm import tqdm

import aoc


day = Path(__file__).stem


def get(day:int, test=False):
    name = f'{day}' + ('_test' if test else '')
    rows = []
    for row in (aoc.data_path / f'{name}.txt').open().read().strip().split('\n'):
        ls, *bs, js = row.split()
        nbs = []
        for v in bs:
            v = eval(v)
            if isinstance(v, int):
                v = (v,)
            nbs.append(v)
        nls = []
        for v in ls[1:-1]:
            nls.append((v == '#'))
        njs = []
        for v in js[1:-1].split(','):
            njs.append(int(v))
        rows.append((nls, nbs, njs))
    return rows


@aoc.part
def part1(data) -> int:
    cmins = []
    for row in data:
        ls, bs, _ = row
        cs = []
        valid = []
        for r in range(1, len(bs)+1):
            for c in combinations(bs, r):
                chain = itertools.chain(*c)
                cn = Counter(chain)
                # print(c)
                cs.append(c)
                result = []

                for i in range(len(ls)):
                    if i in cn:
                        result.append(cn[i] % 2)
                    else:
                        result.append(False)

                if result == ls:
                    valid.append(c)
                    
        cmin = min(valid, key=lambda x: len(x))
        cmins.append(len(cmin))
    return sum(cmins)


@aoc.part
def part2(data) -> int:
    cmins = []
    for row in data:
        _, bs, js = row
        cs = []
        valid = []
        for r in tqdm(range(1, max(js)*len(bs))):
            for c in tqdm(combinations(bs*(max(js)), r), total=max(js)**len(bs)):
                chain = itertools.chain(*c)
                cn = Counter(chain)
                # print(c)
                cs.append(c)
                result = []

                for i in range(len(js)):
                    if i in cn:
                        result.append(cn[i])
                    else:
                        result.append(0)
                # for n, v in cn.items():
                #     # if v % 2 == ls[n]:
                #     #     break
                #     if ((not v % 2) == ls[n]):
                #         break
                # else:

                if result == js:
                    valid.append(c)
                    return len(c)
                    
        cmin = min(valid, key=lambda x: len(x))
        cmins.append(len(cmin))
    return sum(cmins)


if __name__ == '__main__': 
    data_test, data = get(day, test=True), get(day)
    part1(data_test, 7)
    # part1(data)
    
    part2(data_test, 33)
    # part2(data)
