import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp
from ortools.sat.python.cp_model import CpSolverSolutionCallback

sys.path.append(str(Path(__file__).parent.parent))
from core.utils import Pos, get_all_pos, set_char, get_pos, get_char


@dataclass(frozen=True)
class SingleSolution:
    assignment: dict[Pos, int]


def get_hashable_solution(solution: SingleSolution) -> str:
    result = []
    for pos, v in solution.assignment.items():
        result.append((pos.x, pos.y, v))
    return json.dumps(result, sort_keys=True)


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
                assignment[pos] = self.Value(var)
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
        assert board.shape[0] % 2 == 0, 'board must have even number of rows'
        assert board.shape[1] % 2 == 0, 'board must have even number of columns'
        self.board = board
        self.V = board.shape[0]
        self.H = board.shape[1]
        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[pos] = self.model.NewBoolVar(f'{pos}')

    def add_all_constraints(self):
        # some cells are already filled
        for pos in get_all_pos(self.V, self.H):
            c = get_char(self.board, pos)
            if c == '*':
                continue
            v = 1 if c == 'B' else 0
            self.model.Add(self.model_vars[pos] == v)
        # no three consecutive squares, horizontally or vertically, are the same colour 
        for col in range(self.H):
            for i in range(self.V - 2):
                var_list = [self.model_vars[get_pos(x=col, y=j)] for j in range(i, i+3)]
                self.model.Add(lxp.Sum(var_list) != 0)
                self.model.Add(lxp.Sum(var_list) != 3)
        for row in range(self.V):
            for i in range(self.H - 2):
                var_list = [self.model_vars[get_pos(x=j, y=row)] for j in range(i, i+3)]
                self.model.Add(lxp.Sum(var_list) != 0)
                self.model.Add(lxp.Sum(var_list) != 3)
        # each row and column contains the same number of black and white squares.
        for col in range(self.H):
            var_list = [self.model_vars[get_pos(x=col, y=row)] for row in range(self.V)]
            self.model.Add(lxp.Sum(var_list) == self.V // 2)
        for row in range(self.V):
            var_list = [self.model_vars[get_pos(x=col, y=row)] for col in range(self.H)]
            self.model.Add(lxp.Sum(var_list) == self.H // 2)

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
            for pos in get_all_pos(self.V, self.H):
                c = get_char(self.board, pos)
                if c == '*':
                    c = 'B' if single_res.assignment[pos] == 1 else 'W'
                set_char(res, pos, c)
            print(res)
        return self.solve_all(callback=callback)
