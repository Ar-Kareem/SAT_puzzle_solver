from dataclasses import dataclass
from typing import Tuple, Iterable, Union
from enum import Enum

import numpy as np


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Direction8(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    UP_LEFT = 5
    UP_RIGHT = 6
    DOWN_LEFT = 7
    DOWN_RIGHT = 8

@dataclass(frozen=True, order=True)
class Pos:
    x: int
    y: int

    def __add__(self, other: 'Pos') -> 'Pos':
        return get_pos(self.x + other.x, self.y + other.y)


Shape = frozenset[Pos]  # a shape on the 2d board is just a set of positions


def get_pos(x: int, y: int) -> Pos:
    return Pos(x=x, y=y)


def get_next_pos(cur_pos: Pos, direction: Union[Direction, Direction8]) -> Pos:
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


def get_opposite_direction(direction: Direction) -> Direction:
    if direction == Direction.RIGHT:
        return Direction.LEFT
    elif direction == Direction.LEFT:
        return Direction.RIGHT
    elif direction == Direction.DOWN:
        return Direction.UP
    elif direction == Direction.UP:
        return Direction.DOWN
    else:
        raise ValueError(f'invalid direction: {direction}')


def get_deltas(direction: Union[Direction, Direction8]) -> Tuple[int, int]:
    if direction == Direction.RIGHT or direction == Direction8.RIGHT:
        return +1, 0
    elif direction == Direction.LEFT or direction == Direction8.LEFT:
        return -1, 0
    elif direction == Direction.DOWN or direction == Direction8.DOWN:
        return 0, +1
    elif direction == Direction.UP or direction == Direction8.UP:
        return 0, -1
    elif direction == Direction8.UP_LEFT:
        return -1, -1
    elif direction == Direction8.UP_RIGHT:
        return +1, -1
    elif direction == Direction8.DOWN_LEFT:
        return -1, +1
    elif direction == Direction8.DOWN_RIGHT:
        return +1, +1
    else:
        raise ValueError(f'invalid direction: {direction}')


def polyominoes(N):
    """Generate all polyominoes of size N. Every rotation and reflection is considered different and included in the result.
    Translation is not considered different and is removed from the result (otherwise the result would be infinite).

    Below is the number of unique polyominoes of size N (not including rotations and reflections) and the lenth of the returned result (which includes all rotations and reflections)
    N	name		#shapes		#results
    1	monomino	1			1
    2	domino		1			2
    3	tromino		2			6
    4	tetromino	5			19
    5	pentomino	12			63
    6	hexomino	35			216
    7	heptomino	108			760
    8	octomino	369			2,725
    9	nonomino	1,285		9,910
    10	decomino	4,655		36,446
    11	undecomino	17,073		135,268
    12	dodecomino	63,600		505,861
    Source: https://en.wikipedia.org/wiki/Polyomino

    Args:
        N (int): The size of the polyominoes to generate.

    Returns:
        set[(frozenset[Pos], int)]: A set of all polyominoes of size N (rotated and reflected up to D4 symmetry).
    """
    assert N >= 1, 'N cannot be less than 1'
    # need a frozenset because regular sets are not hashable
    FastShape = frozenset[Tuple[int, int]]
    shapes: set[FastShape] = {frozenset({(0, 0)})}
    for i in range(1, N):
        next_shapes: set[FastShape] = set()
        directions = ((1,0),(-1,0),(0,1)) if i > 1 else (((1,0),(0,1)))  # cannot take left on first step, if confused read: https://louridas.github.io/rwa/assignments/polyominoes/
        for s in shapes:
            # frontier of a single shape: all 4-neighbors of existing cells not already in the shape
            frontier = set()
            for x, y in s:
                # only need to consider 3 directions and neighbors condition is (n.y > 0 or (n.y == 0 and n.x >= 0)) it's obvious if you plot it
                # if confused read: https://louridas.github.io/rwa/assignments/polyominoes/
                for dx, dy in directions:
                    n = (x + dx, y + dy)
                    if n not in s and (n[1] > 0 or (n[1] == 0 and n[0] >= 0)):
                        frontier.add(n)
            for cell in frontier:
                t = s | {cell}
                # normalize by translation only: shift so min x,y is (0,0). This removes translational symmetries.
                minx = min(x for x, y in t)
                miny = min(y for x, y in t)
                t0 = frozenset((x - minx, y - miny) for x, y in t)
                next_shapes.add(t0)
        shapes = next_shapes
    # shapes is now complete, now classify up to D4 symmetry (rotations/reflections), translations ignored
    shapes = {frozenset(Pos(x, y) for x, y in s) for s in shapes}  # regular class, not the dirty-fast one
    return shapes

def polyominoes_with_shape_id(N):
    """Refer to polyominoes() for more details. This function returns a set of all polyominoes of size N (rotated and reflected up to D4 symmetry) along with a unique ID for each polyomino that is unique up to D4 symmetry.
    Args:
        N (int): The size of the polyominoes to generate.

    Returns:
        set[(frozenset[Pos], int)]: A set of all polyominoes of size N (rotated and reflected up to D4 symmetry) along with a unique ID for each polyomino that is unique up to D4 symmetry.
    """
    FastPos = Tuple[int, int]
    FastShape = frozenset[Tuple[int, int]]
    shapes = polyominoes(N)
    shapes = {frozenset((p.x, p.y) for p in s) for s in shapes}
    mats = (
        ( 1, 0,  0, 1),  # regular
        (-1, 0,  0, 1),  # reflect about x
        ( 1, 0,  0,-1),  # reflect about y
        (-1, 0,  0,-1),  # reflect about x and y
        # trnaspose then all 4 above
        ( 0, 1,  1, 0), ( 0, 1, -1, 0), ( 0,-1,  1, 0), ( 0,-1, -1, 0),
    )
    # compute canonical representative for each shape (lexicographically smallest normalized transform)
    shape_to_canon: dict[FastShape, tuple[FastPos, ...]] = {}
    for s in shapes:
        reps: list[tuple[FastPos, ...]] = []
        for a, b, c, d in mats:
            pts = {(a*x + b*y, c*x + d*y) for x, y in s}
            minx = min(x for x, y in pts)
            miny = min(y for x, y in pts)
            rep = tuple(sorted((x - minx, y - miny) for x, y in pts))
            reps.append(rep)
        canon = min(reps)
        shape_to_canon[s] = canon

    canon_set = set(shape_to_canon.values())
    canon_to_id = {canon: i for i, canon in enumerate(sorted(canon_set))}
    result = {(s, canon_to_id[shape_to_canon[s]]) for s in shapes}
    result = {(frozenset(Pos(x, y) for x, y in s), _id) for s, _id in result}
    return result
