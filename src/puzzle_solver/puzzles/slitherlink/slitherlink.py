import numpy as np
from collections import defaultdict
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, set_char, get_pos, Direction, get_row_pos, get_col_pos, get_next_pos, in_bounds, get_opposite_direction
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution, force_connected_component


CellBorder = tuple[Pos, Direction]
Corner = Pos


class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all(c.item() == ' ' or str(c.item()).isdecimal() for c in np.nditer(board)), 'board must contain only spaces or digits'
        self.V = board.shape[0]
        self.H = board.shape[1]
        self.board = board
        self.cell_borders_to_corners: dict[CellBorder, set[Corner]] = defaultdict(set)  # for every cell border, a set of all corners it is connected to
        self.corners_to_cell_borders: dict[Corner, set[CellBorder]] = defaultdict(set)  # opposite direction

        self.model = cp_model.CpModel()
        self.model_vars: dict[CellBorder, cp_model.IntVar] = {}  # one entry for every unique variable in the model
        self.cell_borders: dict[CellBorder, cp_model.IntVar] = {}  # for every position and direction, one entry for that edge (thus the same edge variables are used in opposite directions of neighboring cells)
        self.corner_vars: dict[Corner, set[cp_model.IntVar]] = defaultdict(set)  # for every corner, one entry for each edge that touches the corner (i.e. 4 per corner unless on the border)

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            for direction in [Direction.RIGHT, Direction.DOWN]:
                self.add_var(pos, direction)
        for pos in get_row_pos(0, self.H):
            self.add_var(pos, Direction.UP)
        for pos in get_col_pos(0, self.V):
            self.add_var(pos, Direction.LEFT)

    def add_var(self, pos: Pos, direction: Direction):
        cell_border = (pos, direction)
        v = self.model.NewBoolVar(f'main:{cell_border}')
        self.model_vars[cell_border] = v
        self.add_cell_border_var(cell_border, v)
        self.add_corner_vars(cell_border, v)

    def add_cell_border_var(self, cell_border: CellBorder, var: cp_model.IntVar):
        """An edge belongs to two cells unless its on the border in which case it only belongs to one."""
        pos, direction = cell_border
        self.cell_borders[cell_border] = var
        next_pos = get_next_pos(pos, direction)
        if in_bounds(next_pos, self.V, self.H):
            self.cell_borders[(next_pos, get_opposite_direction(direction))] = var
    
    def add_corner_vars(self, cell_border: CellBorder, var: cp_model.IntVar):
        """
        An edge always belongs to two corners. Note that the cell xi,yi has the 4 corners (xi,yi), (xi+1,yi), (xi,yi+1), (xi+1,yi+1). (memorize these 4 coordinates or the function wont make sense)
        Thus corner index is +1 of board coordinates.
        Never check for bounds here because an edge ALWAYS touches two corners AND because the +1 will make in_bounds return False when its still in bounds.
        """
        pos, direction = cell_border
        if direction == Direction.LEFT:  # it touches me and (xi,yi+1)
            corner1 = pos
            corner2 = get_next_pos(pos, Direction.DOWN)
        elif direction == Direction.UP:  # it touches me and (xi+1,yi)
            corner1 = pos
            corner2 = get_next_pos(pos, Direction.RIGHT)
        elif direction == Direction.RIGHT:  # it touches (xi+1,yi) and (xi+1,yi+1)
            corner1 = get_next_pos(pos, Direction.RIGHT)
            corner2 = get_next_pos(corner1, Direction.DOWN)
        elif direction == Direction.DOWN:  # it touches (xi,yi+1) and (xi+1,yi+1)
            corner1 = get_next_pos(pos, Direction.DOWN)
            corner2 = get_next_pos(corner1, Direction.RIGHT)
        else:
            raise ValueError(f'Invalid direction: {direction}')
        self.corner_vars[corner1].add(var)
        self.corner_vars[corner2].add(var)
        self.cell_borders_to_corners[cell_border].add(corner1)
        self.cell_borders_to_corners[cell_border].add(corner2)
        self.corners_to_cell_borders[corner1].add(cell_border)
        self.corners_to_cell_borders[corner2].add(cell_border)

    def add_all_constraints(self):
        for pos in get_all_pos(self.V, self.H):  # enforce cells with numbers
            variables = [self.cell_borders[(pos, direction)] for direction in Direction if (pos, direction) in self.cell_borders]
            val = get_char(self.board, pos)
            if not val.isdecimal():
                continue
            self.model.Add(sum(variables) == int(val))
        for corner in self.corner_vars:  # a corder always has 0 or 2 active edges
            g = self.model.NewBoolVar(f'corner_gate_{corner}')
            self.model.Add(sum(self.corner_vars[corner]) == 0).OnlyEnforceIf(g.Not())
            self.model.Add(sum(self.corner_vars[corner]) == 2).OnlyEnforceIf(g)
        # single connected component
        def is_neighbor(cb1: CellBorder, cb2: CellBorder) -> bool:
            cb1_corners = self.cell_borders_to_corners[cb1]
            cb2_corners = self.cell_borders_to_corners[cb2]
            return len(cb1_corners & cb2_corners) > 0
        force_connected_component(self.model, self.model_vars, is_neighbor=is_neighbor)




    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, str] = {}
            for (pos, direction), var in board.model_vars.items():
                if solver.value(var) == 1:
                    if pos not in assignment:
                        assignment[pos] = ''
                    assignment[pos] += direction.name[0]
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.full((self.V, self.H), ' ', dtype=object)
            for pos in get_all_pos(self.V, self.H):
                if pos not in single_res.assignment:
                    continue
                c = ''.join(sorted(single_res.assignment[pos]))
                set_char(res, pos, c)
            print(render_grid(cell_flags=res, center_char=lambda c, r: self.board[r, c] if self.board[r, c] != ' ' else '·'))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose, max_solutions=999)





def render_grid(cell_flags: np.ndarray = None,
                H: np.ndarray = None,
                V: np.ndarray = None,
                mark_centers: bool = True,
                center_char: str = '·',
                show_axes: bool = True,
                scale_x: int = 2) -> str:
    """
    AI generated this because I don't currently care about the details of rendering to the terminal and I did it in a quick and dirty way while the AI made it in a pretty way, and this looks good during my development.
        cell_flags: np.ndarray of shape (N, N) with characters 'U', 'D', 'L', 'R' to represent the edges of the cells.
    OR:
        H: (N+1, N) horizontal edges between corners
        V: (N,   N+1) vertical edges between corners
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

    # centers (help count exact widths/heights)
    if mark_centers:
        for r in range(N):
            rr = 2*r + 1
            for c in range(N):
                # center lies midway across the stretched span
                xc = x_corner(c) + scale_x          # middle-ish; works for any integer scale_x
                canvas[rr][xc] = center_char if isinstance(center_char, str) else center_char(c, r)

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


