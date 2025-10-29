import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, get_neighbors4, get_all_pos_to_idx_dict, get_row_pos, get_col_pos, get_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution, force_connected_component
from puzzle_solver.core.utils_visualizer import combined_function


class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert board.shape[0] == board.shape[1], 'board must be square'
        self.board = board
        self.V = board.shape[0]
        self.H = board.shape[1]
        self.N = self.V * self.H
        self.idx_of: dict[Pos, int] = get_all_pos_to_idx_dict(self.V, self.H)
        self.model = cp_model.CpModel()
        self.B = {}
        self.W = {}
        self.Num = {} # value of squares (Num = N + idx if black, else board[pos])
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.B[pos] = self.model.NewBoolVar(f'B:{pos}')
            self.W[pos] = self.B[pos].Not()
            self.Num[pos] = self.model.NewIntVar(0, 2*self.N, f'{pos}')
            self.model.Add(self.Num[pos] == self.N + self.idx_of[pos]).OnlyEnforceIf(self.B[pos])
            self.model.Add(self.Num[pos] == int(get_char(self.board, pos))).OnlyEnforceIf(self.W[pos])

    def add_all_constraints(self):
        for pos in get_all_pos(self.V, self.H):  # no two black squares are adjacent
            for neighbor in get_neighbors4(pos, self.V, self.H):
                self.model.Add(self.B[pos] + self.B[neighbor] <= 1)
        for row in range(self.V):  # no number appears twice in any row (numbers are ignored if black)
            self.model.AddAllDifferent([self.Num[pos] for pos in get_row_pos(row, self.H)])
        for col in range(self.H):  # no number appears twice in any column (numbers are ignored if black)
            self.model.AddAllDifferent([self.Num[pos] for pos in get_col_pos(col, self.V)])
        force_connected_component(self.model, self.W)  # all white squares must be a single connected component

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: 1 if solver.Value(val) == 1 else 0 for pos, val in board.B.items()})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H,
                is_shaded=lambda r, c: single_res.assignment[get_pos(x=c, y=r)] == 1,
                center_char=lambda r, c: self.board[r, c],
                text_on_shaded_cells=False
            ))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
