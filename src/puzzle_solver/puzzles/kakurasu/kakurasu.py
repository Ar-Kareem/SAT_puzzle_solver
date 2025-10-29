import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


class Board:
    def __init__(self, side: np.array, bottom: np.array):
        assert side.ndim == 1, f'side must be 1d, got {side.ndim}'
        assert bottom.ndim == 1, f'bottom must be 1d, got {bottom.ndim}'
        self.V = side.shape[0]
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
            return SingleSolution(assignment={pos: solver.Value(var) for pos, var in board.model_vars.items()})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H, is_shaded=lambda r, c: single_res.assignment[get_pos(x=c, y=r)]))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
