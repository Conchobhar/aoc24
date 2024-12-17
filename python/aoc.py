from pathlib import Path
from typing import *

data_path = Path(__file__).absolute().parents[1] / 'data'


class Debug:

    set = False


def prog_print(s:str):
    print(f"{s}", end='\r', flush=True)


def debug(s:str):
    if Debug.set:
        print(s)


class P:
    """Define a 2D point
    
    Limits for x and y are class attribs defining the range of the grid the points are used in.
    These are set by the revelent problem.
    """

    limx = None
    limy = None
    
    @classmethod
    def valid_points(self):
        """Generate all valid points in the grid."""
        if self.limx is None or self.limy is None:
            raise ValueError("Need to set class attribs limx and limy.")
        for x in range(self.limx):
            for y in range(self.limy):
                yield P(x, y)

    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y

    def __add__(self, other):
        return P(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return P(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return P(-self.x, -self.y)

    def __repr__(self): 
        return f'P({self.x}, {self.y})'
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)
    
    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)
    
    @property
    def adjacent(self) -> Set['P']:
        """Get all 4 adjacent (but not necessarily in bounds) points to this one."""
        return set(self + d for d in deltas)
    
    @property
    def in_bounds(self) -> bool:
        if self.limx is None or self.limy is None:
            raise ValueError("Need to set class attribs limx and limy.")
        return (0 <= self.x < self.limx) and (0 <= self.y < self.limy)
    

deltas = [P(0, 1), P(1, 0), P(0, -1), P(-1, 0)]