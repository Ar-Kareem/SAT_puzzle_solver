import sys
from pathlib import Path

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

sys.path.append(str(Path(__file__).parent.parent))
from core.utils import Pos, get_all_pos, set_char, get_char, get_neighbors8, SingleSolution
from core.utils_ortools import generic_solve_all


class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert board.shape[0] == board.shape[1], 'board must be square'
        assert all((c.item() == '*') or str(c.item()).isdecimal() for c in np.nditer(board)), 'board must contain only * or digits'
        self.board = board
        self.N = board.shape[0]
        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.N):
            self.model_vars[pos] = self.model.NewBoolVar(f'{pos}')

    def add_all_constraints(self):
        for pos in get_all_pos(self.N):
            c = get_char(self.board, pos)
            if not str(c).isdecimal():
                continue
            neighbour_vars = [self.model_vars[p] for p in get_neighbors8(pos, self.N, include_self=True)]
            self.model.Add(lxp.sum(neighbour_vars) == int(c))

    def solve_and_print(self):
        def board_to_assignment(board: Board, solver: cp_model.CpSolverSolutionCallback) -> dict[Pos, str|int]:
            assignment: dict[Pos, int] = {}
            for pos, var in board.model_vars.items():
                assignment[pos] = solver.Value(var)
            return assignment
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.zeros_like(self.board)
            for pos in get_all_pos(self.N):
                c = get_char(self.board, pos)
                c = 'B' if single_res.assignment[pos] == 1 else ' '
                set_char(res, pos, c)
            print(res)
        return generic_solve_all(self, board_to_assignment, callback=callback)
