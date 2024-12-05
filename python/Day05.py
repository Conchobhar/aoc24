from pathlib import Path
from typing import *

day = Path(__file__).stem


def read_input(name:str) -> Tuple[dict[str, Set], List[List[str]]]:
    d1, d2 = Path(f'data/{name}.txt').open().read().split('\n\n')
    rules_raw, reports = d1.split('\n'), [x.split(',') for x in d2.split('\n')]
    rules_map = {}
    for rule in rules_raw:
        k, v = rule.split('|')
        rules_map[k] = rules_map[k] | {v} if k in rules_map else {v}
    return rules_map, reports


def is_valid_report(rules:Dict, report:str) -> bool:
    for i, v in enumerate(report):
        if v in rules:
            pre_v = set(report[:i])
            if pre_v.intersection(rules[v]):
                return False
        else:
            pass
    return True


def part1(rules:Dict, reports:List[List[str]]) -> int:
    c = 0
    for report in reports:
        if is_valid_report(rules, report):
            c += int(report[len(report)//2])
    return c


def fix_report(rules:Dict, report: List[str]) -> List[str]:
    m = {}
    for v in report:
        if v in rules:
            deps = set(report) - {v}
            m[v] = deps.intersection(rules[v])
        else:
            m[v] = {}
    return sorted(m, key = lambda k: len(m[k]), reverse=True)


def part2(rules:Dict, reports:List[str]) -> int:
    c = 0
    for report in reports:
        if not is_valid_report(rules, report):
            report = fix_report(rules, report)
            c += int(report[len(report)//2])
    return c


if __name__ == '__main__':
    rules_test, reports_test = read_input(f'{day}_test')
    assert part1(rules_test, reports_test) == 143
    rules, reports = read_input(day)
    print(part1(rules, reports))
    assert fix_report(rules_test, ['75','97','47','61','53']) == ['97','75','47','61','53']
    assert fix_report(rules_test, ['61','13','29']) == ['61','29','13']
    assert fix_report(rules_test, ['97','13','75','29','47']) == ['97','75','47','29','13']
    assert part2(rules_test, reports_test) == 123
    print(part2(rules, reports))