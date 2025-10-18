import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Pos, get_all_pos, set_char, get_char, get_row_pos, get_col_pos, in_bounds, Direction, get_next_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution


def get_3_consecutive_horiz_and_vert(pos: Pos, V: int, H: int) -> tuple[list[Pos], list[Pos]]:
    """Get 3 consecutive squares, horizontally and vertically, from the given position."""
    horiz = []
    vert = []
    cur_pos = pos
    for _ in range(3):
        if in_bounds(cur_pos, V, H):
            horiz.append(cur_pos)
        cur_pos = get_next_pos(cur_pos, Direction.RIGHT)
    cur_pos = pos
    for _ in range(3):
        if in_bounds(cur_pos, V, H):
            vert.append(cur_pos)
        cur_pos = get_next_pos(cur_pos, Direction.DOWN)
    return horiz, vert


class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert board.shape[0] % 2 == 0, 'board must have even number of rows'
        assert board.shape[1] % 2 == 0, 'board must have even number of columns'
        self.board = board
        self.V = board.shape[0]
        self.H = board.shape[1]
        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[pos] = self.model.NewBoolVar(f'{pos}')

    def add_all_constraints(self):
        # some cells are already filled
        for pos in get_all_pos(self.V, self.H):
            c = get_char(self.board, pos)
            if c == ' ':
                continue
            v = 1 if c == 'B' else 0
            self.model.Add(self.model_vars[pos] == v)
        # no three consecutive squares, horizontally or vertically, are the same colour 
        for pos in get_all_pos(self.V, self.H):
            horiz, vert = get_3_consecutive_horiz_and_vert(pos, self.V, self.H)
            if len(horiz) == 3:
                horiz = [self.model_vars[h] for h in horiz]
                self.model.Add(lxp.Sum(horiz) != 0)
                self.model.Add(lxp.Sum(horiz) != 3)
            if len(vert) == 3:
                vert = [self.model_vars[v] for v in vert]
                self.model.Add(lxp.Sum(vert) != 0)
                self.model.Add(lxp.Sum(vert) != 3)
        # each row and column contains the same number of black and white squares.
        for col in range(self.H):
            var_list = [self.model_vars[pos] for pos in get_col_pos(col, self.V)]
            self.model.Add(lxp.Sum(var_list) == self.V // 2)
        for row in range(self.V):
            var_list = [self.model_vars[pos] for pos in get_row_pos(row, self.H)]
            self.model.Add(lxp.Sum(var_list) == self.H // 2)

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
                if c == ' ':
                    c = 'B' if single_res.assignment[pos] == 1 else 'W'
                set_char(res, pos, c)
            print(res)
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
