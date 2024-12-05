from pathlib import Path
from typing import List

day = Path(__file__).stem


def read_input(name:str) -> List[str]:
    return Path(f'data/{name}.txt').open().read().split('\n')


def part1(g:List[str]) -> int:
    return ...


def part2(g:List[str]) -> int:
    return ...


if __name__ == '__main__':
    input_test = read_input(f'{day}_test')
    assert part1(input_test) == ...
    print(part1(read_input(day)))
    assert part2(input_test) == ...
    print(part2(read_input(day)))