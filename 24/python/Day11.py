import argparse
from functools import cache, lru_cache
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


def prog_print(s:str):
    print(f"{s}", end='\r', flush=True)


def debug(s:str):
    if DEBUG:
        print(s)


def read_input(name:str) -> List[str]:
    return (data_path / f'{name}.txt').open().read().strip().split(' ')


@cache
def blink(s:str) -> Tuple[str]:
    """Go from one stone to a tuple of one or two stones"""
    if s == '0':
        return ('1',)
    elif len(s) % 2 == 0:
        return (s[:len(s)//2], str(int(s[len(s)//2:])),)
    else:
        return (str(int(s) * 2024),)
    

def blinkn(t:Tuple[str], n) -> Tuple[str]:
    """Maintain collection of stones.
    This requires too much memory for part2.
    """
    mid = len(t) // 2
    if mid > 0:
        return blinkn(t[0:mid], n) + blinkn(t[mid:],n)
    else:
        while len(t) == 1 and n > 0:
            debug(f"{t=} {n=}")
            s = t[0]
            t = blink(s)
            n -= 1    
        if n > 0:
            t = blinkn(t, n)
        return t


@cache
def count_stones_after_blinks(s:str, n) -> int:
    """Only keep track of total count of stones after n blinks."""
    if n == 0:
        return 1
    stones = blink(s)
    return sum(count_stones_after_blinks(s, n-1) for s in stones)


def part1(stones:List[str]) -> int:
    for ib in range(25):
        # prog_print(f"{ib=}/{25} {len(stones)=}")
        post_stones = []
        debug(f'blink {ib} stones {stones}')
        for i, s in enumerate(stones):
            stones = blink(s)
            post_stones.extend(stones)
        stones = post_stones
    return len(stones)


def part2(stones:List[str]) -> int:
    stones = tuple(stones)
    c=0
    for stone in stones:
        c += count_stones_after_blinks(stone, 75)
    return c


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()
    DEBUG = args.debug

    input_test = read_input(f'{day}_test')
    # assert blinkn(('253', '0', '2024', '14168',) , 1) == ('512072', '1', '20', '24', '28676032')
    assert blinkn(('253000', '1', '7',),  2) == ('512072', '1', '20', '24', '28676032')
    assert blinkn(('125','17',) , 3) == ('512072', '1', '20', '24', '28676032')
    assert blinkn(tuple(input_test), 3) == ('512072', '1', '20', '24', '28676032')
    assert len(blinkn(tuple(input_test), 25)) == 55312
    print(part1(read_input(day), 25))
    print(part2(read_input(day)))
