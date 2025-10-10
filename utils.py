from typing import Dict, List, Tuple, Iterable, Optional, Literal
from enum import Enum
from dataclasses import dataclass
import json

import numpy as np


@dataclass(frozen=True)
class Pos:
    x: int
    y: int


Direction = Literal['right', 'left', 'down', 'up']

class Monster(Enum):
    VAMPIRE = ("VA", "vampire")
    ZOMBIE = ("ZO", "zombie")
    GHOST = ("GH", "ghost")


@dataclass
class SingleBeamResult:
    position: Pos
    reflect_count: int


@dataclass(frozen=True)
class SingleSolution:
    assignment: dict[Pos, Monster]


def get_all_monster_types() -> Iterable[tuple[str, str]]:
    for monster in Monster:
        yield monster, monster.value[1]


def can_see(pos: Pos, reflect_count: int, monster: Monster) -> bool:
    if monster == Monster.ZOMBIE:
        return True
    elif monster == Monster.VAMPIRE:
        return reflect_count == 0
    elif monster == Monster.GHOST:
        return reflect_count > 0
    else:
        raise ValueError


def get_deltas(direction: Direction) -> Tuple[int, int]:
    if direction == 'right':
        return +1, 0
    elif direction == 'left':
        return -1, 0
    elif direction == 'down':
        return 0, +1
    elif direction == 'up':
        return 0, -1
    else:
        raise ValueError


def get_pos(x: int, y: int) -> Pos:
    return Pos(x, y)


def get_next_pos(cur_pos: Pos, direction: Direction) -> Pos:
    delta_x, delta_y = get_deltas(direction)
    return Pos(cur_pos.x+delta_x, cur_pos.y+delta_y)


def get_hashable_solution(solution: SingleSolution) -> str:
    result = []
    for pos, monster in solution.assignment.items():
        result.append((pos.x, pos.y, monster.value[0]))
    return json.dumps(result, sort_keys=True)


def get_char(board: np.array, pos: Pos) -> str:
    c = board[pos.y][pos.x]
    assert c in ['//', '\\', '**']
    return c

def set_char(board: np.array, pos: Pos, char: str):
    board[pos.y][pos.x] = char


def in_bounds(pos: Pos, N: int) -> bool:
    return 0 <= pos.y < N and 0 <= pos.x < N
