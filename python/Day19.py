import argparse
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

import aoc


day = Path(__file__).stem


def read_input(name:str):
    rules, designs = (aoc.data_path / f'{name}.txt').open().read().strip().split('\n\n')
    rules = rules.split(', ')
    designs = designs.split('\n')
    return rules, designs


def part1(rules, designs) -> int:
    possible_idx = []
    for idx, design in enumerate(designs):
        q = [design]
        while q:
            d = q.pop()
            possible = False
            for r in rules:
                if d.startswith(r):
                    # possible route
                    nd = d.removeprefix(r)
                    # [r for r in rules if d.startswith(r)]
                    if not nd:
                        # finished, count this and break out of design
                        possible_idx.append(idx)
                        possible = True
                        break
                    else:
                        # print(r, nd)
                        # add reduced str to queue
                        q.append(nd)
            if possible:
                # no need to find other routes
                break
        # print(f"{idx=}, {possible=}, {design=}")
    return len(possible_idx)

class TrieNode:

    def __init__(self, s, is_rule=False):
        self.d = {}
        self.s = s
        self.is_rule = is_rule

    def __hash__(self) -> int:
        return hash(self.s)
    
    def __repr__(self) -> str:
        return f"{self.s}{'*' if self.is_rule else ''}"
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def __getitem__(self, s):
        return self.d.get(s)
    
    def add_node(self, s:str, is_rule=False):
        if s not in self.d:
            self.d[s] = TrieNode(s, is_rule)
        return self.d[s]


class Trie:

    def __init__(self, words:List[str]):
        self.root = TrieNode('')
        for word in words:
            self.add_word(word)

    def add_word(self, word:str):
        node = self.root
        for idx in range(0, len(word)):
            new_node = node.add_node(word[0:idx+1])
            node = new_node
        node.is_rule = True
    
    def match(self, word:str):
        node = self.root
        m = []
        for idx in range(len(word)):
            pre = word[0:idx+1]
            node = node[pre]
            if node:
                if node.is_rule:
                    m.append(node.s)
            else:
                break
        return m

@cache
def count_possible(s:str) -> int:
    return sum([count_possible(s.removeprefix(m)) for m in trie.match(s)]) if s else 1


def part2(rules:Trie, designs) -> int:
    global trie
    trie = rules
    return sum([count_possible(d) for d in designs])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()
    if args.debug:
        aoc.Debug.set = True
    
    rules_test, designs_test = read_input(f'{day}_test')
    assert part1(rules_test, designs_test) == 6
    print(part1(*read_input(day)))
    
    global trie
    assert part2(Trie(rules_test), designs_test) == 16
    rules, designs = read_input(day)
    print(part2(Trie(rules), designs))  # 723524534506343
