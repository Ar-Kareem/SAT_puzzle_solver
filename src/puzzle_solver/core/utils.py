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
    if cell_flags is not None:
        N = cell_flags.shape[0]
        H = np.zeros((N+1, N), dtype=bool)
        V = np.zeros((N, N+1), dtype=bool)
        for r in range(N):
            for c in range(N):
                s = cell_flags[r, c]
                if 'U' in s: H[r, c]   = True          # edge between (r,c) and (r, c+1) above the cell
                if 'D' in s: H[r+1, c] = True          # edge below the cell
                if 'L' in s: V[r, c]   = True          # edge left of the cell
                if 'R' in s: V[r, c+1] = True          # edge right of the cell
    assert H is not None and V is not None, 'H and V must be provided'
    # Bitmask for corner connections
    U, R, D, L = 1, 2, 4, 8
    JUNCTION = {
        0: ' ',
        U: '│', D: '│', U|D: '│',
        L: '─', R: '─', L|R: '─',
        U|R: '└', R|D: '┌', D|L: '┐', L|U: '┘',
        U|D|L: '┤', U|D|R: '├', L|R|U: '┴', L|R|D: '┬',
        U|R|D|L: '┼',
    }

    assert scale_x >= 1
    N = V.shape[0]
    assert H.shape == (N+1, N) and V.shape == (N, N+1)

    rows = 2*N + 1
    cols = 2*N*scale_x + 1                 # stretched width
    canvas = [[' ']*cols for _ in range(rows)]

    def x_corner(c):     # x of corner column c
        return (2*c) * scale_x
    def x_between(c,k):  # kth in-between column (1..scale_x) between c and c+1 corners
        return (2*c) * scale_x + k

    # horizontal edges: fill the stretched band between corners with '─'
    for r in range(N+1):
        rr = 2*r
        for c in range(N):
            if H[r, c]:
                # previously: for k in range(1, scale_x*2, 2):
                for k in range(1, scale_x*2):          # 1..(2*scale_x-1), no gaps
                    canvas[rr][x_between(c, k)] = '─'

    # vertical edges: draw at the corner columns (no horizontal stretching needed)
    for r in range(N):
        rr = 2*r + 1
        for c in range(N+1):
            if V[r, c]:
                canvas[rr][x_corner(c)] = '│'

    # junctions at corners
    for r in range(N+1):
        rr = 2*r
        for c in range(N+1):
            m = 0
            if r > 0   and V[r-1, c]: m |= U
            if c < N   and H[r, c]:   m |= R
            if r < N   and V[r, c]:   m |= D
            if c > 0   and H[r, c-1]: m |= L
            canvas[rr][x_corner(c)] = JUNCTION[m]

    # centers
    # ── Centers (now safe for multi-character strings) ──────────────────────
    # We render center text within the interior span (between corner columns),
    # centered if it fits; otherwise we truncate to the span width.
    def put_center_text(rr: int, c: int, text: str):
        # interior span (exclusive of the corner columns)
        left  = x_corner(c) + 1
        right = x_corner(c+1) - 1
        if right < left:
            return  # no interior space (shouldn’t happen when scale_x>=1)
        span_width = right - left + 1

        s = str(text)
        if len(s) > span_width:
            s = s[:span_width]  # hard truncate if it doesn't fit
        # center within the span
        start = left + (span_width - len(s)) // 2
        for i, ch in enumerate(s):
            canvas[rr][start + i] = ch

    if center_char is not None:
        for r in range(N):
            rr = 2*r + 1
            for c in range(N):
                val = center_char if isinstance(center_char, str) else center_char[r, c]
                put_center_text(rr, c, '' if val is None else str(val))

    # turn canvas rows into strings
    art_rows = [''.join(row) for row in canvas]

    if not show_axes:
        return '\n'.join(art_rows)

    # ── Axes ────────────────────────────────────────────────────────────────
    gut = max(2, len(str(N-1)))       # left gutter width
    gutter = ' ' * gut
    top_tens = list(gutter + ' ' * cols)
    top_ones = list(gutter + ' ' * cols)

    for c in range(N):
        xc_center = x_corner(c) + scale_x
        if N >= 10:
            top_tens[gut + xc_center] = str((c // 10) % 10)
        top_ones[gut + xc_center] = str(c % 10)

    # tiny corner labels
    if gut >= 2:
        top_tens[gut-2:gut] = list('  ')
        top_ones[gut-2:gut] = list('  ')

    labeled = []
    for r, line in enumerate(art_rows):
        if r % 2 == 1:                     # cell-center row
            label = str(r//2).rjust(gut)
        else:
            label = ' ' * gut
        labeled.append(label + line)

    return ''.join(top_tens) + '\n' + ''.join(top_ones) + '\n' + '\n'.join(labeled)
