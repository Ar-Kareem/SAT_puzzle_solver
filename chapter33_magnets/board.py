
import json
from typing import Dict, List, Tuple, Optional, Literal, Optional, Callable
from dataclasses import dataclass
from enum import Enum

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp
from ortools.sat.python.cp_model import CpSolverSolutionCallback

Direction = Literal['right', 'left', 'down', 'up']


@dataclass(frozen=True)
class Pos:
    x: int
    y: int


class State(Enum):
    BLANK = ('BLANK', 'B')
    POSITIVE = ('POSITIVE', 'P')
    NEGATIVE = ('NEGATIVE', 'N')


@dataclass(frozen=True)
class SingleSolution:
    assignment: dict[Pos, str]


def get_deltas(direction: Direction) -> Tuple[int, int]:
    if direction == 'right':
        return +1, 0
    elif direction == 'left':
        return -1, 0
    elif direction == 'down':
        return 0, +1
    elif direction == 'up':
        return 0, -1
    else:
        raise ValueError


def get_pos(x: int, y: int) -> Pos:
    return Pos(x=x, y=y)


def get_next_pos(cur_pos: Pos, direction: Direction) -> Pos:
    delta_x, delta_y = get_deltas(direction)
    return Pos(cur_pos.x+delta_x, cur_pos.y+delta_y)


def get_hashable_solution(solution: SingleSolution) -> str:
    result = []
    for pos, state in solution.assignment.items():
        result.append((pos.x, pos.y, state.value[0]))
    return json.dumps(result, sort_keys=True)


def get_all_pos(V, H):
    for y in range(V):
        for x in range(H):
            yield get_pos(x=x, y=y)


def get_char(board: np.array, pos: Pos) -> str:
    c = board[pos.y][pos.x]
    assert c in ['H', 'V']
    return c


def set_char(board: np.array, pos: Pos, char: str):
    board[pos.y][pos.x] = char


def in_bounds(pos: Pos, H: int, V: int) -> bool:
    return 0 <= pos.y < V and 0 <= pos.x < H


class AllSolutionsCollector(CpSolverSolutionCallback):
    def __init__(self, model_vars, out: List[SingleSolution], max_solutions: Optional[int] = None, callback: Optional[Callable[[SingleSolution], None]] = None):
        super().__init__()
        self.out = out
        self.unique_solutions = set()
        self.max_solutions = max_solutions
        self.callback = callback
        self.name_to_state: Dict[str, State] = {m.value[0]: m for m in State}
        self.vars_by_pos: Dict[Pos, List[tuple[str, cp_model.IntVar]]] = {}
        for (pos, state), var in model_vars.items():
            self.vars_by_pos.setdefault(pos, []).append((state, var))

    def on_solution_callback(self):
        try:
            assignment: Dict[Pos, str] = {}
            for pos, candidates in self.vars_by_pos.items():
                for state, var in candidates:  # exactly one is true per star cell
                    if self.BooleanValue(var):
                        assignment[pos] = state
                        break
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
        assert len(sides) == 4, '4 sides must be provided'
        assert all(s.ndim == 1 for s in sides.values()), 'all sides must be 1d'
        assert set(sides.keys()) == set(['pos_v', 'neg_v', 'pos_h', 'neg_h'])
        assert sides['pos_h'].shape[0] == board.shape[0], 'pos_h dim must equal vertical board size'
        assert sides['neg_h'].shape[0] == board.shape[0], 'neg_h dim must equal vertical board size'
        assert sides['pos_v'].shape[0] == board.shape[1], 'pos_v dim must equal horizontal board size'
        assert sides['neg_v'].shape[0] == board.shape[1], 'neg_v dim must equal horizontal board size'
        self.board = board
        self.sides = sides
        self.V = board.shape[0]
        self.H = board.shape[1]
        self.model = cp_model.CpModel()
        self.pairs: set[tuple[Pos, Pos]] = set()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        # init vars
        for pos in get_all_pos(V=self.V, H=self.H):
            var_list = []
            for state in State:
                v = self.model.NewBoolVar(f'{pos}:{state.value[0]}')
                self.model_vars[(pos, state)] = v
                var_list.append(v)
            self.model.AddExactlyOne(var_list)
        # init pairs. traverse from top left and V indicates vertical domino (2x1) while H is horizontal (1x2)
        seen_pos = set()
        for pos in get_all_pos(V=self.V, H=self.H):
            if pos in seen_pos:
                continue
            seen_pos.add(pos)
            c = get_char(self.board, pos)
            direction = {'V': 'down', 'H': 'right'}[c]
            other_pos = get_next_pos(pos, direction)
            seen_pos.add(other_pos)
            self.pairs.add((pos, other_pos))
        assert len(self.pairs)*2 == self.V*self.H

    def add_all_constraints(self):
        # pairs must be matching
        for pair in self.pairs:
            a, b = pair
            self.model.add(self.model_vars[(a, State.BLANK)] == self.model_vars[(b, State.BLANK)])
            self.model.add(self.model_vars[(a, State.POSITIVE)] == self.model_vars[(b, State.NEGATIVE)])
            self.model.add(self.model_vars[(a, State.NEGATIVE)] == self.model_vars[(b, State.POSITIVE)])
        # no orthoginal matching poles
        for x in range(self.H):
            for y in range(self.V):
                pos = get_pos(x=x, y=y)
                right_pos = get_pos(x=x+1, y=y)
                down_pos = get_pos(x=x, y=y+1)
                if in_bounds(right_pos, H=self.H, V=self.V):
                    self.model.add(self.model_vars[(pos, State.POSITIVE)] == 0).OnlyEnforceIf(self.model_vars[(right_pos, State.POSITIVE)])
                    self.model.add(self.model_vars[(right_pos, State.POSITIVE)] == 0).OnlyEnforceIf(self.model_vars[(pos, State.POSITIVE)])
                    self.model.add(self.model_vars[(pos, State.NEGATIVE)] == 0).OnlyEnforceIf(self.model_vars[(right_pos, State.NEGATIVE)])
                    self.model.add(self.model_vars[(right_pos, State.NEGATIVE)] == 0).OnlyEnforceIf(self.model_vars[(pos, State.NEGATIVE)])
                if in_bounds(down_pos, H=self.H, V=self.V):
                    self.model.add(self.model_vars[(pos, State.POSITIVE)] == 0).OnlyEnforceIf(self.model_vars[(down_pos, State.POSITIVE)])
                    self.model.add(self.model_vars[(down_pos, State.POSITIVE)] == 0).OnlyEnforceIf(self.model_vars[(pos, State.POSITIVE)])
                    self.model.add(self.model_vars[(pos, State.NEGATIVE)] == 0).OnlyEnforceIf(self.model_vars[(down_pos, State.NEGATIVE)])
                    self.model.add(self.model_vars[(down_pos, State.NEGATIVE)] == 0).OnlyEnforceIf(self.model_vars[(pos, State.NEGATIVE)])

        # sides counts must equal actual count
        for row_i in range(self.V):
            sum_pos = lxp.sum([self.model_vars[(get_pos(x=i, y=row_i), State.POSITIVE)] for i in range(self.H)])
            sum_neg = lxp.sum([self.model_vars[(get_pos(x=i, y=row_i), State.NEGATIVE)] for i in range(self.H)])
            ground_pos = self.sides['pos_h'][row_i]
            ground_neg = self.sides['neg_h'][row_i]
            if ground_pos != -1:
                self.model.Add(sum_pos == ground_pos)
            if ground_neg != -1:
                self.model.Add(sum_neg == ground_neg)
        for col_i in range(self.H):
            sum_pos = lxp.sum([self.model_vars[(get_pos(x=col_i, y=i), State.POSITIVE)] for i in range(self.V)])
            sum_neg = lxp.sum([self.model_vars[(get_pos(x=col_i, y=i), State.NEGATIVE)] for i in range(self.V)])
            ground_pos = self.sides['pos_v'][col_i]
            ground_neg = self.sides['neg_v'][col_i]
            if ground_pos != -1:
                self.model.Add(sum_pos == ground_pos)
            if ground_neg != -1:
                self.model.Add(sum_neg == ground_neg)

        


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
            for pos in get_all_pos(V=self.V, H=self.H):
                c = get_char(self.board, pos)
                c = single_res.assignment[pos].value[1]
                set_char(res, pos, c)
            print(res)
        return self.solve_all(callback=callback, max_solutions=999)
