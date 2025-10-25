import numpy as np
from typing import Union, Callable, Optional, List, Sequence, Literal
from puzzle_solver.core.utils import Pos, get_all_pos, get_next_pos, in_bounds, set_char, get_char, Direction


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

def render_shaded_grid(V: int,
                       H: int,
                       is_shaded: Callable[[int, int], bool],
                       *,
                       scale_x: int = 2,
                       scale_y: int = 1,
                       fill_char: str = '▒',
                       empty_char: str = ' ',
                       empty_text: Optional[Union[str, Callable[[int, int], Optional[str]]]] = None,
                       show_axes: bool = True) -> str:
    """
    Most of this function was AI generated then modified by me, I don't currently care about the details of rendering to the terminal this looked good enough during my testing.
    Visualize a V x H grid where each cell is shaded if is_shaded(r, c) is True.
    The grid lines are always present.

    scale_x: horizontal stretch (>=1). Interior width per cell = 2*scale_x - 1.
    scale_y: vertical stretch (>=1). Interior height per cell = scale_y.
    fill_char: character to fill shaded cell interiors (single char).
    empty_char: background character for unshaded interiors (single char).
    empty_text: Optional text for unshaded cells. If a string, used for all unshaded
                cells. If a callable (r, c) -> str|None, used per cell. Text is
                centered within the interior row and truncated to fit.
    """
    assert V >= 1 and H >= 1
    assert scale_x >= 1 and scale_y >= 1
    assert len(fill_char) == 1 and len(empty_char) == 1

    # ── Layout helpers ─────────────────────────────────────────────────────
    def x_corner(c: int) -> int:                 # column of vertical border at grid column c (0..H)
        return (2 * c) * scale_x
    def y_border(r: int) -> int:                 # row of horizontal border at grid row r (0..V)
        return (scale_y + 1) * r

    rows = y_border(V) + 1
    cols = x_corner(H) + 1
    canvas = [[empty_char] * cols for _ in range(rows)]

    # ── Shading first (borders will overwrite as needed) ───────────────────
    shaded_map = [[False]*H for _ in range(V)]
    for r in range(V):
        top = y_border(r) + 1
        bottom = y_border(r + 1) - 1             # inclusive
        if top > bottom:
            continue
        for c in range(H):
            left  = x_corner(c) + 1
            right = x_corner(c + 1) - 1          # inclusive
            if left > right:
                continue
            shaded = bool(is_shaded(r, c))
            shaded_map[r][c] = shaded
            ch = fill_char if shaded else empty_char
            for yy in range(top, bottom + 1):
                for xx in range(left, right + 1):
                    canvas[yy][xx] = ch

    # ── Grid lines ─────────────────────────────────────────────────────────
    U, Rb, D, Lb = 1, 2, 4, 8
    JUNCTION = {
        0: ' ',
        U: '│', D: '│', U | D: '│',
        Lb: '─', Rb: '─', Lb | Rb: '─',
        U | Rb: '└', Rb | D: '┌', D | Lb: '┐', Lb | U: '┘',
        U | D | Lb: '┤', U | D | Rb: '├', Lb | Rb | U: '┴', Lb | Rb | D: '┬',
        U | Rb | D | Lb: '┼',
    }

    # Horizontal borders (every y_border row)
    for r in range(V + 1):
        yy = y_border(r)
        for c in range(H):
            base = x_corner(c)
            for k in range(1, 2 * scale_x):      # 1..(2*scale_x-1)
                canvas[yy][base + k] = '─'

    # Vertical borders (every x_corner col)
    for c in range(H + 1):
        xx = x_corner(c)
        for r in range(V):
            for ky in range(1, scale_y + 1):
                canvas[y_border(r) + ky][xx] = '│'

    # Junctions at intersections
    for r in range(V + 1):
        yy = y_border(r)
        for c in range(H + 1):
            xx = x_corner(c)
            m = 0
            if r > 0: m |= U
            if r < V: m |= D
            if c > 0: m |= Lb
            if c < H: m |= Rb
            canvas[yy][xx] = JUNCTION[m]

    # ── Optional per-cell text for UNshaded cells ──────────────────────────
    def put_center_text(r_cell: int, c_cell: int, s: str):
        # interior box
        left  = x_corner(c_cell) + 1
        right = x_corner(c_cell + 1) - 1
        top   = y_border(r_cell) + 1
        bottom= y_border(r_cell + 1) - 1
        if left > right or top > bottom:
            return
        span_w = right - left + 1
        # choose middle interior row for text
        yy = top + (bottom - top) // 2
        s = '' if s is None else str(s)
        if len(s) > span_w:
            s = s[:span_w]
        start = left + (span_w - len(s)) // 2
        for i, ch in enumerate(s):
            canvas[yy][start + i] = ch

    if empty_text is not None:
        for r in range(V):
            for c in range(H):
                if not shaded_map[r][c]:
                    s = empty_text(r, c) if callable(empty_text) else empty_text
                    if s:
                        put_center_text(r, c, s)

    # ── Stringify ──────────────────────────────────────────────────────────
    art_rows = [''.join(row) for row in canvas]
    if not show_axes:
        return '\n'.join(art_rows)

    # Axes labels: columns on top; rows on left
    gut = max(2, len(str(V - 1)))
    gutter = ' ' * gut
    top_tens = list(gutter + ' ' * cols)
    top_ones = list(gutter + ' ' * cols)
    for c in range(H):
        xc_center = x_corner(c) + scale_x
        if H >= 10:
            top_tens[gut + xc_center] = str((c // 10) % 10)
        top_ones[gut + xc_center] = str(c % 10)
    if gut >= 2:
        top_tens[gut - 2:gut] = list('  ')
        top_ones[gut - 2:gut] = list('  ')

    labeled = []
    for y, line in enumerate(art_rows):
        mod = y % (scale_y + 1)
        if 1 <= mod <= scale_y:
            r = y // (scale_y + 1)
            mid = (scale_y + 1) // 2
            label = (str(r).rjust(gut) if mod == mid else ' ' * gut)
        else:
            label = ' ' * gut
        labeled.append(label + line)

    return ''.join(top_tens) + '\n' + ''.join(top_ones) + '\n' + '\n'.join(labeled)

CellVal = Literal["B", "W", "TL", "TR", "BL", "BR"]
GridLike = Sequence[Sequence[CellVal]]

def render_bw_tiles_split(
    grid: GridLike,
    cell_w: int = 6,
    cell_h: int = 3,
    borders: bool = False,
    mode: Literal["ansi", "text"] = "ansi",
    text_palette: Literal["solid", "hatch"] = "solid",
    cell_text: Optional[Callable[[int, int], str]] = None) -> str:
    """
    Render a VxH grid with '/' or '\\' splits and optional per-cell centered text.

    `cell_text(r, c) -> str`: if returns non-empty, its first character is drawn
    near the geometric center of cell (r,c), nudged to the black side for halves.
    """

    V = len(grid)
    if V == 0:
        return ""
    H = len(grid[0])
    if any(len(row) != H for row in grid):
        raise ValueError("All rows must have the same length")
    if cell_w < 1 or cell_h < 1:
        raise ValueError("cell_w and cell_h must be >= 1")

    allowed = {"B","W","TL","TR","BL","BR"}
    for r in range(V):
        for c in range(H):
            if grid[r][c] not in allowed:
                raise ValueError(f"Invalid cell value at ({r},{c}): {grid[r][c]}")

    # ── Mode setup ─────────────────────────────────────────────────────────
    use_color = (mode == "ansi")

    def sgr(bg: int | None = None, fg: int | None = None) -> str:
        if not use_color:
            return ""
        parts = []
        if fg is not None: parts.append(str(fg))
        if bg is not None: parts.append(str(bg))
        return ("\x1b[" + ";".join(parts) + "m") if parts else ""

    RESET = "\x1b[0m" if use_color else ""

    BG_BLACK, BG_WHITE = 40, 47
    FG_BLACK, FG_WHITE = 30, 37

    if text_palette == "solid":
        TXT_BLACK, TXT_WHITE = " ", "█"
    elif text_palette == "hatch":
        TXT_BLACK, TXT_WHITE = "░", "▓"
    else:
        raise ValueError("text_palette must be 'solid' or 'hatch'")

    def diag_kind_and_slash(val: CellVal):
        if val in ("TR", "BL"):
            return "main", "\\"
        elif val in ("TL", "BR"):
            return "anti", "/"
        return None, "?"

    def is_black(val: CellVal, fx: float, fy: float) -> bool:
        if val == "B":
            return True
        if val == "W":
            return False
        kind, _ = diag_kind_and_slash(val)
        if kind == "main":         # y = x
            return (fy < fx) if val == "TR" else (fy > fx)
        else:                      # y = 1 - x
            return (fy < 1 - fx) if val == "TL" else (fy > 1 - fx)

    def on_boundary(val: CellVal, fx: float, fy: float) -> bool:
        if val in ("B","W"):
            return False
        kind, _ = diag_kind_and_slash(val)
        eps = 0.5 / max(cell_w, cell_h)   # thin boundary
        if kind == "main":
            return abs(fy - fx) <= eps
        else:
            return abs(fy - (1 - fx)) <= eps

    # Build one tile as a matrix of 1-char tokens (already colorized if ANSI)
    def make_tile(val: CellVal) -> List[List[str]]:
        rows: List[List[str]] = []
        kind, slash_ch = diag_kind_and_slash(val)

        for y in range(cell_h):
            fy = (y + 0.5) / cell_h
            line: List[str] = []
            for x in range(cell_w):
                fx = (x + 0.5) / cell_w

                if val == "B":
                    line.append(sgr(bg=BG_BLACK) + " " + RESET if use_color else TXT_BLACK)
                    continue
                if val == "W":
                    line.append(sgr(bg=BG_WHITE) + " " + RESET if use_color else TXT_WHITE)
                    continue

                black_side = is_black(val, fx, fy)
                boundary   = on_boundary(val, fx, fy)

                if use_color:
                    bg = BG_BLACK if black_side else BG_WHITE
                    if boundary:
                        fg = FG_WHITE if bg == BG_BLACK else FG_BLACK
                        line.append(sgr(bg=bg, fg=fg) + slash_ch + RESET)
                    else:
                        line.append(sgr(bg=bg) + " " + RESET)
                else:
                    if boundary:
                        line.append(slash_ch)
                    else:
                        line.append(TXT_BLACK if black_side else TXT_WHITE)
            rows.append(line)
        return rows

    # Overlay a single character centered (nudged into black side if needed)
    def overlay_center_char(tile: List[List[str]], val: CellVal, ch: str):
        if not ch:
            return
        ch = ch[0]  # keep one character (user said single number)
        cx, cy = cell_w // 2, cell_h // 2
        fx = (cx + 0.5) / cell_w
        fy = (cy + 0.5) / cell_h

        # If center is boundary or not black, nudge horizontally toward black side
        if val in ("TL","TR","BL","BR"):
            kind, _ = diag_kind_and_slash(val)
            # Determine which side is black relative to x at this y
            if kind == "main":  # boundary y=x → compare fx vs fy
                want_right = (val == "TR")  # black is to the right of boundary
                if on_boundary(val, fx, fy) or (is_black(val, fx, fy) is False):
                    if want_right and cx + 1 < cell_w:  cx += 1
                    elif not want_right and cx - 1 >= 0: cx -= 1
            else:               # boundary y=1-x → compare fx vs 1-fy
                want_left = (val == "TL")  # black is to the left of boundary
                if on_boundary(val, fx, fy) or (is_black(val, fx, fy) is False):
                    if want_left and cx - 1 >= 0:        cx -= 1
                    elif not want_left and cx + 1 < cell_w: cx += 1

        # Compose the glyph for that spot
        if use_color:
            # Force black bg + white fg so it pops
            token = sgr(bg=BG_BLACK, fg=FG_WHITE) + ch + RESET
        else:
            # In text mode, just put the raw character
            token = ch
        tile[cy][cx] = token

    # Optional borders
    if borders:
        horiz = "─" * cell_w
        top = "┌" + "┬".join(horiz for _ in range(H)) + "┐"
        mid = "├" + "┼".join(horiz for _ in range(H)) + "┤"
        bot = "└" + "┴".join(horiz for _ in range(H)) + "┘"

    out_lines: List[str] = []
    if borders:
        out_lines.append(top)

    for r in range(V):
        # Build tiles for this row (so we can overlay per-cell text)
        row_tiles: List[List[List[str]]] = []
        for c in range(H):
            t = make_tile(grid[r][c])
            if cell_text is not None:
                label = cell_text(r, c)
                if label:
                    overlay_center_char(t, grid[r][c], label)
            row_tiles.append(t)

        # Emit tile rows
        for y in range(cell_h):
            if borders:
                parts = ["│"]
                for c in range(H):
                    parts.append("".join(row_tiles[c][y]))
                    parts.append("│")
                out_lines.append("".join(parts))
            else:
                out_lines.append("".join("".join(row_tiles[c][y]) for c in range(H)))

        if borders and r < V - 1:
            out_lines.append(mid)

    if borders:
        out_lines.append(bot)

    return "\n".join(out_lines) + (RESET if use_color else "")




# demo = [
#     ["TL","TR","BL","BR","B","W","BL","BR","B","W","TL","TR","BL","BR","B","W","BL","BR","B","W","W","BL","BR","B","W"],
#     ["W","BL","TR","BL","TL","BR","BL","BR","W","W","W","B","TR","BL","TL","BR","BL","BR","B","W","BR","BL","BR","B","W"],
#     ["BR","BL","TR","TL","W","B","BL","BR","B","W","BR","BL","TR","TL","W","B","BL","BR","B","W","B","BL","BR","B","W"],
# ]
# print(render_bw_tiles_split(demo, cell_w=8, cell_h=4, borders=True, mode="ansi"))
# art = render_bw_tiles_split(
#     demo,
#     cell_w=8,
#     cell_h=4,
#     borders=True,
#     mode="text",        # ← key change
#     text_palette="solid"  # try "solid" for stark black/white
# )
# print("```text\n" + art + "\n```")