import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from core.utils import Pos, get_all_pos, set_char, get_pos, get_char
from core.utils_ortools import generic_solve_all, SingleSolution


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
            if c == '*':
                continue
            v = 1 if c == 'B' else 0
            self.model.Add(self.model_vars[pos] == v)
        # no three consecutive squares, horizontally or vertically, are the same colour 
        for col in range(self.H):
            for i in range(self.V - 2):
                var_list = [self.model_vars[get_pos(x=col, y=j)] for j in range(i, i+3)]
                self.model.Add(lxp.Sum(var_list) != 0)
                self.model.Add(lxp.Sum(var_list) != 3)
        for row in range(self.V):
            for i in range(self.H - 2):
                var_list = [self.model_vars[get_pos(x=j, y=row)] for j in range(i, i+3)]
                self.model.Add(lxp.Sum(var_list) != 0)
                self.model.Add(lxp.Sum(var_list) != 3)
        # each row and column contains the same number of black and white squares.
        for col in range(self.H):
            var_list = [self.model_vars[get_pos(x=col, y=row)] for row in range(self.V)]
            self.model.Add(lxp.Sum(var_list) == self.V // 2)
        for row in range(self.V):
            var_list = [self.model_vars[get_pos(x=col, y=row)] for col in range(self.H)]
            self.model.Add(lxp.Sum(var_list) == self.H // 2)

    def solve_and_print(self):
        def board_to_assignment(board: Board, solver: cp_model.CpSolverSolutionCallback) -> dict[Pos, str|int]:
            assignment: dict[Pos, int] = {}
            for pos, var in board.model_vars.items():
                assignment[pos] = solver.Value(var)
            return assignment
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.full((self.V, self.H), ' ', dtype=object)
            for pos in get_all_pos(self.V, self.H):
                c = get_char(self.board, pos)
                if c == '*':
                    c = 'B' if single_res.assignment[pos] == 1 else 'W'
                set_char(res, pos, c)
            print(res)
        return generic_solve_all(self, board_to_assignment, callback=callback)
