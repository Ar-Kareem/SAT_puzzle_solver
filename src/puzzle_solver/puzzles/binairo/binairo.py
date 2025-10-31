from typing import Optional

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Direction, Pos, get_all_pos, get_next_pos, get_pos, in_bounds, get_char, get_row_pos, get_col_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


class Board:
    def __init__(self, board: np.array, arith_rows: Optional[np.array] = None, arith_cols: Optional[np.array] = None, force_unique: bool = True, disallow_three: bool = True):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert board.shape[0] % 2 == 0 and board.shape[1] % 2 == 0, f'board must have even number of rows and columns, got {board.shape[0]}x{board.shape[1]}'
        assert all(c.item() in [' ', 'B', 'W'] for c in np.nditer(board)), 'board must contain only space or B'
        assert arith_rows is None or all(isinstance(c.item(), str) and c.item() in [' ', 'x', '='] for c in np.nditer(arith_rows)), 'arith_rows must contain only space, x, or ='
        assert arith_cols is None or all(isinstance(c.item(), str) and c.item() in [' ', 'x', '='] for c in np.nditer(arith_cols)), 'arith_cols must contain only space, x, or ='
        self.board = board
        self.V, self.H = board.shape
        self.arith_rows = arith_rows
        self.arith_cols = arith_cols
        self.force_unique = force_unique
        self.disallow_three = disallow_three

        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[pos] = self.model.NewBoolVar(f'{pos}')

    def add_all_constraints(self):
        for pos in get_all_pos(self.V, self.H):  # force clues
            c = get_char(self.board, pos).strip()
            if c:
                self.model.Add(self.model_vars[pos] == (c == 'B'))
        # 1. Each row and each column must contain an equal number of white and black circles.
        for row in range(self.V):
            row_vars = [self.model_vars[pos] for pos in get_row_pos(row, self.H)]
            self.model.Add(lxp.sum(row_vars) == len(row_vars) // 2)
        for col in range(self.H):
            col_vars = [self.model_vars[pos] for pos in get_col_pos(col, self.V)]
            self.model.Add(lxp.sum(col_vars) == len(col_vars) // 2)
        # 2. No three consecutive cells of the same color
        if self.disallow_three:
            for pos in get_all_pos(self.V, self.H):
                self.disallow_three_in_a_row(pos, Direction.RIGHT)
                self.disallow_three_in_a_row(pos, Direction.DOWN)
        # 3. Each row and column is unique.
        if self.force_unique:
            self.force_unique_double_list([[self.model_vars[pos] for pos in get_row_pos(row, self.H)] for row in range(self.V)])
            self.force_unique_double_list([[self.model_vars[pos] for pos in get_col_pos(col, self.V)] for col in range(self.H)])
        # if arithmetic is provided, add constraints for it
        if self.arith_rows is not None:
            self.force_arithmetic(self.arith_rows, Direction.RIGHT, self.V, self.H-1)
        if self.arith_cols is not None:
            self.force_arithmetic(self.arith_cols, Direction.DOWN, self.V-1, self.H)

    def disallow_three_in_a_row(self, p1: Pos, direction: Direction):
        p2 = get_next_pos(p1, direction)
        p3 = get_next_pos(p2, direction)
        if all(in_bounds(p, self.V, self.H) for p in [p1, p2, p3]):
            self.model.AddBoolOr([self.model_vars[p1], self.model_vars[p2], self.model_vars[p3]])
            self.model.AddBoolOr([self.model_vars[p1].Not(), self.model_vars[p2].Not(), self.model_vars[p3].Not()])

    def force_unique_double_list(self, model_vars: list[list[cp_model.IntVar]]):
        m = len(model_vars[0])
        assert m <= 61, f'Too many cells for binary encoding in int64: m={m}, model_vars={model_vars}'
        codes = []
        pow2 = [2**k for k in range(m)]
        for i, line in enumerate(model_vars):
            code = self.model.NewIntVar(0, 2**m, f"code_{i}")
            self.model.Add(code == lxp.weighted_sum(line, pow2))  # Sum 2^k * r[k] == code
            codes.append(code)
        self.model.AddAllDifferent(codes)

    def force_arithmetic(self, arith_board: np.array, direction: Direction, V: int, H: int):
        assert arith_board.shape == (V, H), f'arith_board going {direction} expected shape {V}x{H}, got {arith_board.shape}'
        for pos in get_all_pos(V, H):
            c = get_char(arith_board, pos).strip()
            if c == 'x':
                self.model.Add(self.model_vars[pos] != self.model_vars[get_next_pos(pos, direction)])
            elif c == '=':
                self.model.Add(self.model_vars[pos] == self.model_vars[get_next_pos(pos, direction)])

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, int] = {}
            for pos, var in board.model_vars.items():
                assignment[pos] = solver.Value(var)
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H, is_shaded=lambda r, c: single_res.assignment[get_pos(x=c, y=r)] == 1))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
