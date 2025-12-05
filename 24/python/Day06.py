from pathlib import Path
from typing import List
import numpy as np

data_path = Path(__file__).absolute().parents[1] / 'data'
day = Path(__file__).stem


class P:
    """A 2D point"""

    def __init__(self, x:int, y:int) -> None:
        self.x = x
        self.y = y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f'P({self.x}, {self.y})'
    
    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y
    
    def in_bounds(self, a:np.array) -> bool:
        return self.x >= 0 and self.y >= 0 and self.x < a.shape[0] and self.y < a.shape[1]
    

def print_arr(a:np.array, lim=18, p:P=None):
    """print subset of array around point p"""
    if p:
        x, y = p.x, p.y
    else:
        x, y = a.shape
    for i in range(max(0, x-lim), min(x+lim, a.shape[0])):
        print(''.join(a[i, max(0, y-lim):min(y+lim, a.shape[1])]))
    print()


class Patrol:

    dir_cycle = ['^', '>', 'v', '<']
    obstructing_syms = '#O'
    traveresed_syms = '+|-'


    def __init__(self, name:str=None, a:np.array=None, loc:P=None, hypo=False) -> None:
        if a is not None:
            self.a = a
        else:
            self.a:np.array = self.read_input(name)
        self.dir = '^'  # this is the starting dir for all inputs
        self.loc: P = P(np.where(self.a == self.dir)[0][0], np.where(self.a == self.dir)[1][0]) if not loc else loc
        self.loc_init = self.loc
        self.visited = set()
        self.hypo = hypo
        self.obs = set()
        self.dir_changed = False # did dir change last step
        self.is_loop = False

    def read_input(self, name:str) -> List[str]:
        """Go from raw data of form
        '.#..^.....', '........#.',
        to a np array of 0s and 1s
        """
        d = (data_path / f'{name}.txt').open().read().strip().split('\n')
        a = np.array([list(x) for x in d])
        return a
    
    @staticmethod
    def step(loc, dir):
        match dir:
            case '^':
                return P(loc.x - 1, loc.y)
            case '>':
                return P(loc.x, loc.y + 1)
            case 'v':
                return P(loc.x + 1, loc.y)
            case '<':
                return P(loc.x, loc.y - 1)
    
    def traverse(self):
        """Traverse the map
        nloc - next loc after move
        nval - next value after move
        """
        while True:
            # if self.hypo:
            #     print(f"{n=} {self.loc=} {self.dir=}")
            #     print_arr(self.a, p=self.loc)
            #     print()
            if self.dir_changed:
                sym = '+'
            elif self.dir in '^v':
                sym = '|'
            else:
                sym = '-'
            self.a[self.loc.x, self.loc.y] = sym
            nloc = self.step(self.loc, self.dir)
            if nloc.in_bounds(self.a):
                nval = self.a[nloc.x, nloc.y]
            else:
                return
            
            match nval:
                case _ if nval in self.obstructing_syms:  # update dir
                    self.dir_changed = True
                    self.dir = self.dir_cycle[(self.dir_cycle.index(self.dir) +1)%4]
                case _:  # update loc
                    if (self.loc, self.dir) in self.visited:
                        # in loop - set flag and exit
                        self.is_loop = True
                        self.a[self.loc.x, self.loc.y] = self.dir
                        # print(f"Loop detected from {self.loc_init=} {self.dir_init=}")
                        pobs = P(np.where(self.a == 'O')[0][0], np.where(self.a == 'O')[1][0])
                        # print_arr(self.a, lim=6, p=pobs)
                        # print(f"Loops at: {self.loc=} {self.dir=}")
                        # print_arr(self.a, lim=6, p=self.loc)
                        return None
                    if self.hypo:
                        # consider if this was hypothetical
                        ha = self.a.copy()
                        ha[nloc.x, nloc.y] = 'O'
                        hp = Patrol(a=ha,loc=self.loc_init,hypo=False)
                        hp.traverse()
                        if hp.is_loop:
                            self.obs |= {nloc}

                    self.visited |= {(self.loc, self.dir)}
                    self.loc = nloc
                    self.a[self.loc.x, self.loc.y] = self.dir
                    self.dir_changed = False


def part1(patrol:Patrol) -> int:
    patrol.traverse()
    # where a contains one of the symbols in the set
    return np.isin(patrol.a, list(Patrol.traveresed_syms)).sum()


def part2(patrol:Patrol) -> int:
    patrol.traverse()
    return len(patrol.obs - {patrol.loc_init})


if __name__ == '__main__':

    # print options for viewing large arrays in console
    import sys
    import numpy
    numpy.set_printoptions(threshold=sys.maxsize,edgeitems=30, linewidth = 1000000)
    patrol_test = Patrol(f'{day}_test')
    patrol = Patrol(day)
    assert part1(patrol_test) == 41
    print(part1(patrol))  # 5564

    patrol_test = Patrol(f'{day}_test', hypo=True)
    patrol = Patrol(day, hypo=True) 
    assert part2(patrol_test) == 6
    print(part2(patrol_test))
    print(part2(patrol))  # 1976
