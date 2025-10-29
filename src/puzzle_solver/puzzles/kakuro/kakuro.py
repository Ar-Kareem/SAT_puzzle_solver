from typing import Iterator

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Direction, Pos, get_all_pos, get_next_pos, get_pos, in_bounds, get_char
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


class Board:
    def __init__(self, board: np.array, row_sums: list[list[int]], col_sums: list[list[int]], N: int = 9):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all((c.item() in ['#', ' ', '1', '2', '3', '4', '5', '6', '7', '8', '9']) for c in np.nditer(board)), 'board must contain only #, space, or digits'
        assert len(row_sums) == board.shape[0] and all(isinstance(i, list) and all(isinstance(j, int) or j == '#' for j in i) for i in row_sums), 'row_sums must be a list of lists of integers or #'
        assert len(col_sums) == board.shape[1] and all(isinstance(i, list) and all(isinstance(j, int) or j == '#' for j in i) for i in col_sums), 'col_sums must be a list of lists of integers or #'
        self.board = board
        self.row_sums = row_sums
        self.col_sums = col_sums
        self.V, self.H = board.shape
        self.N = N
        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            if get_char(self.board, pos) == '#':
                continue
            self.model_vars[pos] = self.model.NewIntVar(1, self.N, f'{pos}')

    def get_consecutives(self, pos: Pos, direction: Direction) -> Iterator[list[Pos]]:
        consecutive = []
        while in_bounds(pos, self.V, self.H):
            if get_char(self.board, pos) == '#':
                if len(consecutive) > 0:
                    yield consecutive
                    consecutive = []
            else:
                consecutive.append(pos)
            pos = get_next_pos(pos, direction)
        if len(consecutive) > 0:
            yield consecutive

    def add_all_constraints(self):
        for row in range(self.V):
            row_consecutives = self.get_consecutives(get_pos(x=0, y=row), Direction.RIGHT)
            for i, consecutive in enumerate(row_consecutives):
                # print('row', row, 'i', i, 'consecutive', consecutive)
                self.model.AddAllDifferent([self.model_vars[p] for p in consecutive])
                clue = self.row_sums[row][i]
                if clue != '#':
                    self.model.Add(lxp.sum([self.model_vars[p] for p in consecutive]) == clue)
            assert len(self.row_sums[row]) == i + 1, f'row_sums[{row}] has {len(self.row_sums[row])} clues, but {i + 1} consecutive cells'
        for col in range(self.H):
            col_consecutives = self.get_consecutives(get_pos(x=col, y=0), Direction.DOWN)
            for i, consecutive in enumerate(col_consecutives):
                # print('col', col, 'i', i, 'consecutive', consecutive)
                self.model.AddAllDifferent([self.model_vars[p] for p in consecutive])
                clue = self.col_sums[col][i]
                if clue != '#':
                    self.model.Add(lxp.sum([self.model_vars[p] for p in consecutive]) == clue)
            assert len(self.col_sums[col]) == i + 1, f'col_sums[{col}] has {len(self.col_sums[col])} clues, but {i + 1} consecutive cells'

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, int] = {}
            for pos, var in board.model_vars.items():
                assignment[pos] = solver.Value(var)
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H,
                is_shaded=lambda r, c: self.board[r, c] == '#',
                center_char=lambda r, c: str(single_res.assignment[get_pos(x=c, y=r)]),
                text_on_shaded_cells=False
            ))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
