from pathlib import Path
from typing import *
from typing import Any
import argparse
from collections import defaultdict
from itertools import product, permutations, combinations
# product gets every pairing
#   permutations excludes (self, self)
#   combinations excludes ordering

from tqdm import tqdm
import bisect

data_path = Path(__file__).absolute().parents[1] / 'data'
day = Path(__file__).stem

DEBUG = False 


def debug(s:str):
    if DEBUG:
        print(s)


def read_input(name:str) -> str:
    return (data_path / f'{name}.txt').open().read().strip()


def checksum(l) -> int:
    s = 0
    for i,c in enumerate(l):
        s += i*c if c != '.' else 0
        print(f"{s}", end='\r', flush=True)
    return s


def part1(s:str) -> int:
    l = []
    idc = 0
    for i, c in enumerate(s):
        if i % 2 == 0:
            l += [idc]*int(c)
            idc += 1
        else:
            l += ['.']*int(c)
    lix = 0
    rix = len(l)
    lc, rc = '', '.'
    while lix < rix:
        try:
            print(f"{lix/len(l):.2%} {lix=} {rix=}\r", flush=True, end='')
            while lc != '.' and lix < len(l):
                lc = l[lix]
                lix += 1
            while rc == '.' and rix > lix:
                # GT because once rix equals lix it could pop the last element
                rc = l.pop()
                rix -= 1
            if lix <= rix and rc != '.':
                # LTEQ because lix could equal rix but still require subbing in last value
                l[lix-1] = rc
            debug(f"{lix=}, {lc=}, {rix=}, {rc=}")
            lc, rc = '', '.'
        except Exception as err:
            print(f"{lix=}, {lc=}, {rix=}, {rc=}, {len(l)=}")
            raise(err)
            break
    print(f"{len(l)=}")

    return checksum(l)


def part2(s:str) -> int:
    l = []  # tuples of (file start idx, file length, file id)
    # startidx2length
    files = []
    spaces = []
    idc = 0
    for i, c in enumerate(s):
        if i % 2 == 0:
            files += [(len(l), int(c), idc)]
            l += [idc]*int(c)
            idc += 1
        else:
            spaces += [(len(l), int(c))]
            l += ['.']*int(c)

    for ef, (fix, flen, fid) in enumerate(reversed(files)):
        for es, (six, slen) in enumerate(spaces):
            print(f"{ef/len(files):.2%}\r", flush=True, end='')
            if six > fix:
                break
            if flen <= slen:
                l[six:six+flen] = [l[fix]]*flen
                l[fix:fix+flen] = ['.']*flen
                if flen == slen:
                    del spaces[es]
                else:
                    spaces[es] = (six+flen, slen-flen)
                break
        debug(''.join([str(v) for v in l]))
    return checksum(l)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()
    if args.debug:
        DEBUG = True

    input_test = read_input(f'{day}_test')
    assert part1(input_test) == 1928
    print(part1(read_input(day)))
    assert part2(input_test) == 2858
    print(part2(read_input(day)))  # 6363268339304
