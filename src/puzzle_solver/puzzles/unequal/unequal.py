from typing import Literal, Optional, Union
from dataclasses import dataclass

import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_row_pos, get_col_pos, set_char, get_pos, get_char
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution

def parse_board(board: np.array) -> tuple[np.array, list[tuple[Pos, Pos, str]]]:
    """Returns the internal board and a list for every pair of positions (p1, p2, comparison_type) where p1 < p2 if comparison_type is '<' otherwise abs(p1 - p2)==1 if comparison_type is '|'"""
    V = int(np.ceil(board.shape[0] / 2))
    H = int(np.ceil(board.shape[1] / 2))
    internal_board = np.full((V, H), ' ', dtype=object)
    pairs = []
    for row_i in range(board.shape[0]):
        for col_i in range(board.shape[1]):
            cell = board[row_i, col_i]
            if row_i % 2 == 0 and col_i % 2 == 0:  # number or empty cell
                if cell == ' ':
                    continue
                # map A to 10, B to 11, etc.
                if str(cell).isalpha() and len(str(cell)) == 1:
                    cell = ord(cell.upper()) - ord('A') + 10
                assert str(cell).isdecimal(), f'expected number at {row_i, col_i}, got {cell}'
                internal_board[row_i // 2, col_i // 2] = int(cell)
            elif row_i % 2 == 0 and col_i % 2 == 1:  # horizontal comparison
                assert cell in ['<', '>', '|', ' '], f'expected <, >, |, or empty cell at {row_i, col_i}, got {cell}'
                if cell == ' ':
                    continue
                p1 = get_pos(x=col_i // 2, y=row_i // 2)
                p2 = get_pos(x=p1.x + 1, y=p1.y)
                if cell == '<':
                    pairs.append((p1, p2, '<'))
                elif cell == '>':
                    pairs.append((p2, p1, '<'))
                elif cell == '|':
                    pairs.append((p1, p2, '|'))
                else:
                    raise ValueError(f'unexpected cell {cell} at {row_i, col_i}')
            elif row_i % 2 == 1 and col_i % 2 == 0:  # vertical comparison
                assert cell in ['∧', '∨', 'U', 'D', 'V', 'n', '-', '|', ' '], f'expected ∧, ∨, U, D, V, n, -, |, or empty cell at {row_i, col_i}, got {cell}'
                if cell == ' ':
                    continue
                p1 = get_pos(x=col_i // 2, y=row_i // 2)
                p2 = get_pos(x=p1.x, y=p1.y + 1)
                if cell in ['∨', 'U', 'V']:
                    pairs.append((p2, p1, '<'))
                elif cell in ['∧', 'D', 'n']:
                    pairs.append((p1, p2, '<'))
                elif cell in ['-', '|']:
                    pairs.append((p1, p2, '|'))
                else:
                    raise ValueError(f'unexpected cell {cell} at {row_i, col_i}')
            else:
                assert cell in [' ', '.', 'X'], f'expected empty cell or dot or X at unused corner {row_i, col_i}, got {cell}'
    return internal_board, pairs


class Board:
    def __init__(self, board: np.array, include_zero_before_letter: bool = True):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert board.shape[0] > 0 and board.shape[1] > 0, 'board must be non-empty'
        self.board, self.pairs = parse_board(board)
        self.V, self.H = self.board.shape
        self.lb = 1
        self.N = max(self.V, self.H)
        if include_zero_before_letter and self.N > 9: # zero is introduced when board gets to 10, then we add 1 letter after that
            self.lb = 0
            self.N -= 1

        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[pos] = self.model.NewIntVar(self.lb, self.N, f'{pos}')

    def add_all_constraints(self):
        for row_i in range(self.V):
            self.model.AddAllDifferent([self.model_vars[pos] for pos in get_row_pos(row_i, self.H)])
        for col_i in range(self.H):
            self.model.AddAllDifferent([self.model_vars[pos] for pos in get_col_pos(col_i, self.V)])
        for p1, p2, comparison_type in self.pairs:
            assert comparison_type in ['<', '|'], f'SHOULD NEVER HAPPEN: invalid comparison type {comparison_type}, expected < or |'
            if comparison_type == '<':
                self.model.Add(self.model_vars[p1] < self.model_vars[p2])
            elif comparison_type == '|':
                v = self.model.NewBoolVar(f'adjacent_{p1}_{p2}')
                self.model.Add(self.model_vars[p1] == self.model_vars[p2] + 1).OnlyEnforceIf(v)
                self.model.Add(self.model_vars[p1] == self.model_vars[p2] - 1).OnlyEnforceIf(v.Not())
        for pos in get_all_pos(self.V, self.H):
            c = get_char(self.board, pos)
            if str(c).isdecimal():
                self.model.Add(self.model_vars[pos] == int(c))

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, int] = {}
            for pos, var in board.model_vars.items():
                assignment[pos] = solver.Value(var)
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.full((self.V, self.H), ' ', dtype=object)
            for pos in get_all_pos(self.V, self.H):
                set_char(res, pos, str(single_res.assignment[pos]))
            print('[')
            for row in range(self.V):
                line = '    [ ' + ' '.join(res[row].tolist()) + ' ]'
                print(line)
            print(']')
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
