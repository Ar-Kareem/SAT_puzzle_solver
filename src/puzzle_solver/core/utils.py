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


def polyominoes(N) -> set[Shape]:
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
        directions = ((1,0),(-1,0),(0,1),(0,-1)) if i > 1 else (((1,0),(0,1)))  # cannot take left on first step, if confused read: https://louridas.github.io/rwa/assignments/polyominoes/
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


def render_grid(cell_flags: np.ndarray,
                center_char: Union[np.ndarray, str, None] = None,
                show_axes: bool = True,
                scale_x: int = 2) -> str:
    """
    most of this function was AI generated then modified by me, I don't currently care about the details of rendering to the terminal this looked good enough during my testing.
    cell_flags: np.ndarray of shape (N, N) with characters 'U', 'D', 'L', 'R' to represent the edges of the cells.
    center_char: np.ndarray of shape (N, N) with the center of the cells, or a string to use for all cells, or None to not show centers.
    scale_x: horizontal stretch factor (>=1). Try 2 or 3 for squarer cells.
    """
    assert cell_flags is not None and cell_flags.ndim == 2
    R, C = cell_flags.shape

    # Edge presence arrays (note the rectangular shapes)
    H = np.zeros((R+1, C), dtype=bool)  # horizontal edges between rows
    V = np.zeros((R, C+1), dtype=bool)  # vertical edges between cols
    for r in range(R):
        for c in range(C):
            s = cell_flags[r, c]
            if 'U' in s: H[r,   c] = True
            if 'D' in s: H[r+1, c] = True
            if 'L' in s: V[r,   c] = True
            if 'R' in s: V[r, c+1] = True

    # Bitmask for corner connections
    U, Rb, D, Lb = 1, 2, 4, 8
    JUNCTION = {
        0: ' ',
        U: '│', D: '│', U|D: '│',
        Lb: '─', Rb: '─', Lb|Rb: '─',
        U|Rb: '└', Rb|D: '┌', D|Lb: '┐', Lb|U: '┘',
        U|D|Lb: '┤', U|D|Rb: '├', Lb|Rb|U: '┴', Lb|Rb|D: '┬',
        U|Rb|D|Lb: '┼',
    }

    assert scale_x >= 1
    assert H.shape == (R+1, C) and V.shape == (R, C+1)

    rows = 2*R + 1
    cols = 2*C*scale_x + 1
    canvas = [[' ']*cols for _ in range(rows)]

    def x_corner(c):     # x of corner column c  (0..C)
        return (2*c) * scale_x
    def x_between(c,k):  # kth in-between col (1..2*scale_x-1) between corners c and c+1
        return (2*c) * scale_x + k

    # horizontal edges: fill the stretched band between corners with '─'
    for r in range(R+1):
        rr = 2*r
        for c in range(C):
            if H[r, c]:
                for k in range(1, scale_x*2):  # 1..(2*scale_x-1)
                    canvas[rr][x_between(c, k)] = '─'

    # vertical edges: at the corner columns
    for r in range(R):
        rr = 2*r + 1
        for c in range(C+1):
            if V[r, c]:
                canvas[rr][x_corner(c)] = '│'

    # junctions at every corner grid point
    for r in range(R+1):
        rr = 2*r
        for c in range(C+1):
            m = 0
            if r > 0   and V[r-1, c]: m |= U
            if c < C   and H[r, c]:   m |= Rb
            if r < R   and V[r, c]:   m |= D
            if c > 0   and H[r, c-1]: m |= Lb
            canvas[rr][x_corner(c)] = JUNCTION[m]

    # centers (safe for multi-character strings)
    def put_center_text(rr: int, c: int, text: str):
        left  = x_corner(c) + 1
        right = x_corner(c+1) - 1
        if right < left:
            return
        span_width = right - left + 1
        s = str(text)
        if len(s) > span_width:
            s = s[:span_width]  # truncate to protect borders
        start = left + (span_width - len(s)) // 2
        for i, ch in enumerate(s):
            canvas[rr][start + i] = ch

    if center_char is not None:
        for r in range(R):
            rr = 2*r + 1
            for c in range(C):
                val = center_char if isinstance(center_char, str) else center_char[r, c]
                put_center_text(rr, c, '' if val is None else str(val))

    # rows -> strings
    art_rows = [''.join(row) for row in canvas]
    if not show_axes:
        return '\n'.join(art_rows)

    # Axes labels: row indices on the left, column indices on top (handle C, not R)
    gut = max(2, len(str(R-1)))  # gutter width based on row index width
    gutter = ' ' * gut
    top_tens = list(gutter + ' ' * cols)
    top_ones = list(gutter + ' ' * cols)

    for c in range(C):
        xc_center = x_corner(c) + scale_x
        if C >= 10:
            top_tens[gut + xc_center] = str((c // 10) % 10)
        top_ones[gut + xc_center] = str(c % 10)

    if gut >= 2:
        top_tens[gut-2:gut] = list('  ')
        top_ones[gut-2:gut] = list('  ')

    labeled = []
    for r, line in enumerate(art_rows):
        if r % 2 == 1:  # cell-center row
            label = str(r//2).rjust(gut)
        else:
            label = ' ' * gut
        labeled.append(label + line)

    return ''.join(top_tens) + '\n' + ''.join(top_ones) + '\n' + '\n'.join(labeled)

def id_board_to_wall_board(id_board: np.array, border_is_wall = True) -> np.array:
    """In many instances, we have a 2d array where cell values are arbitrary ids
    and we want to convert it to a 2d array where cell values are walls "U", "D", "L", "R" to represent the edges that separate me from my neighbors that have different ids.
    Args:
        id_board: np.array of shape (N, N) with arbitrary ids.
        border_is_wall: if True, the edges of the board are considered to be walls.
    Returns:
        np.array of shape (N, N) with walls "U", "D", "L", "R".
    """
    res = np.full((id_board.shape[0], id_board.shape[1]), '', dtype=object)
    V, H = id_board.shape
    def append_char(pos: Pos, s: str):
        set_char(res, pos, get_char(res, pos) + s)
    def handle_pos_direction(pos: Pos, direction: Direction, s: str):
        pos2 = get_next_pos(pos, direction)
        if in_bounds(pos2, V, H):
            if get_char(id_board, pos2) != get_char(id_board, pos):
                append_char(pos, s)
        else:
            if border_is_wall:
                append_char(pos, s)
    for pos in get_all_pos(V, H):
        handle_pos_direction(pos, Direction.LEFT, 'L')
        handle_pos_direction(pos, Direction.RIGHT, 'R')
        handle_pos_direction(pos, Direction.UP, 'U')
        handle_pos_direction(pos, Direction.DOWN, 'D')
    return res