import numpy as np

from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Pos, get_all_pos, set_char, get_char, in_bounds, Direction, get_next_pos, get_pos
from puzzle_solver.core.utils_ortools import and_constraint, generic_solve_all, SingleSolution, force_connected_component


class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all(c.item() in [' ', 'B', 'W'] for c in np.nditer(board)), 'board must contain only space, B, or W'
        self.board = board
        self.V, self.H = board.shape
        self.model = cp_model.CpModel()
        self.B: dict[Pos, cp_model.IntVar] = {}
        self.W: dict[Pos, cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.B[pos] = self.model.NewBoolVar(f'B:{pos}')

    def add_all_constraints(self):
        self.force_clues()
        self.disallow_2x2()
        self.disallow_checkers()
        self.force_connected_component()
        self.force_border_transitions()

    def force_clues(self):
        for pos in get_all_pos(self.V, self.H):  # force clues
            c = get_char(self.board, pos)
            if c not in ['B', 'W']:
                continue
            self.model.Add(self.B[pos] == (c == 'B'))

    def disallow_2x2(self):
        for pos in get_all_pos(self.V, self.H):  # disallow 2x2 (WW/WW) and (BB/BB)
            tl = pos
            tr = get_next_pos(pos, Direction.RIGHT)
            bl = get_next_pos(pos, Direction.DOWN)
            br = get_next_pos(bl, Direction.RIGHT)
            if any(not in_bounds(p, self.V, self.H) for p in [tl, tr, bl, br]):
                continue
            self.model.AddBoolOr([self.B[tl], self.B[tr], self.B[bl], self.B[br]])
            self.model.AddBoolOr([self.B[tl].Not(), self.B[tr].Not(), self.B[bl].Not(), self.B[br].Not()])
    
    def disallow_checkers(self):
        # from https://ralphwaldo.github.io/yinyang_summary.html
        for pos in get_all_pos(self.V, self.H):  # disallow (WB/BW) and (BW/WB)
            tl = pos
            tr = get_next_pos(pos, Direction.RIGHT)
            bl = get_next_pos(pos, Direction.DOWN)
            br = get_next_pos(bl, Direction.RIGHT)
            if any(not in_bounds(p, self.V, self.H) for p in [tl, tr, bl, br]):
                continue
            self.model.AddBoolOr([self.B[tl], self.B[tr].Not(), self.B[bl].Not(), self.B[br]])  # disallow (WB/BW)
            self.model.AddBoolOr([self.B[tl].Not(), self.B[tr], self.B[bl], self.B[br].Not()])  # disallow (BW/WB)

    def force_connected_component(self):
        # force single connected component for both colors
        force_connected_component(self.model, self.B)
        force_connected_component(self.model, {k: v.Not() for k, v in self.B.items()})

    def force_border_transitions(self):
        # from https://ralphwaldo.github.io/yinyang_summary.html
        # The border cells cannot be split into four (or more) separate blocks of colours
        # It is therefore either split into two blocks (one of each colour), or is just a single block of one colour or the other
        border_cells = []  # go in a ring clockwise from top left
        for x in range(self.H):
            border_cells.append(get_pos(x=x, y=0))
        for y in range(1, self.V):
            border_cells.append(get_pos(x=self.H-1, y=y))
        for x in range(self.H-2, -1, -1):
            border_cells.append(get_pos(x=x, y=self.V-1))
        for y in range(self.V-2, 0, -1):
            border_cells.append(get_pos(x=0, y=y))
        # tie the knot
        border_cells.append(border_cells[0])
        # unequal sum is 0 or 2
        deltas = []
        for i in range(len(border_cells)-1):
            aux = self.model.NewBoolVar(f'border_transition_{i}')  # i is black while i+1 is white
            and_constraint(self.model, aux, [self.B[border_cells[i]], self.B[border_cells[i+1]].Not()])
            deltas.append(aux)
        self.model.Add(lxp.Sum(deltas) <= 1)


    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, int] = {}
            for pos, var in board.B.items():
                assignment[pos] = 'B' if solver.BooleanValue(var) else 'W'
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.full((self.V, self.H), ' ', dtype=object)
            for pos in get_all_pos(self.V, self.H):
                c = get_char(self.board, pos)
                c = single_res.assignment[pos]
                set_char(res, pos, c)
            print('[')
            for row in res:
                print("    [ '" + "', '".join(row.tolist()) + "' ],")
            print(']')
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
