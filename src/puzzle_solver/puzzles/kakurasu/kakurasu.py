import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, set_char, get_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution


class Board:
    def __init__(self, side: np.array, bottom: np.array):
        assert side.ndim == 1, f'side must be 1d, got {side.ndim}'
        self.V = side.shape[0]
        assert bottom.ndim == 1, f'bottom must be 1d, got {bottom.ndim}'
        self.H = bottom.shape[0]
        self.side = side
        self.bottom = bottom

        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[pos] = self.model.NewBoolVar(f'{pos}')

    def add_all_constraints(self):
        for row in range(self.V):
            self.model.Add(sum([self.model_vars[get_pos(x=col, y=row)] * (col + 1) for col in range(self.H)]) == self.side[row])
        for col in range(self.H):
            self.model.Add(sum([self.model_vars[get_pos(x=col, y=row)] * (row + 1) for row in range(self.V)]) == self.bottom[col])

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, int] = {}
            for pos, var in board.model_vars.items():
                assignment[pos] = solver.value(var)
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.full((self.V, self.H), ' ', dtype=object)
            for pos in get_all_pos(self.V, self.H):
                c = 'X' if single_res.assignment[pos] else ' '
                set_char(res, pos, c)
            print(res)
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
