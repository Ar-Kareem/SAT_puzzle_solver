
import json
from typing import Dict, List, Tuple, Optional, Literal, Optional, Callable
from dataclasses import dataclass

import numpy as np
from numpy.core.defchararray import isdecimal
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp
from ortools.sat.python.cp_model import CpSolverSolutionCallback


@dataclass(frozen=True)
class Pos:
    x: int
    y: int


@dataclass(frozen=True)
class SingleSolution:
    assignment: dict[Pos, int]


def get_pos(x: int, y: int) -> Pos:
    return Pos(x=x, y=y)


def get_hashable_solution(solution: SingleSolution) -> str:
    result = []
    for pos, v in solution.assignment.items():
        result.append((pos.x, pos.y, v))
    return json.dumps(result, sort_keys=True)


def get_all_pos(N):
    for y in range(N):
        for x in range(N):
            yield get_pos(x=x, y=y)


def get_char(board: np.array, pos: Pos) -> str:
    c = board[pos.y][pos.x]
    assert (c == '*') or str(c).isdecimal()
    return c


def set_char(board: np.array, pos: Pos, char: str):
    board[pos.y][pos.x] = char


def in_bounds(pos: Pos, N: int) -> bool:
    return 0 <= pos.y < N and 0 <= pos.x < N


def neighbours(board: np.array, pos: Pos) -> list[Pos]:
    N = board.shape[0]
    result = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            d_pos = Pos(x=pos.x+dx, y=pos.y+dy)
            if in_bounds(d_pos, N):
                result.append(d_pos)
    return result


class AllSolutionsCollector(CpSolverSolutionCallback):
    def __init__(self, model_vars, out: List[SingleSolution], max_solutions: Optional[int] = None, callback: Optional[Callable[[SingleSolution], None]] = None):
        super().__init__()
        self.out = out
        self.unique_solutions = set()
        self.max_solutions = max_solutions
        self.callback = callback
        self.vars_by_pos: Dict[Pos, cp_model.IntVar] = model_vars.copy()

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
        self.board = board
        self.N = board.shape[0]
        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.N):
            self.model_vars[pos] = self.model.NewBoolVar(f'{pos}')

    def add_all_constraints(self):
        for pos in get_all_pos(self.N):
            c = get_char(self.board, pos)
            if not str(c).isdecimal():
                continue
            neighbour_vars = [self.model_vars[p] for p in neighbours(self.board, pos)]
            self.model.Add(lxp.sum(neighbour_vars) == int(c))


    def solve_all(self, max_solutions: Optional[int] = None, callback: Optional[Callable[[SingleSolution], None]] = None) -> List[SingleSolution]:
        solver = cp_model.CpSolver()
        solver.parameters.enumerate_all_solutions = True
        solutions: List[SingleSolution] = []
        collector = AllSolutionsCollector(self.model_vars, solutions, max_solutions=max_solutions, callback=callback)
        solver.solve(self.model, collector)
        print("Solutions found:", len(solutions))
        print("status:", solver.StatusName())
        return solutions

    def solve_and_print(self):
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.zeros_like(self.board)
            for pos in get_all_pos(self.N):
                c = get_char(self.board, pos)
                c = 'B' if single_res.assignment[pos] == 1 else ' '
                set_char(res, pos, c)
            print(res)
        return self.solve_all(callback=callback)
