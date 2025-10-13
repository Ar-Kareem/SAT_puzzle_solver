
import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Optional, Callable
from dataclasses import dataclass

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp
from ortools.sat.python.cp_model import CpSolverSolutionCallback

sys.path.append(str(Path(__file__).parent.parent))
from core.utils import Pos, get_pos, get_all_pos, get_char, set_char, in_bounds

@dataclass(frozen=True)
class SingleSolution:
    assignment: dict[Pos, int]


def get_hashable_solution(solution: SingleSolution) -> str:
    result = []
    for pos, v in solution.assignment.items():
        result.append((pos.x, pos.y, v))
    return json.dumps(result, sort_keys=True)


def get_value(board: np.array, pos: Pos) -> int|str:
    c = get_char(board, pos)
    if c == '*':
        return c
    if str(c).isdecimal():
        return int(c)
    # a,b,... maps to 10,11,...
    return ord(c) - ord('a') + 10


def set_value(board: np.array, pos: Pos, value: int|str):
    if value == '*':
        value = '*'
    elif value < 10:
        value = str(value)
    else:
        value = chr(value - 10 + ord('a'))
    set_char(board, pos, value)


def get_block_pos(i: int, B: int) -> list[Pos]:
    top_left = Pos(x=(i%B)*B, y=(i//B)*B)
    return [Pos(x=top_left.x + x, y=top_left.y + y) for x in range(B) for y in range(B)]

class AllSolutionsCollector(CpSolverSolutionCallback):
    def __init__(self, board: 'Board', out: List[SingleSolution], max_solutions: Optional[int] = None, callback: Optional[Callable[[SingleSolution], None]] = None):
        super().__init__()
        self.out = out
        self.unique_solutions = set()
        self.max_solutions = max_solutions
        self.callback = callback
        self.vars_by_pos: Dict[Pos, cp_model.IntVar] = board.model_vars.copy()

    def on_solution_callback(self):
        try:
            assignment: Dict[Pos, int] = {}
            for pos, var in self.vars_by_pos.items():
                assignment[pos] = self.value(var)
            result = SingleSolution(assignment=assignment)
            result_json = get_hashable_solution(result)
            if result_json in self.unique_solutions:
                return
            self.unique_solutions.add(result_json)
            self.out.append(result)
            if self.callback is not None:
                self.callback(result)
            if self.max_solutions is not None and len(self.out) >= self.max_solutions:
                self.StopSearch()
        except Exception as e:
            print(e)
            raise e


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
            row_vars = [self.model_vars[get_pos(x=x, y=row)] for x in range(self.N)]
            self.model.AddAllDifferent(row_vars)
        # each column
        for col in range(self.N):
            col_vars = [self.model_vars[get_pos(x=col, y=y)] for y in range(self.N)]
            self.model.AddAllDifferent(col_vars)
        # each block
        for block_i in range(self.N):
            block_vars = [self.model_vars[p] for p in get_block_pos(block_i, self.B)]
            self.model.AddAllDifferent(block_vars)

    def solve_all(self, max_solutions: Optional[int] = None, callback: Optional[Callable[[SingleSolution], None]] = None) -> List[SingleSolution]:
        solver = cp_model.CpSolver()
        solver.parameters.enumerate_all_solutions = True
        solutions: List[SingleSolution] = []
        collector = AllSolutionsCollector(self, solutions, max_solutions=max_solutions, callback=callback)
        tic = time.time()
        solver.solve(self.model, collector)
        print("Solutions found:", len(solutions))
        print("status:", solver.StatusName())
        toc = time.time()
        print(f"Time taken: {toc - tic:.2f} seconds")
        return solutions

    def solve_and_print(self):
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.zeros_like(self.board)
            for pos in get_all_pos(self.N):
                c = get_value(self.board, pos)
                c = single_res.assignment[pos]
                set_value(res, pos, c)
            print(res)
        return self.solve_all(callback=callback)
