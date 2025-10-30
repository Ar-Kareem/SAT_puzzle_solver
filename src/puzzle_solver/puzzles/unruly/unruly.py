import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, get_row_pos, get_col_pos, in_bounds, Direction, get_next_pos, get_pos
from puzzle_solver.core.utils_visualizer import combined_function
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution


class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert board.shape[0] % 2 == 0 and board.shape[1] % 2 == 0, 'board must have even number of rows and columns'
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
        for pos in get_all_pos(self.V, self.H):
            # enforce hints
            c = get_char(self.board, pos)
            if c.strip():
                self.model.Add(self.model_vars[pos] == (c.strip() == 'B'))
            # no three consecutive squares, horizontally or vertically, are the same colour
            for direction in [Direction.RIGHT, Direction.DOWN]:
                var_list = [pos]
                for _ in range(2):
                    var_list.append(get_next_pos(var_list[-1], direction))
                if all(in_bounds(v, self.V, self.H) for v in var_list):
                    self.model.Add(lxp.Sum([self.model_vars[v] for v in var_list]) != 0)
                    self.model.Add(lxp.Sum([self.model_vars[v] for v in var_list]) != 3)
        # each row and column contains the same number of black and white squares.
        for col in range(self.H):
            var_list = [self.model_vars[pos] for pos in get_col_pos(col, self.V)]
            self.model.Add(lxp.Sum(var_list) == self.V // 2)
        for row in range(self.V):
            var_list = [self.model_vars[pos] for pos in get_row_pos(row, self.H)]
            self.model.Add(lxp.Sum(var_list) == self.H // 2)

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: solver.Value(var) for pos, var in board.model_vars.items()})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H, is_shaded=lambda r, c: single_res.assignment[get_pos(x=c, y=r)] == 1))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
