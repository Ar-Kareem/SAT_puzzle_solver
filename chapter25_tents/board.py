
import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Literal, Optional, Callable
from dataclasses import dataclass
from collections import defaultdict
from enum import Enum

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp
from ortools.sat.python.cp_model import CpSolverSolutionCallback

sys.path.append(str(Path(__file__).parent.parent))
from core.utils import Pos, get_all_pos, get_char, set_char, in_bounds, get_next_pos, Direction, get_pos



@dataclass(frozen=True)
class SingleSolution:
    assignment: dict[Pos, int]


def get_hashable_solution(solution: SingleSolution) -> str:
    result = []
    for pos, v in solution.assignment.items():
        result.append((pos.x, pos.y, v > 0))  # we don't care which assignment of tent-tree, we only care if there is a tent or not to determine uniqueness
    return json.dumps(result, sort_keys=True)


def neighbours(board: np.array, pos: Pos) -> list[Pos]:
    N = board.shape[0]
    result = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if (dx, dy) == (0, 0):
                continue
            d_pos = Pos(x=pos.x+dx, y=pos.y+dy)
            if in_bounds(d_pos, N) and get_char(board, d_pos) == '*':
                result.append(d_pos)
    return result

@dataclass(frozen=True)
class ModelVars:
    is_tent: dict[Pos, cp_model.IntVar]
    tent_direction: dict[Pos, cp_model.IntVar]


class AllSolutionsCollector(CpSolverSolutionCallback):
    def __init__(self, board: 'Board', out: List[SingleSolution], max_solutions: Optional[int] = None, callback: Optional[Callable[[SingleSolution], None]] = None):
        super().__init__()
        self.out = out
        self.unique_solutions = set()
        self.max_solutions = max_solutions
        self.callback = callback
        self.model_vars: ModelVars = board.model_vars

    def on_solution_callback(self):
        try:
            assignment: Dict[Pos, int] = {}
            for pos, var in self.model_vars.is_tent.items():
                if isinstance(var, int):
                    continue
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
    def __init__(self, board: np.array, sides: dict[str, np.array]):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert board.shape[0] == board.shape[1], 'board must be square'
        assert len(sides) == 2, '2 sides must be provided'
        assert set(sides.keys()) == set(['top', 'side'])
        assert all(s.ndim == 1 and s.shape[0] == board.shape[0] for s in sides.values()), 'all sides must be equal to board size'
        assert all(c.item() in ['*', 'T'] for c in np.nditer(board)), 'board must contain only * or T'
        self.board = board
        self.N = board.shape[0]
        self.star_positions: set[Pos] = {pos for pos in get_all_pos(self.N) if get_char(self.board, pos) == '*'}
        self.tree_positions: set[Pos] = {pos for pos in get_all_pos(self.N) if get_char(self.board, pos) == 'T'}
        self.model = cp_model.CpModel()
        self.model_vars: ModelVars = ModelVars(is_tent=defaultdict(int), tent_direction=defaultdict(int))
        self.sides = sides
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in self.star_positions:
            is_tent = self.model.NewBoolVar(f'{pos}:is_tent')
            tent_direction = self.model.NewIntVar(0, 4, f'{pos}:tent_direction')
            self.model.Add(tent_direction == 0).OnlyEnforceIf(is_tent.Not())
            self.model.Add(tent_direction > 0).OnlyEnforceIf(is_tent)
            self.model_vars.is_tent[pos] = is_tent
            self.model_vars.tent_direction[pos] = tent_direction

    def add_all_constraints(self):
        # - There are exactly as many tents as trees.
        self.model.Add(lxp.sum([self.model_vars.is_tent[pos] for pos in self.star_positions]) == len(self.tree_positions))
        # - no two tents are adjacent horizontally, vertically or diagonally
        for pos in self.star_positions:
            for neighbour in neighbours(self.board, pos):
                self.model.Add(self.model_vars.is_tent[neighbour] == 0).OnlyEnforceIf(self.model_vars.is_tent[pos])
        # - the number of tents in each row and column matches the numbers around the edge of the grid 
        for row in range(self.N):
            row_vars = [self.model_vars.is_tent[get_pos(x=i, y=row)] for i in range(self.N)]
            self.model.Add(lxp.sum(row_vars) == self.sides['side'][row])
        for col in range(self.N):
            col_vars = [self.model_vars.is_tent[get_pos(x=col, y=i)] for i in range(self.N)]
            self.model.Add(lxp.sum(col_vars) == self.sides['top'][col])
        # - it is possible to match tents to trees so that each tree is orthogonally adjacent to its own tent (but may also be adjacent to other tents). 
        # for each tree, one of the following must be true:
        # a tent on its left has direction RIGHT
        # a tent on its right has direction LEFT
        # a tent on its top has direction DOWN
        # a tent on its bottom has direction UP
        for tree in self.tree_positions:
            self.add_tree_constraints(tree)

    def add_tree_constraints(self, tree_pos: Pos):
        left_pos = get_next_pos(tree_pos, Direction.LEFT)
        right_pos = get_next_pos(tree_pos, Direction.RIGHT)
        top_pos = get_next_pos(tree_pos, Direction.UP)
        bottom_pos = get_next_pos(tree_pos, Direction.DOWN)
        var_list = []
        if left_pos in self.star_positions:
            aux = self.model.NewBoolVar(f'{tree_pos}:left')
            self.model.Add(self.model_vars.tent_direction[left_pos] == Direction.RIGHT.value).OnlyEnforceIf(aux)
            self.model.Add(self.model_vars.tent_direction[left_pos] != Direction.RIGHT.value).OnlyEnforceIf(aux.Not())
            var_list.append(aux)
        if right_pos in self.star_positions:
            aux = self.model.NewBoolVar(f'{tree_pos}:right')
            self.model.Add(self.model_vars.tent_direction[right_pos] == Direction.LEFT.value).OnlyEnforceIf(aux)
            self.model.Add(self.model_vars.tent_direction[right_pos] != Direction.LEFT.value).OnlyEnforceIf(aux.Not())
            var_list.append(aux)
        if top_pos in self.star_positions:
            aux = self.model.NewBoolVar(f'{tree_pos}:top')
            self.model.Add(self.model_vars.tent_direction[top_pos] == Direction.DOWN.value).OnlyEnforceIf(aux)
            self.model.Add(self.model_vars.tent_direction[top_pos] != Direction.DOWN.value).OnlyEnforceIf(aux.Not())
            var_list.append(aux)
        if bottom_pos in self.star_positions:
            aux = self.model.NewBoolVar(f'{tree_pos}:bottom')
            self.model.Add(self.model_vars.tent_direction[bottom_pos] == Direction.UP.value).OnlyEnforceIf(aux)
            self.model.Add(self.model_vars.tent_direction[bottom_pos] != Direction.UP.value).OnlyEnforceIf(aux.Not())
            var_list.append(aux)
        self.model.AddBoolOr(var_list)

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
                c = get_char(self.board, pos)
                if c == '*':
                    c = single_res.assignment[pos]
                    c = 'E' if c == 1 else ' '
                set_char(res, pos, c)
            print(res)
        return self.solve_all(callback=callback)
