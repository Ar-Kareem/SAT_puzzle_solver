import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, set_char, get_neighbors8, get_row_pos, get_col_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function, id_board_to_wall_fn


class Board:
    def __init__(self, board: np.array, star_count: int = 1, shapeless: bool = False):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert board.shape[0] == board.shape[1], 'board must be square'
        assert star_count >= 1 and isinstance(star_count, int), 'star_count must be an integer greater than or equal to 1'
        self.board = board
        self.V = board.shape[0]
        self.H = board.shape[1]
        self.N = self.V * self.H
        self.star_count = star_count
        self.shapeless = shapeless
        if not shapeless:
            assert all((str(c.item()).isdecimal() for c in np.nditer(board))), 'board must contain only digits'
            self.block_numbers = set([int(c.item()) for c in np.nditer(board)])
            self.blocks = {i: [pos for pos in get_all_pos(self.V, self.H) if int(get_char(self.board, pos)) == i] for i in self.block_numbers}
        else:
            assert all((str(c.item()) in [' ', 'B'] for c in np.nditer(board))), 'board must contain only digits'
        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[pos] = self.model.NewBoolVar(f'{pos}')

    def add_all_constraints(self):
        # N stars per row / column
        for row in range(self.V):
            self.model.Add(sum(self.model_vars[pos] for pos in get_row_pos(row, H=self.H)) == self.star_count)
        for col in range(self.H):
            self.model.Add(sum(self.model_vars[pos] for pos in get_col_pos(col, V=self.V)) == self.star_count)
        if self.shapeless:  # shapeless version = no blocks but disallow black cells
            for pos in get_all_pos(self.V, self.H):
                if get_char(self.board, pos) == 'B':
                    self.model.Add(self.model_vars[pos] == 0)
        else:  # shaped version = blocks
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
                if single_res.assignment[pos] == 1:
                    set_char(res, pos, 'X')
                else:
                    b = get_char(self.board, pos)
                    if b == 'B':
                        set_char(res, pos, ' ')
                    else:
                        set_char(res, pos, '.')
            print(combined_function(self.V, self.H,
                cell_flags=id_board_to_wall_fn(self.board),
                center_char=lambda r, c: res[r][c]
            ))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
