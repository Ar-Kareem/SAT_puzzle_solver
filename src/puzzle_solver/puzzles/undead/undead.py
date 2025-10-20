from typing import Iterable, Optional
from enum import Enum
from dataclasses import dataclass

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Pos, get_all_pos, set_char, get_pos, get_next_pos, in_bounds, get_char, Direction
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution


class Monster(Enum):
    VAMPIRE = "VA"
    ZOMBIE = "ZO"
    GHOST = "GH"


@dataclass
class SingleBeamResult:
    position: Pos
    reflect_count: int


def get_all_monster_types() -> Iterable[tuple[str, str]]:
    for monster in Monster:
        yield monster, monster.value


def can_see(reflect_count: int, monster: Monster) -> bool:
    if monster == Monster.ZOMBIE:
        return True
    elif monster == Monster.VAMPIRE:
        return reflect_count == 0
    elif monster == Monster.GHOST:
        return reflect_count > 0
    else:
        raise ValueError


def beam(board, start_pos: Pos, direction: Direction) -> list[SingleBeamResult]:
    N = board.shape[0]
    cur_result: list[SingleBeamResult] = []
    reflect_count = 0
    cur_pos = start_pos
    while True:
        if not in_bounds(cur_pos, N):
            break
        cur_pos_char = get_char(board, cur_pos)
        if cur_pos_char == '//':
            direction = {
                Direction.RIGHT: Direction.UP,
                Direction.UP: Direction.RIGHT,
                Direction.DOWN: Direction.LEFT,
                Direction.LEFT: Direction.DOWN
            }[direction]
            reflect_count += 1
        elif cur_pos_char == '\\':
            direction = {
                Direction.RIGHT: Direction.DOWN,
                Direction.DOWN: Direction.RIGHT,
                Direction.UP: Direction.LEFT,
                Direction.LEFT: Direction.UP
            }[direction]
            reflect_count += 1
        else:
            # not a mirror
            cur_result.append(SingleBeamResult(cur_pos, reflect_count))
        cur_pos = get_next_pos(cur_pos, direction)
    return cur_result


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
        self.star_positions: set[Pos] = {pos for pos in get_all_pos(self.N) if get_char(self.board, pos) == '  '}
        self.monster_count = monster_count

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in self.star_positions:
            c = get_char(self.board, pos)
            assert c == '  ', f'star position {pos} has character {c}'
            monster_vars = []
            for _, monster_name in get_all_monster_types():
                v = self.model.NewBoolVar(f"{pos}_is_{monster_name}")
                self.model_vars[(pos, monster_name)] = v
                monster_vars.append(v)
            self.model.add_exactly_one(*monster_vars)

    def add_all_constraints(self):
        # top edge
        for i, ground in zip(range(self.N), self.sides['top']):
            if ground == -1:
                continue
            pos = get_pos(x=i, y=0)
            beam_result = beam(self.board, pos, Direction.DOWN)
            self.model.add(self.get_var(beam_result) == ground)

        # left edge
        for i, ground in zip(range(self.N), self.sides['left']):
            if ground == -1:
                continue
            pos = get_pos(x=0, y=i)
            beam_result = beam(self.board, pos, Direction.RIGHT)
            self.model.add(self.get_var(beam_result) == ground)

        # right edge
        for i, ground in zip(range(self.N), self.sides['right']):
            if ground == -1:
                continue
            pos = get_pos(x=self.N-1, y=i)
            beam_result = beam(self.board, pos, Direction.LEFT)
            self.model.add(self.get_var(beam_result) == ground)

        # bottom edge
        for i, ground in zip(range(self.N), self.sides['bottom']):
            if ground == -1:
                continue
            pos = get_pos(x=i, y=self.N-1)
            beam_result = beam(self.board, pos, Direction.UP)
            self.model.add(self.get_var(beam_result) == ground)
        
        if self.monster_count is not None:
            for monster, count in self.monster_count.items():
                if count == -1:
                    continue
                monster_name = monster.value
                monster_vars = [self.model_vars[(pos, monster_name)] for pos in self.star_positions]
                self.model.add(lxp.Sum(monster_vars) == count)

    def get_var(self, path: list[SingleBeamResult]) -> lxp:
        path_vars = []
        for square in path:
            assert square.position in self.star_positions, f'square {square.position} is not a star position'
            for monster, monster_name in get_all_monster_types():
                if can_see(square.reflect_count, monster):
                    path_vars.append(self.model_vars[(square.position, monster_name)])
        return lxp.Sum(path_vars) if path_vars else 0

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, str] = {}
            for (pos, monster_name), var in board.model_vars.items():
                if solver.BooleanValue(var):
                    assignment[pos] = monster_name
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.full((self.N, self.N), ' ', dtype=object)
            for pos in get_all_pos(self.N):
                c = get_char(self.board, pos)
                if c == '  ':
                    c = single_res.assignment[pos]
                set_char(res, pos, c)
            print(res)
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
