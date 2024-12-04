from pathlib import Path
from typing import List

def read_input(name:str) -> List[str]:
    return Path(f'src/{name}.txt').open().read().split('\n')


def part1(g:List[str]) -> int:
    """Search over grid once looking along 4 directions for both 'XMAS' and 'SAMX'"""
    deltas = [
        [(0, 1), (0, 2), (0, 3)],
        [(1, 0), (2, 0), (3, 0)],
        [(1, 1), (2, 2), (3, 3)],
        [(1, -1), (2, -2), (3, -3)]
        ]
    found = 0
    ncols, nrows = len(g), len(g[0])
    for ir in range(ncols):
        for ic in range(nrows):
            match g[ir][ic]:
                case 'X':
                    find = 'MAS'
                case 'S':
                    find = 'AMX'
                case _:
                    continue
            
            for delta in deltas:
                any_break = False
                for (ird, icd), char in zip(delta, find):
                    if 0 <= ir+ird < ncols and 0 <= ic+icd < nrows:
                        if g[ir+ird][ic+icd] != char:
                            any_break = True
                            break
                    else:
                        any_break = True
                        break
                if not any_break:
                    found += 1
    return found

def part2(g:List[str]) -> int:
    index_deltas = [
        [(-1, -1), (1, 1)],
        [(-1, 1), (1, -1)]
    ]
    found = 0
    ncols, nrows = len(g), len(g[0])
    for ir in range(ncols):
        for ic in range(nrows):
            if g[ir][ic] == 'A':
                any_break = False
                for ird, icd in index_deltas:
                    if ir+ird[0] in range(ncols) and ic+ird[1] in range(nrows) and ir+icd[0] in range(ncols) and ic+icd[1] in range(nrows):
                        char1 = g[ir+ird[0]][ic+ird[1]]
                        char2 = g[ir+icd[0]][ic+icd[1]]
                        if not (char1 in 'MS' and char2 in 'MS' and char1 != char2):
                            any_break = True
                            break
                    else:
                        any_break = True
                        break
                if not any_break:
                    found += 1
    return found

input_test = read_input('Day04_test')
assert part1(input_test) == 18
print(part1(read_input('Day04')))
assert part2(input_test) == 9
print(part2(read_input('Day04')))
