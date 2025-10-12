
import multiprocessing
import json
from typing import Dict, List, Tuple, Iterable, Optional, Literal, Optional, Callable
from enum import Enum
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


class Monster(Enum):
    VAMPIRE = ("VA", "vampire")
    ZOMBIE = ("ZO", "zombie")
    GHOST = ("GH", "ghost")


@dataclass
class SingleBeamResult:
    position: Pos
    reflect_count: int


@dataclass(frozen=True)
class SingleSolution:
    assignment: dict[Pos, Monster]


def get_all_monster_types() -> Iterable[tuple[str, str]]:
    for monster in Monster:
        yield monster, monster.value[1]


def can_see(reflect_count: int, monster: Monster) -> bool:
    if monster == Monster.ZOMBIE:
        return True
    elif monster == Monster.VAMPIRE:
        return reflect_count == 0
    elif monster == Monster.GHOST:
        return reflect_count > 0
    else:
        raise ValueError


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
    return Pos(x, y)


def get_next_pos(cur_pos: Pos, direction: Direction) -> Pos:
    delta_x, delta_y = get_deltas(direction)
    return Pos(cur_pos.x+delta_x, cur_pos.y+delta_y)


def get_hashable_solution(solution: SingleSolution) -> str:
    result = []
    for pos, monster in solution.assignment.items():
        result.append((pos.x, pos.y, monster.value[0]))
    return json.dumps(result, sort_keys=True)


def get_all_pos(N):
    for y in range(N):
        for x in range(N):
            yield get_pos(x, y)


def get_char(board: np.array, pos: Pos) -> str:
    c = board[pos.y][pos.x]
    assert c in ['//', '\\', '**']
    return c

def set_char(board: np.array, pos: Pos, char: str):
    board[pos.y][pos.x] = char


def in_bounds(pos: Pos, N: int) -> bool:
    return 0 <= pos.y < N and 0 <= pos.x < N


def beam(board, start_pos: Pos, direction: Direction) -> list[SingleBeamResult]:
    N = board.shape[0]
    cur_result: list[SingleBeamResult] = []
    reflect_count = 0
    cur_pos = start_pos
    while True:
        cur_pos = get_next_pos(cur_pos, direction)
        if not in_bounds(cur_pos, N):
            break
        cur_pos_char = get_char(board, cur_pos)
        if cur_pos_char == '//':
            direction = {
                'right': 'up',
                'up': 'right',
                'down': 'left',
                'left': 'down'
            }[direction]
            reflect_count += 1
        elif cur_pos_char == '\\':
            direction = {
                'right': 'down',
                'down': 'right',
                'up': 'left',
                'left': 'up'
            }[direction]
            reflect_count += 1
        else:
            # not a mirror
            cur_result.append(SingleBeamResult(cur_pos, reflect_count))
    return cur_result


class AllSolutionsCollector(CpSolverSolutionCallback):
    def __init__(self, model_vars, out: List[SingleSolution], max_solutions: Optional[int] = None, callback: Optional[Callable[[SingleSolution], None]] = None):
        super().__init__()
        self.out = out
        self.unique_solutions = set()
        self.max_solutions = max_solutions
        self.callback = callback
        # Precompute a name->Monster map and group vars by cell for fast lookup
        self.name_to_monster: Dict[str, Monster] = {m.value[1]: m for m in Monster}
        self.vars_by_pos: Dict[Pos, List[tuple[str, cp_model.IntVar]]] = {}
        for (pos, monster_name), var in model_vars.items():
            self.vars_by_pos.setdefault(pos, []).append((monster_name, var))

    def on_solution_callback(self):
        try:
            assignment: Dict[Pos, Monster] = {}
            for pos, candidates in self.vars_by_pos.items():
                for monster_name, var in candidates:  # exactly one is true per star cell
                    if self.BooleanValue(var):
                        assignment[pos] = self.name_to_monster[monster_name]
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
    def __init__(self, board: np.array, sides: dict[str, np.array], monster_count: Optional[dict[Monster, int]] = None):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert board.shape[0] == board.shape[1], 'board must be square'
        assert len(sides) == 4, '4 sides must be provided'
        assert all(s.ndim == 1 and s.shape[0] == board.shape[0] for s in sides.values()), 'all sides must be equal to board size'
        assert set(sides.keys()) == set(['right', 'left', 'top', 'bottom'])
        self.board = board
        self.sides = sides
        self.N = board.shape[0]
        self.model = cp_model.CpModel()
        self.model_vars: dict[tuple[Pos, str], cp_model.IntVar] = {}
        self.star_positions: set[Pos] = {pos for pos in get_all_pos(self.N) if get_char(self.board, pos) == '**'}
        self.monster_count = monster_count

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in self.star_positions:
            c = get_char(self.board, pos)
            assert c == '**', f'star position {pos} has character {c}'
            monster_vars = []
            for _, monster_name in get_all_monster_types():
                v = self.model.NewBoolVar(f"{pos}_is_{monster_name}")
                self.model_vars[(pos, monster_name)] = v
                monster_vars.append(v)
            self.model.add_exactly_one(*monster_vars)

    def add_all_constraints(self):
        # top edge
        for i, ground in zip(range(self.N), self.sides['top']):
            pos = get_pos(x=i, y=-1)
            beam_result = beam(self.board, pos, 'down')
            self.model.add(self.get_var(beam_result) == ground)

        # left edge
        for i, ground in zip(range(self.N), self.sides['left']):
            pos = get_pos(x=-1, y=i)
            beam_result = beam(self.board, pos, 'right')
            self.model.add(self.get_var(beam_result) == ground)

        # right edge
        for i, ground in zip(range(self.N), self.sides['right']):
            pos = get_pos(x=self.N, y=i)
            beam_result = beam(self.board, pos, 'left')
            self.model.add(self.get_var(beam_result) == ground)

        # bottom edge
        for i, ground in zip(range(self.N), self.sides['bottom']):
            pos = get_pos(x=i, y=self.N)
            beam_result = beam(self.board, pos, 'up')
            self.model.add(self.get_var(beam_result) == ground)
        
        if self.monster_count is not None:
            for monster, limit in self.monster_count.items():
                monster_name = monster.value[1]
                monster_vars = [self.model_vars[(pos, monster_name)] for pos in self.star_positions]
                self.model.add(lxp.Sum(monster_vars) == limit)

    def get_var(self, path: list[SingleBeamResult]) -> lxp:
        path_vars = []
        for square in path:
            assert square.position in self.star_positions, f'square {square.position} is not a star position'
            for monster, monster_name in get_all_monster_types():
                if can_see(square.reflect_count, monster):
                    path_vars.append(self.model_vars[(square.position, monster_name)])
        return lxp.Sum(path_vars) if path_vars else 0

    def solve_all(self, max_solutions: Optional[int] = None, callback: Optional[Callable[[SingleSolution], None]] = None) -> List[SingleSolution]:
        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = multiprocessing.cpu_count()
        solutions: List[SingleSolution] = []
        collector = AllSolutionsCollector(self.model_vars, solutions, max_solutions=max_solutions, callback=callback)
        solver.Solve(self.model, collector)
        print("Solutions found:", len(solutions))
        print("status:", solver.StatusName())
        return solutions

    def solve_and_print(self):
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.zeros_like(self.board)
            for pos in get_all_pos(self.N):
                c = get_char(self.board, pos)
                if c == '**':
                    c = single_res.assignment[pos].value[0]
                set_char(res, pos, c)
            print(res)
        return self.solve_all(callback=callback)
