import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, set_char, get_neighbors4, get_all_pos_to_idx_dict, get_row_pos, get_col_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution, force_connected_component


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
        self.B = {} # black squares
        self.W = {} # white squares
        self.Num = {} # value of squares (Num = N + idx if black, else board[pos])

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.B[pos] = self.model.NewBoolVar(f'B:{pos}')
            self.W[pos] = self.model.NewBoolVar(f'W:{pos}')
            # either black or white
            self.model.AddExactlyOne([self.B[pos], self.W[pos]])
            self.Num[pos] = self.model.NewIntVar(0, 2*self.N, f'{pos}')
            self.model.Add(self.Num[pos] == self.N + self.idx_of[pos]).OnlyEnforceIf(self.B[pos])
            self.model.Add(self.Num[pos] == int(get_char(self.board, pos))).OnlyEnforceIf(self.B[pos].Not())

    def add_all_constraints(self):
        self.no_adjacent_blacks()
        self.no_number_appears_twice()
        self.force_connected_component()

    def no_adjacent_blacks(self):
        # no two black squares are adjacent 
        for pos in get_all_pos(self.V, self.H):
            for neighbor in get_neighbors4(pos, self.V, self.H):
                self.model.Add(self.B[pos] + self.B[neighbor] <= 1)

    def no_number_appears_twice(self):
        # no number appears twice in any row or column (numbers are ignored if black)
        for row in range(self.V):
            var_list = [self.Num[pos] for pos in get_row_pos(row, self.H)]
            self.model.AddAllDifferent(var_list)
        for col in range(self.H):
            var_list = [self.Num[pos] for pos in get_col_pos(col, self.V)]
            self.model.AddAllDifferent(var_list)

    def force_connected_component(self):
        force_connected_component(self.model, self.W)



    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, int] = {}
            for pos, var in board.B.items():
                assignment[pos] = solver.value(var)
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.full((self.V, self.H), ' ', dtype=object)
            for pos in get_all_pos(self.V, self.H):
                c = get_char(self.board, pos)
                c = 'B' if single_res.assignment[pos] == 1 else ' '
                set_char(res, pos, c)
            print(res)
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
