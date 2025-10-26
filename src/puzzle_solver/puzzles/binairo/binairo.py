from typing import Optional

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Direction, Pos, get_all_pos, get_next_pos, get_pos, in_bounds, get_char, get_row_pos, get_col_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import render_shaded_grid


class Board:
    def __init__(self, board: np.array, arith_rows: Optional[np.array] = None, arith_cols: Optional[np.array] = None, force_unique: bool = True):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all(c.item() in [' ', 'B', 'W'] for c in np.nditer(board)), 'board must contain only space or B'
        self.board = board
        self.V, self.H = board.shape
        if arith_rows is not None:
            assert arith_rows.ndim == 2, f'arith_rows must be 2d, got {arith_rows.ndim}'
            assert arith_rows.shape == (self.V, self.H-1), f'arith_rows must be one column less than board, got {arith_rows.shape} for {board.shape}'
            assert all(isinstance(c.item(), str) and c.item() in [' ', 'x', '='] for c in np.nditer(arith_rows)), 'arith_rows must contain only space, x, or ='
        if arith_cols is not None:
            assert arith_cols.ndim == 2, f'arith_cols must be 2d, got {arith_cols.ndim}'
            assert arith_cols.shape == (self.V-1, self.H), f'arith_cols must be one column and row less than board, got {arith_cols.shape} for {board.shape}'
            assert all(isinstance(c.item(), str) and c.item() in [' ', 'x', '='] for c in np.nditer(arith_cols)), 'arith_cols must contain only space, x, or ='
        self.arith_rows = arith_rows
        self.arith_cols = arith_cols
        self.force_unique = force_unique

        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[pos] = self.model.NewBoolVar(f'{pos}')

    def add_all_constraints(self):
        for pos in get_all_pos(self.V, self.H):  # force clues
            c = get_char(self.board, pos)
            if c == 'B':
                self.model.Add(self.model_vars[pos] == 1)
            elif c == 'W':
                self.model.Add(self.model_vars[pos] == 0)
        # 1. Each row and each column must contain an equal number of white and black circles.
        for row in range(self.V):
            row_vars = [self.model_vars[pos] for pos in get_row_pos(row, self.H)]
            self.model.Add(lxp.sum(row_vars) == len(row_vars) // 2)
        for col in range(self.H):
            col_vars = [self.model_vars[pos] for pos in get_col_pos(col, self.V)]
            self.model.Add(lxp.sum(col_vars) == len(col_vars) // 2)
        # 2. More than two circles of the same color can't be adjacent.
        for pos in get_all_pos(self.V, self.H):
            self.disallow_three_in_a_row(pos, Direction.RIGHT)
            self.disallow_three_in_a_row(pos, Direction.DOWN)

        # 3. Each row and column is unique.
        if self.force_unique:
            # a list per row
            self.force_unique_double_list([[self.model_vars[pos] for pos in get_row_pos(row, self.H)] for row in range(self.V)])
            # a list per column
            self.force_unique_double_list([[self.model_vars[pos] for pos in get_col_pos(col, self.V)] for col in range(self.H)])

        # if arithmetic is provided, add constraints for it
        if self.arith_rows is not None:
            assert self.arith_rows.shape == (self.V, self.H-1), f'arith_rows must be one column less than board, got {self.arith_rows.shape} for {self.board.shape}'
            for pos in get_all_pos(self.V, self.H-1):
                c = get_char(self.arith_rows, pos)
                if c == 'x':
                    self.model.Add(self.model_vars[pos] != self.model_vars[get_next_pos(pos, Direction.RIGHT)])
                elif c == '=':
                    self.model.Add(self.model_vars[pos] == self.model_vars[get_next_pos(pos, Direction.RIGHT)])
        if self.arith_cols is not None:
            assert self.arith_cols.shape == (self.V-1, self.H), f'arith_cols must be one row less than board, got {self.arith_cols.shape} for {self.board.shape}'
            for pos in get_all_pos(self.V-1, self.H):
                c = get_char(self.arith_cols, pos)
                if c == 'x':
                    self.model.Add(self.model_vars[pos] != self.model_vars[get_next_pos(pos, Direction.DOWN)])
                elif c == '=':
                    self.model.Add(self.model_vars[pos] == self.model_vars[get_next_pos(pos, Direction.DOWN)])


    def disallow_three_in_a_row(self, p1: Pos, direction: Direction):
        p2 = get_next_pos(p1, direction)
        p3 = get_next_pos(p2, direction)
        if any(not in_bounds(p, self.V, self.H) for p in [p1, p2, p3]):
            return
        self.model.AddBoolOr([
            self.model_vars[p1],
            self.model_vars[p2],
            self.model_vars[p3],
        ])
        self.model.AddBoolOr([
            self.model_vars[p1].Not(),
            self.model_vars[p2].Not(),
            self.model_vars[p3].Not(),
        ])

    def force_unique_double_list(self, model_vars: list[list[cp_model.IntVar]]):
        if not model_vars or len(model_vars) < 2:
            return
        m = len(model_vars[0])
        assert m <= 61, f"Too many cells for binary encoding in int64: m={m}, model_vars={model_vars}"

        codes = []
        pow2 = [1 << k for k in range(m)]  # weights for bit positions (LSB at index 0)
        for i, line in enumerate(model_vars):
            code = self.model.NewIntVar(0, (1 << m) - 1, f"code_{i}")
            # Sum 2^k * r[k] == code
            self.model.Add(code == sum(pow2[k] * line[k] for k in range(m)))
            codes.append(code)

        self.model.AddAllDifferent(codes)

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, int] = {}
            for pos, var in board.model_vars.items():
                assignment[pos] = solver.Value(var)
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(render_shaded_grid(self.V, self.H, lambda r, c: single_res.assignment[get_pos(x=c, y=r)] == 1))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
