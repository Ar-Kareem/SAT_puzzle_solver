from typing import Union

import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_pos, get_all_pos, get_char, set_char, get_row_pos, get_col_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution


def get_value(board: np.array, pos: Pos) -> Union[int, str]:
    c = get_char(board, pos)
    if c == '*':
        return c
    if str(c).isdecimal():
        return int(c)
    # a,b,... maps to 10,11,...
    return ord(c) - ord('a') + 10


def set_value(board: np.array, pos: Pos, value: Union[int, str]):
    if value == '*':
        value = '*'
    elif value < 10:
        value = str(value)
    else:
        value = chr(value - 10 + ord('a'))
    set_char(board, pos, value)


def get_block_pos(i: int, B: int) -> list[Pos]:
    top_left_x = (i%B)*B
    top_left_y = (i//B)*B
    return [get_pos(x=top_left_x + x, y=top_left_y + y) for x in range(B) for y in range(B)]


class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert board.shape[0] == board.shape[1], 'board must be square'
        assert all(isinstance(i.item(), str) and len(i.item()) == 1 and (i.item().isalnum() or i.item() == '*') for i in np.nditer(board)), 'board must contain only alphanumeric characters or *'
        self.board = board
        self.N = board.shape[0]
        self.B = np.sqrt(self.N)  # block size
        assert self.B.is_integer(), 'board size must be a perfect square'
        self.B = int(self.B)
        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.N):
            self.model_vars[pos] = self.model.NewIntVar(1, self.N, f'{pos}')

    def add_all_constraints(self):
        # some squares are already filled
        for pos in get_all_pos(self.N):
            c = get_value(self.board, pos)
            if c != '*':
                self.model.Add(self.model_vars[pos] == c)
        # every number appears exactly once in each row, each column and each block
        # each row
        for row in range(self.N):
            row_vars = [self.model_vars[pos] for pos in get_row_pos(row, self.N)]
            self.model.AddAllDifferent(row_vars)
        # each column
        for col in range(self.N):
            col_vars = [self.model_vars[pos] for pos in get_col_pos(col, self.N)]
            self.model.AddAllDifferent(col_vars)
        # each block
        for block_i in range(self.N):
            block_vars = [self.model_vars[p] for p in get_block_pos(block_i, self.B)]
            self.model.AddAllDifferent(block_vars)

    def solve_and_print(self):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, int] = {}
            for pos, var in board.model_vars.items():
                assignment[pos] = solver.value(var)
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.full((self.N, self.N), ' ', dtype=object)
            for pos in get_all_pos(self.N):
                c = get_value(self.board, pos)
                c = single_res.assignment[pos]
                set_value(res, pos, c)
            print(res)
        return generic_solve_all(self, board_to_solution, callback=callback)
