
import json
from typing import Dict, List, Tuple, Optional, Literal, Optional, Callable
from dataclasses import dataclass

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp
from ortools.sat.python.cp_model import CpSolverSolutionCallback


Direction = Literal['right', 'left', 'down', 'up']


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

def bool_from_greater_than(model, a, b, name):
    res = model.NewBoolVar(name)
    model.add(a > b).OnlyEnforceIf(res)
    model.add(a <= b).OnlyEnforceIf(res.Not())
    return res


class Board:
    def __init__(self, board: np.array, sides: dict[str, np.array]):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert board.shape[0] == board.shape[1], 'board must be square'
        assert len(sides) == 4, '4 sides must be provided'
        assert all(s.ndim == 1 and s.shape[0] == board.shape[0] for s in sides.values()), 'all sides must be equal to board size'
        assert set(sides.keys()) == set(['right', 'left', 'top', 'bottom'])
        self.board = board
        self.sides = sides
        self.N = board.shape[0]
        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.N):
            self.model_vars[pos] = self.model.NewIntVar(1, self.N, f'{pos}')

    def add_all_constraints(self):
        # if board has value then force intvar to be that value
        for pos in get_all_pos(self.N):
            v = get_char(self.board, pos)
            if str(v).isdecimal():
                self.model.Add(self.model_vars[pos] == int(v))
        # all different for rows
        for row_i in range(self.N):
            row_vars = [self.model_vars[get_pos(x=i, y=row_i)] for i in range(self.N)]
            self.model.AddAllDifferent(row_vars)
        # all different for cols
        for col_i in range(self.N):
            col_vars = [self.model_vars[get_pos(x=col_i, y=i)] for i in range(self.N)]
            self.model.AddAllDifferent(col_vars)
        # constrain number of viewable towers
        # top
        for x in range(self.N):
            real = self.sides['top'][x]
            if real == -1:
                continue
            can_see_variables = []
            previous_towers: list[cp_model.IntVar] = []
            for y in range(self.N):
                current_tower = self.model_vars[get_pos(x=x, y=y)]
                can_see_variables.append(self.can_see_tower(previous_towers, current_tower, f'top:{x}:{y}'))
                previous_towers.append(current_tower)
            self.model.add(lxp.sum(can_see_variables) == real)
        # bottom
        for x in range(self.N):
            real = self.sides['bottom'][x]
            if real == -1:
                continue
            can_see_variables = []
            previous_towers: list[cp_model.IntVar] = []
            for y in range(self.N-1, -1, -1):
                current_tower = self.model_vars[get_pos(x=x, y=y)]
                can_see_variables.append(self.can_see_tower(previous_towers, current_tower, f'bottom:{x}:{y}'))
                previous_towers.append(current_tower)
            self.model.add(lxp.sum(can_see_variables) == real)
        # left
        for y in range(self.N):
            real = self.sides['left'][y]
            if real == -1:
                continue
            can_see_variables = []
            previous_towers: list[cp_model.IntVar] = []
            for x in range(self.N):
                current_tower = self.model_vars[get_pos(x=x, y=y)]
                can_see_variables.append(self.can_see_tower(previous_towers, current_tower, f'left:{x}:{y}'))
                previous_towers.append(current_tower)
            self.model.add(lxp.sum(can_see_variables) == real)
        # right
        for y in range(self.N):
            real = self.sides['right'][y]
            if real == -1:
                continue
            can_see_variables = []
            previous_towers: list[cp_model.IntVar] = []
            for x in range(self.N-1, -1, -1):
                current_tower = self.model_vars[get_pos(x=x, y=y)]
                can_see_variables.append(self.can_see_tower(previous_towers, current_tower, f'right:{x}:{y}'))
                previous_towers.append(current_tower)
            self.model.add(lxp.sum(can_see_variables) == real)

    def can_see_tower(self, blocks: list[cp_model.IntVar], tower: cp_model.IntVar, name: str):
        if len(blocks) == 0:
            return self.model.NewConstant(True)
        # I can see "tower" if it's larger that all the blocks
        # lits is a list of [(tower > b0), (tower > b1), ..., (tower > bi)]
        lits = [bool_from_greater_than(self.model, tower, block, f'{name}:lits:{i}') for i, block in enumerate(blocks)]

        # create a single bool which decides if I can see it or not
        res = self.model.NewBoolVar(name)
        self.model.AddBoolAnd(lits).OnlyEnforceIf(res)
        self.model.AddBoolOr([res] + [l.Not() for l in lits])
        return res

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
                c = single_res.assignment[pos]
                set_char(res, pos, c)
            print(res)
        return self.solve_all(callback=callback)
