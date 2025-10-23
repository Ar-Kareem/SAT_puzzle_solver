import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Direction, Pos, get_all_pos, get_next_pos, in_bounds, set_char, get_char, get_neighbors8, get_row_pos, get_col_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution


class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all(c.item() in [' ', 'B', 'W'] for c in np.nditer(board)), 'board must contain only space or B'
        self.board = board
        self.V, self.H = board.shape
        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[pos] = self.model.NewBoolVar(f'{pos}')

    def add_all_constraints(self):
        for pos in get_all_pos(self.V, self.H):  # force clues
            c = get_char(self.board, pos)
            if c == 'B':
                self.model.Add(self.model_vars[pos] == 1)
            elif c == 'W':
                self.model.Add(self.model_vars[pos] == 0)
        # 1. Each row and each column must contain an equal number of white and black circles.
        for row in range(self.V):
            row_vars = [self.model_vars[pos] for pos in get_row_pos(row, self.H)]
            self.model.Add(lxp.sum(row_vars) == len(row_vars) // 2)
        for col in range(self.H):
            col_vars = [self.model_vars[pos] for pos in get_col_pos(col, self.V)]
            self.model.Add(lxp.sum(col_vars) == len(col_vars) // 2)
        # 2. More than two circles of the same color can't be adjacent.
        for pos in get_all_pos(self.V, self.H):
            self.disallow_three_in_a_row(pos, Direction.RIGHT)
            self.disallow_three_in_a_row(pos, Direction.DOWN)
        # 3. Each row and column is unique. 
        # a list per row
        self.force_unique([[self.model_vars[pos] for pos in get_row_pos(row, self.H)] for row in range(self.V)])
        # a list per column
        self.force_unique([[self.model_vars[pos] for pos in get_col_pos(col, self.V)] for col in range(self.H)])

    def disallow_three_in_a_row(self, p1: Pos, direction: Direction):
        p2 = get_next_pos(p1, direction)
        p3 = get_next_pos(p2, direction)
        if any(not in_bounds(p, self.V, self.H) for p in [p1, p2, p3]):
            return
        self.model.AddBoolOr([
            self.model_vars[p1],
            self.model_vars[p2],
            self.model_vars[p3],
        ])
        self.model.AddBoolOr([
            self.model_vars[p1].Not(),
            self.model_vars[p2].Not(),
            self.model_vars[p3].Not(),
        ])

    def force_unique(self, model_vars: list[list[cp_model.IntVar]]):
        if not model_vars or len(model_vars) < 2:
            return
        m = len(model_vars[0])
        assert m <= 61, f"Too many cells for binary encoding in int64: m={m}, model_vars={model_vars}"

        codes = []
        pow2 = [1 << k for k in range(m)]  # weights for bit positions (LSB at index 0)
        for i, l in enumerate(model_vars):
            code = self.model.NewIntVar(0, (1 << m) - 1, f"code_{i}")
            # Sum 2^k * r[k] == code
            self.model.Add(code == sum(pow2[k] * l[k] for k in range(m)))
            codes.append(code)

        self.model.AddAllDifferent(codes)

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, int] = {}
            for pos, var in board.model_vars.items():
                assignment[pos] = solver.Value(var)
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.full((self.V, self.H), ' ', dtype=object)
            for pos in get_all_pos(self.V, self.H):
                c = get_char(self.board, pos)
                c = 'B' if single_res.assignment[pos] == 1 else 'W'
                set_char(res, pos, c)
            print('[')
            for row in res:
                print("    [ '" + "', '".join(row.tolist()) + "' ],")
            print(']')
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
