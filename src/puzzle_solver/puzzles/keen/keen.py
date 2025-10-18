from typing import Optional

import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, set_char, get_row_pos, get_col_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution


def add_opcode_constraint(model: cp_model.CpModel, vlist: list[cp_model.IntVar], opcode: str, result: int):
    assert opcode in ['+', '-', '*', '/'], "Invalid opcode"
    if opcode in ['-', '/']:
        assert len(vlist) == 2, f"Opcode '{opcode}' requires exactly 2 variables"

    if opcode == '+':
        model.Add(sum(vlist) == result)
    elif opcode == '*':
        model.AddMultiplicationEquality(result, vlist)

    elif opcode == '-':
        # either vlist[0] - vlist[1] == result OR vlist[1] - vlist[0] == result
        b = model.NewBoolVar('sub_dir')
        model.Add(vlist[0] - vlist[1] == result).OnlyEnforceIf(b)
        model.Add(vlist[1] - vlist[0] == result).OnlyEnforceIf(b.Not())
    elif opcode == '/':
        # either v0 / v1 == result or v1 / v0 == result
        b = model.NewBoolVar('div_dir')
        # Ensure no division by zero
        model.Add(vlist[0] != 0)
        model.Add(vlist[1] != 0)
        # case 1: v0 / v1 == result → v0 == v1 * result
        model.Add(vlist[0] == vlist[1] * result).OnlyEnforceIf(b)
        # case 2: v1 / v0 == result → v1 == v0 * result
        model.Add(vlist[1] == vlist[0] * result).OnlyEnforceIf(b.Not())

class Board:
    def __init__(self, board: np.ndarray, block_results: dict[str, tuple[str, int]], clues: Optional[np.ndarray] = None):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert board.shape[0] == board.shape[1], 'board must be square'
        assert clues is None or clues.ndim == 2 and clues.shape[0] == board.shape[0] and clues.shape[1] == board.shape[1], f'clues must be 2d, got {clues.ndim}'
        assert all((c.item().startswith('d') and c.item()[1:].isdecimal()) for c in np.nditer(board)), "board must contain 'd' prefixed digits"
        block_names = set(c.item() for c in np.nditer(board))
        assert set(block_results.keys()).issubset(block_names), f'block results must contain all block names, {block_names - set(block_results.keys())}'
        self.board = board
        self.N = board.shape[0]
        self.block_results = {block: (op, result) for block, (op, result) in block_results.items()}
        self.clues = clues
        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}
        self.create_vars()
        self.add_all_constraints()

    def get_block_pos(self, block: str):
        return [p for p in get_all_pos(self.N) if get_char(self.board, p) == block]

    def create_vars(self):
        for pos in get_all_pos(self.N):
            self.model_vars[pos] = self.model.NewIntVar(1, self.N, f'{pos}')
        if self.clues is not None:
            for pos in get_all_pos(self.N):
                c = get_char(self.clues, pos)
                if int(c) >= 1:
                    self.model.Add(self.model_vars[pos] == int(c))

    def add_all_constraints(self):
        self.unique_digits()
        self.constrain_block_results()

    def unique_digits(self):
        # Each row contains only one occurrence of each digit
        for row in range(self.N):
            row_vars = [self.model_vars[pos] for pos in get_row_pos(row, self.N)]
            self.model.AddAllDifferent(row_vars)
        # Each column contains only one occurrence of each digit
        for col in range(self.N):
            col_vars = [self.model_vars[pos] for pos in get_col_pos(col, self.N)]
            self.model.AddAllDifferent(col_vars)
    
    def constrain_block_results(self):
        # The digits in each block can be combined to form the number stated in the clue, using the arithmetic operation given in the clue. That is: 
        for block, (op, result) in self.block_results.items():
            block_vars = [self.model_vars[p] for p in self.get_block_pos(block)]
            add_opcode_constraint(self.model, block_vars, op, result)

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: "Board", solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, int] = {}
            for p in get_all_pos(board.N):
                assignment[p] = solver.Value(board.model_vars[p])
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.full((self.N, self.N), ' ', dtype=object)
            for pos in get_all_pos(self.N):
                c = get_char(self.board, pos)
                c = single_res.assignment[pos]
                set_char(res, pos, c)
            print(res)
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose, max_solutions=10)
