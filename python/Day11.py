from functools import cache
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
def blink(s:str) -> List[str]:
    """
    if 0 -> 1
    elif even digits -> (left, right) split, drop leading zeros
    else x *2024
    """
    if s == '0':
        return ['1']
    elif len(s) % 2 == 0:
        return [s[:len(s)//2], str(int(s[len(s)//2:]))]
    else:
        return [str(int(s) * 2024)]


def part1(stones:List[str], blinks) -> int:
    for ib in range(blinks):
        prog_print(f"{ib=}/{blinks} {len(stones)=}")
        post_stones = []
        debug(f'blink {ib} stones {stones}')
        for i, s in enumerate(stones):
            stones = blink(s)
            post_stones.extend(stones)
        stones = post_stones
    return len(stones)


@cache
def blinkl(t:Tuple[str]) -> Tuple[str]:
    mid = len(t) // 2
    if mid > 0:
        return blinkl(t[0:mid]) + blinkl(t[mid:])
    else:
        return tuple(blink(t[0]))


def part2(stones:List[str], blinks=75) -> int:
    stones = tuple(stones)
    for ib in range(blinks):
        prog_print(f"{ib=}/{blinks} {len(stones)=}")
        debug(f'blink {ib} stones {stones}')
        stones = blinkl(stones)
    return len(stones)


if __name__ == '__main__':
    DEBUG = False
    input_test = read_input(f'{day}_test')
    assert part1(input_test, 25) == 55312
    print(part1(read_input(day), 25))
    # assert part2(input_test) == ...
    print(part2(read_input(day)))
