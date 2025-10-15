from dataclasses import dataclass
from typing import Tuple, Iterable
from enum import Enum

import numpy as np


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

@dataclass(frozen=True)
class Pos:
    x: int
    y: int


def get_pos(x: int, y: int) -> Pos:
    return Pos(x=x, y=y)


def get_next_pos(cur_pos: Pos, direction: Direction) -> Pos:
    delta_x, delta_y = get_deltas(direction)
    return get_pos(cur_pos.x+delta_x, cur_pos.y+delta_y)


def get_neighbors4(pos: Pos, V: int, H: int) -> Iterable[Pos]:
    for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
        p2 = get_pos(x=pos.x+dx, y=pos.y+dy)
        if in_bounds(p2, V, H):
            yield p2


def get_neighbors8(pos: Pos, V: int, H: int = None, include_self: bool = False) -> Iterable[Pos]:
    if H is None:
        H = V
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if not include_self and (dx, dy) == (0, 0):
                continue
            d_pos = get_pos(x=pos.x+dx, y=pos.y+dy)
            if in_bounds(d_pos, V, H):
                yield d_pos


def get_row_pos(row_idx: int, H: int) -> Iterable[Pos]:
    for x in range(H):
        yield get_pos(x=x, y=row_idx)


def get_col_pos(col_idx: int, V: int) -> Iterable[Pos]:
    for y in range(V):
        yield get_pos(x=col_idx, y=y)


def get_all_pos(V, H=None):
    if H is None:
        H = V
    for y in range(V):
        for x in range(H):
            yield get_pos(x=x, y=y)


def get_all_pos_to_idx_dict(V, H=None) -> dict[Pos, int]:
    if H is None:
        H = V
    return {get_pos(x=x, y=y): y*H+x for y in range(V) for x in range(H)}


def get_char(board: np.array, pos: Pos) -> str:
    return board[pos.y][pos.x]


def set_char(board: np.array, pos: Pos, char: str):
    board[pos.y][pos.x] = char


def in_bounds(pos: Pos, V: int, H: int = None) -> bool:
    if H is None:
        H = V
    return 0 <= pos.y < V and 0 <= pos.x < H


def get_deltas(direction: Direction) -> Tuple[int, int]:
    if direction == Direction.RIGHT:
        return +1, 0
    elif direction == Direction.LEFT:
        return -1, 0
    elif direction == Direction.DOWN:
        return 0, +1
    elif direction == Direction.UP:
        return 0, -1
    else:
        raise ValueError
