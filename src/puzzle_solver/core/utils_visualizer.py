import numpy as np
from typing import Callable, Optional, List, Sequence, Literal
from puzzle_solver.core.utils import Pos, get_all_pos, get_next_pos, in_bounds, set_char, get_char, Direction


def combined_function(V: int,
                      H: int,
                      cell_flags: Optional[Callable[[int, int], str]] = None,
                      is_shaded: Optional[Callable[[int, int], bool]] = None,
                      center_char: Optional[Callable[[int, int], str]] = None,
                      special_content: Optional[Callable[[int, int], str]] = None,
                      text_on_shaded_cells: bool = True,
                      scale_x: int = 2,
                      scale_y: int = 1,
                      show_axes: bool = True,
                      show_grid: bool = True,
                    ) -> str:
    """
    Render a V x H grid that can:
      • draw selective edges per cell via cell_flags(r, c) containing any of 'U','D','L','R'
      • shade cells via is_shaded(r, c)
      • place centered text per cell via center_char(r, c)
      • draw interior arms via special_content(r, c) returning any combo of 'U','D','L','R'
             (e.g., 'UR', 'DL', 'ULRD', or '' to leave the interior unchanged).
             Arms extend from the cell’s interior center toward the indicated sides.
      • horizontal stretch (>=1). Interior width per cell = 2*scale_x - 1 (default 2)
      • vertical stretch (>=1). Interior height per cell = scale_y (default 1)
      • show_axes: bool = True, show the axes (columns on top, rows on the left).
      • show_grid: bool = True, show the grid lines.

    Behavior:
      - If cell_flags is None, draws a full grid (all interior and outer borders present).
      - Shading is applied first, borders are drawn on top, and center text is drawn last unless text_on_shaded_cells is False in which case the text is not drawn on shaded cells.
      - Axes are shown (columns on top, rows on the left).

    Draw order:
      1) shading
      2) borders
      3) special_content (interior line arms)
      4) center_char (unless text_on_shaded_cells=False and cell is shaded)
    """
    assert V >= 1 and H >= 1, f'V and H must be >= 1, got {V} and {H}'
    assert cell_flags is None or callable(cell_flags), f'cell_flags must be None or callable, got {cell_flags}'
    assert is_shaded is None or callable(is_shaded), f'is_shaded must be None or callable, got {is_shaded}'
    assert center_char is None or callable(center_char), f'center_char must be None or callable, got {center_char}'
    assert special_content is None or callable(special_content), f'special_content must be None or callable, got {special_content}'

    # Rendering constants
    fill_char: str = '▒'     # single char for shaded interiors
    empty_char: str = ' '    # single char for unshaded interiors

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

    # ── Edge presence arrays derived from cell_flags ──
    # H_edges[r, c] is the horizontal edge between rows r and r+1 above column segment c (shape: (V+1, H))
    # V_edges[r, c] is the vertical edge between cols c and c+1 left of row segment r (shape: (V, H+1))
    if cell_flags is None:
        # Full grid: all horizontal and vertical segments are present
        H_edges = [[show_grid for _ in range(H)] for _ in range(V + 1)]
        V_edges = [[show_grid for _ in range(H + 1)] for _ in range(V)]
    else:
        H_edges = [[False for _ in range(H)] for _ in range(V + 1)]
        V_edges = [[False for _ in range(H + 1)] for _ in range(V)]
        for r in range(V):
            for c in range(H):
                s = cell_flags(r, c) or ''
                if 'U' in s:
                    H_edges[r    ][c] = True
                if 'D' in s:
                    H_edges[r + 1][c] = True
                if 'L' in s:
                    V_edges[r][c    ] = True
                if 'R' in s:
                    V_edges[r][c + 1] = True

    # ── Shading first (borders will overwrite) ─────────────────────────────
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
            shaded = bool(is_shaded(r, c)) if callable(is_shaded) else False
            shaded_map[r][c] = shaded
            ch = fill_char if shaded else empty_char
            for yy in range(top, bottom + 1):
                for xx in range(left, right + 1):
                    canvas[yy][xx] = ch

    # ── Grid lines (respect edge presence) ─────────────────────────────────
    U, Rb, D, Lb = 1, 2, 4, 8
    JUNCTION = {
        0: ' ',
        U: '│', D: '│', U | D: '│',
        Lb: '─', Rb: '─', Lb | Rb: '─',
        U | Rb: '└', Rb | D: '┌', D | Lb: '┐', Lb | U: '┘',
        U | D | Lb: '┤', U | D | Rb: '├', Lb | Rb | U: '┴', Lb | Rb | D: '┬',
        U | Rb | D | Lb: '┼',
    }

    # Horizontal segments
    for r in range(V + 1):
        yy = y_border(r)
        for c in range(H):
            if H_edges[r][c]:
                base = x_corner(c)
                for k in range(1, 2 * scale_x):  # 1..(2*scale_x-1)
                    canvas[yy][base + k] = '─'

    # Vertical segments
    for r in range(V):
        for c in range(H + 1):
            if V_edges[r][c]:
                xx = x_corner(c)
                for ky in range(1, scale_y + 1):
                    canvas[y_border(r) + ky][xx] = '│'

    # Junctions at intersections
    for r in range(V + 1):
        yy = y_border(r)
        for c in range(H + 1):
            xx = x_corner(c)
            m = 0
            if r > 0   and V_edges[r - 1][c]:
                m |= U
            if r < V   and V_edges[r][c]:
                m |= D
            if c > 0   and H_edges[r][c - 1]:
                m |= Lb
            if c < H   and H_edges[r][c]:
                m |= Rb
            canvas[yy][xx] = JUNCTION[m]

    # ── Special interior content (arms) + cross-cell bridges ──────────────
    def draw_special_arms(r_cell: int, c_cell: int, code: Optional[str]):
        if not code:
            return
        s = set(code)
        # interior box
        left  = x_corner(c_cell) + 1
        right = x_corner(c_cell + 1) - 1
        top   = y_border(r_cell) + 1
        bottom= y_border(r_cell + 1) - 1
        if left > right or top > bottom:
            return

        # center of interior
        cx = left + (right - left) // 2
        cy = top  + (bottom - top) // 2

        # draw arms out from center (keep inside interior; don't touch borders)
        if 'U' in s and cy - 1 >= top:
            for yy in range(cy - 1, top - 1, -1):
                canvas[yy][cx] = '│'
        if 'D' in s and cy + 1 <= bottom:
            for yy in range(cy + 1, bottom + 1):
                canvas[yy][cx] = '│'
        if 'L' in s and cx - 1 >= left:
            for xx in range(cx - 1, left - 1, -1):
                canvas[cy][xx] = '─'
        if 'R' in s and cx + 1 <= right:
            for xx in range(cx + 1, right + 1):
                canvas[cy][xx] = '─'
        if '/' in s:
            for xx in range(right - left + 1):
                for yy in range(top - bottom + 1):
                    canvas[top + yy][left + xx] = '/'
        if '\\' in s:
            for xx in range(right - left + 1):
                for yy in range(top - bottom + 1):
                    canvas[top + yy][left + xx] = '\\'

        # center junction
        U_b, R_b, D_b, L_b = 1, 2, 4, 8
        m = 0
        if 'U' in s:
            m |= U_b
        if 'D' in s:
            m |= D_b
        if 'L' in s:
            m |= L_b
        if 'R' in s:
            m |= R_b
        canvas[cy][cx] = JUNCTION.get(m, ' ')

    # pass 1: draw interior arms per cell
    special_map = [[set() for _ in range(H)] for _ in range(V)]
    if callable(special_content):
        for r in range(V):
            for c in range(H):
                flags = set(ch for ch in str(special_content(r, c) or ''))
                special_map[r][c] = flags
                if flags:
                    draw_special_arms(r, c, ''.join(flags))

    # ── Center text (drawn last so it sits atop shading/arms) ─────────────
    def put_center_text(r_cell: int, c_cell: int, s: Optional[str]):
        if s is None:
            return
        s = str(s)
        # interior box
        left  = x_corner(c_cell) + 1
        right = x_corner(c_cell + 1) - 1
        top   = y_border(r_cell) + 1
        bottom= y_border(r_cell + 1) - 1
        if left > right or top > bottom:
            return
        span_w = right - left + 1
        yy = top + (bottom - top) // 2
        if len(s) > span_w:
            s = s[:span_w]  # truncate to protect borders
        start = left + (span_w - len(s)) // 2
        for i, ch in enumerate(s):
            canvas[yy][start + i] = ch


    # helper to get interior-center coordinates
    def _cell_center_rc(r_cell: int, c_cell: int):
        left  = x_corner(c_cell) + 1
        right = x_corner(c_cell + 1) - 1
        top   = y_border(r_cell) + 1
        bottom= y_border(r_cell + 1) - 1
        if left > right or top > bottom:
            return None
        cx = left + (right - left) // 2
        cy = top  + (bottom - top) // 2
        return cy, cx

    # ── REPLACE your place_connector() and "pass 2" with the following ────

    # PASS 2: merge/bridge on every border using bitmasks (works with or without borders)
    if callable(special_content):
        # vertical borders: c in [0..H], between (r,c-1) and (r,c)
        for r in range(V):
            # y (row) where we draw the junction on this border: the interior center row
            cc = _cell_center_rc(r, 0)
            if cc is None:
                continue
            cy = cc[0]
            for c in range(H + 1):
                x = x_corner(c)
                mask = 0
                # base: if the vertical grid line exists here, add U and D
                if V_edges[r][c]:
                    mask |= U | D

                # neighbors pointing toward this vertical border
                left_flags  = special_map[r][c - 1] if c - 1 >= 0 else set()
                right_flags = special_map[r][c]     if c < H       else set()
                if 'R' in left_flags:
                    mask |= Lb
                if 'L' in right_flags:
                    mask |= Rb

                # nothing to draw? leave whatever is already there
                if mask == 0:
                    continue
                canvas[cy][x] = JUNCTION[mask]

        # horizontal borders: r in [0..V], between (r-1,c) and (r,c)
        for c in range(H):
            # x (col) where we draw the junction on this border: the interior center col
            cc = _cell_center_rc(0, c)
            if cc is None:
                continue
            cx = cc[1]
            for r in range(V + 1):
                y = y_border(r)
                mask = 0
                # base: if the horizontal grid line exists here, add L and R
                if r <= V - 1 and H_edges[r][c]:  # H_edges indexed [0..V] x [0..H-1]
                    mask |= Lb | Rb

                # neighbors pointing toward this horizontal border
                up_flags   = special_map[r - 1][c] if r - 1 >= 0 else set()
                down_flags = special_map[r][c]     if r < V      else set()
                if 'D' in up_flags:
                    mask |= U
                if 'U' in down_flags:
                    mask |= D

                if mask == 0:
                    continue
                canvas[y][cx] = JUNCTION[mask]

    if callable(center_char):
        for r in range(V):
            for c in range(H):
                if not text_on_shaded_cells and shaded_map[r][c]:
                    continue
                if not text_on_shaded_cells and special_map[r][c]:
                    continue
                put_center_text(r, c, center_char(r, c))

    # ── Stringify with axes ────────────────────────────────────────────────
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

def id_board_to_wall_fn(id_board: np.array, border_is_wall = True) -> Callable[[int, int], str]:
    """In many instances, we have a 2d array where cell values are arbitrary ids
    and we want to convert it to a 2d array where cell values are walls "U", "D", "L", "R" to represent the edges that separate me from my neighbors that have different ids.
    Args:
        id_board: np.array of shape (N, N) with arbitrary ids.
        border_is_wall: if True, the edges of the board are considered to be walls.
    Returns:
        Callable[[int, int], str] that returns the walls "U", "D", "L", "R" for the cell at (r, c).
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
    return lambda r, c: res[r][c]

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
        if fg is not None:
            parts.append(str(fg))
        if bg is not None:
            parts.append(str(bg))
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

    # Build one tile as a matrix of 1-char tokens (already colorized if ANSI)
    def make_tile(val: CellVal) -> List[List[str]]:
        rows: List[List[str]] = []
        _, slash_ch = diag_kind_and_slash(val)
        for y in range(cell_h):
            fy = (y + 0.5) / cell_h
            line: List[str] = []
            prev = None
            for x in range(cell_w):
                fx = (x + 0.5) / cell_w
                fx_next = (x + 1.5) / cell_w

                if val == "B":
                    line.append(sgr(bg=BG_BLACK) + " " + RESET if use_color else TXT_BLACK)
                    continue
                if val == "W":
                    line.append(sgr(bg=BG_WHITE) + " " + RESET if use_color else TXT_WHITE)
                    continue

                black_side = is_black(val, fx, fy)
                next_black_side = is_black(val, fx_next, fy)
                boundary = False  # if true places a "/" or "\" at the current position
                if prev is not None and not prev and black_side:  # prev white and cur black => boundary now
                    boundary = True
                if black_side and not next_black_side:  # cur black and next white => boundary now
                    boundary = True

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
                prev = black_side
            rows.append(line)
        return rows

    # Overlay a single character centered (nudged into black side if needed)
    def overlay_center_char(tile: List[List[str]], val: CellVal, ch: str):
        if not ch:
            return
        ch = ch[0]  # keep one character (user said single number)
        cx, cy = cell_w // 2, cell_h // 2
        cx -= 1

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
