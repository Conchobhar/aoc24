import argparse
import math
from pathlib import Path
import time
from typing import *
from typing import Any

import aoc


day = Path(__file__).stem


class Computer:

    def __init__(self) -> None:
        self.A = 0
        self.B = 0
        self.C = 0
        self.P = []
        self.ip = 0
        self.out = []
        self.halted = False
        self.seen = set()

    def combo(self, n:int) -> int:
        match n:
            case 4: return self.A
            case 5: return self.B
            case 6: return self.C
            case 7: return 'invalid'
            case _: return n

    def operate(self, opcode:int, operand:int):
        match opcode:
            case 0:  # adv
                self.A = int(self.A / (2**self.combo(operand)))
            case 1: # bxl - bitwise XOR
                self.B = self.B ^ operand
            case 2:  # bst - bitwise AND
                self.B = self.combo(operand) % 8
            case 3:  # jnz - jump if not zero
                if self.A != 0:
                    self.ip = operand
                    return  # skip ip increment
            case 4:  # bxc - bitwize XOR
                self.B = self.B ^ self.C
            case 5:  # out - output
                self.out.append(self.combo(operand) % 8)
            case 6:  # bdv
                self.B = int(self.A / (2**self.combo(operand)))
            case 7:
                self.C = int(self.A / (2**self.combo(operand)))
        self.ip += 2
        return
    
    def run_deconstructed(self) -> List[int]:
        """Logic for my input 2,4,1,1,7,5,1,5,4,3,5,5,0,3,3,0 as a deconstructed function"""
        out = []
        while self.A > 0:
            b = ((self.A % 8) ^ 1)
            c = int(self.A/(2**b))
            v = b ^ 5 ^ c % 8
            out.append(v)
            self.A = int(self.A/8)
        return out

    def run(self, check=False):
        n = 0
        while True:
            opcode = self.P[self.ip]
            operand = self.P[self.ip+1]
            aoc.debug(f"{n=}, ip={self.ip}, p={opcode},{operand} nout={len(self.out)} B={self.B}, C={self.C}, A={self.A}")
            self.operate(opcode, operand)
            if self.ip >= len(self.P):
                self.halted = True
                break
            if check:
                if self.out != self.P[0:len(self.out)]:
                    break
            n += 1

    def reset(self):
        self.A = 0
        self.B = 0
        self.C = 0
        self.ip = 0
        self.out = []
        self.halted = False

def read_input(name:str):
    cmp = Computer()
    ra,rb,rc, _, p = (aoc.data_path / f'{name}.txt').open().read().strip().split('\n')
    cmp.A = int(ra.split()[-1])
    cmp.B = int(rb.split()[-1])
    cmp.C = int(rc.split()[-1])
    cmp.P = list(map(int, p.split()[-1].split(',')))
    return cmp


def part1(cmp:Computer) -> List[int]:
    cmp.run()
    return ','.join(map(str, cmp.out))


def part2(cmp:Computer) -> int:
    """Find the smallest A that produces the Quine of the program i.e. the output
    of the program is the program itself.

    The program at each loop produces a single output value and reduces the value of A by
    a left bitwise shift of 3. This means to output len(cmp.P) values, A would have to be large enough to
    be shifted left by 3*len(cmp.P) bits before reaching 0.

    We can construct possibilites for A by starting with the most significant bits first
    in groups of 3 bits (octets). We know at the end of the program the last 3 bits must produce the last value of the program which
    is only 2**3 possibilities. Once we find all possible octets, we can then work out the next 3 bits, checking over
    len(possible_values)*2**3 values, left shifting the possible_values before adding the octet to test.

    Most significant bits determine the last outputs of the program 
        0b101001010... -> P[..., 0, 3, 3, 0]
        ^^^      determines               ^   
        0b101001010... -> P[..., 0, 3, 3, 0]
        ^^^^^^   determines            ^  ^

    i.e. we can reduce the search space by working backwords from the end of the program
    """
    # keep track of possible most-significant bits for A
    possible = [0]
    for pidx in range(1, len(cmp.P)+1):
        next_possible = []
        for poss in possible:
            for oct in range(2**3):
                cmp.reset()
                a = poss << 3 | oct  # shift left 3 bits and add the octet
                cmp.A = a
                cmp.run()
                if cmp.out == cmp.P[-pidx:]:  # if output for this is the same as the tail of the program, add it to possible
                    next_possible.append(a)
        possible = next_possible
    return min(next_possible)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()
    if args.debug:
        aoc.Debug.set = True
        
    cmp = Computer()
    cmp.reset()
    cmp.A = 2024
    cmp.P = [0,1,5,4,3,0]
    cmp.run()
    assert cmp.out == [4,2,5,6,7,7,7,7,3,1,0]
    assert cmp.A == 0
    cmp.reset()
    cmp.B = 29
    cmp.P = [1, 7]
    cmp.run()
    assert cmp.B == 26
    cmp.reset()
    cmp.B = 2024
    cmp.C = 43690
    cmp.P = [4, 0]
    cmp.run()
    assert cmp.B == 44354

    cmp = read_input(f'{day}_test')
    assert part1(cmp) == '4,6,3,5,6,3,5,2,1,0'
    print(part1(read_input(day)))  # 7,5,4,3,4,5,3,4,6

    cmp = read_input(day)
    cmp.reset()
    cmp.A = 117440
    cmp.P = [0,3,5,4,3,0]
    cmp.run()
    assert cmp.out == cmp.P
    assert part2(cmp) == 117440
    print(part2(read_input(day)))
