import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, set_char, get_neighbors8, get_row_pos, get_col_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution


class Board:
    def __init__(self, board: np.array, star_count: int = 1):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert board.shape[0] == board.shape[1], 'board must be square'
        assert star_count >= 1 and isinstance(star_count, int), 'star_count must be an integer greater than or equal to 1'
        assert all((str(c.item()).isdecimal() for c in np.nditer(board))), 'board must contain only digits'
        self.board = board
        self.V = board.shape[0]
        self.H = board.shape[1]
        self.N = self.V * self.H
        self.star_count = star_count
        self.block_numbers = set([int(c.item()) for c in np.nditer(board)])
        self.blocks = {i: [pos for pos in get_all_pos(self.V, self.H) if int(get_char(self.board, pos)) == i] for i in self.block_numbers}

        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[pos] = self.model.NewBoolVar(f'{pos}')

    def add_all_constraints(self):
        # N stars per row / column / block
        for row in range(self.V):
            self.model.Add(sum(self.model_vars[pos] for pos in get_row_pos(row, H=self.H)) == self.star_count)
        for col in range(self.H):
            self.model.Add(sum(self.model_vars[pos] for pos in get_col_pos(col, V=self.V)) == self.star_count)
        for block_i in self.block_numbers:
            self.model.Add(sum(self.model_vars[pos] for pos in self.blocks[block_i]) == self.star_count)
        # stars cant be adjacent
        for pos in get_all_pos(self.V, self.H):
            for neighbor in get_neighbors8(pos, V=self.V, H=self.H):
                self.model.Add(self.model_vars[neighbor] == 0).OnlyEnforceIf(self.model_vars[pos])


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
                c = '*' if single_res.assignment[pos] == 1 else ' '
                set_char(res, pos, c)
            for row in range(self.V):
                print(res[row].tolist(), end='')
                if row != self.V - 1:
                    print(',', end='')
                print()
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
