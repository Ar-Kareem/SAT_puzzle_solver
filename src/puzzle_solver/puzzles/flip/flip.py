from typing import Any, Optional

import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_neighbors4, get_char, Direction, get_next_pos, get_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


def _to_pos(pos: Pos, s: str) -> Pos:
    d = {'L': Direction.LEFT, 'R': Direction.RIGHT, 'U': Direction.UP, 'D': Direction.DOWN}[s[0]]
    r = get_next_pos(pos, d)
    if len(s) == 1:
        return r
    else:
        return _to_pos(r, s[1:])


class Board:
    def __init__(self, board: np.array, random_mapping: Optional[dict[Pos, Any]] = None):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all((c.item() in ['B', 'W']) for c in np.nditer(board)), 'board must contain only B or W'
        self.board = board
        self.V, self.H = board.shape
        if random_mapping is None:
            self.tap_mapping: dict[Pos, set[Pos]] = {pos: list(get_neighbors4(pos, self.V, self.H, include_self=True)) for pos in get_all_pos(self.V, self.H)}
        else:
            mapping_value = list(random_mapping.values())[0]
            if isinstance(mapping_value, (set, list, tuple)) and isinstance(list(mapping_value)[0], Pos):
                self.tap_mapping: dict[Pos, set[Pos]] = {pos: set(random_mapping[pos]) for pos in get_all_pos(self.V, self.H)}
            elif isinstance(mapping_value, (set, list, tuple)) and isinstance(list(mapping_value)[0], str):  # strings like "L", "UR", etc.
                self.tap_mapping: dict[Pos, set[Pos]] = {pos: set(_to_pos(pos, s) for s in random_mapping[pos]) for pos in get_all_pos(self.V, self.H)}
            else:
                raise ValueError(f'invalid random_mapping: {random_mapping}')
            for k, v in self.tap_mapping.items():
                if k not in v:
                    v.add(k)

        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[pos] = self.model.NewBoolVar(f'tap:{pos}')

    def add_all_constraints(self):
        for pos in get_all_pos(self.V, self.H):
            # the state of a position is its starting state + if it is tapped + if any pos pointing to it is tapped
            pos_that_will_turn_me = [k for k,v in self.tap_mapping.items() if pos in v]
            literals = [self.model_vars[p] for p in pos_that_will_turn_me]
            if get_char(self.board, pos) == 'W':  # if started as white then needs an even number of taps while xor checks for odd number
                literals.append(self.model.NewConstant(True))
            self.model.AddBoolXOr(literals)

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: solver.Value(var) for pos, var in board.model_vars.items()})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H, is_shaded=lambda r, c: single_res.assignment[get_pos(x=c, y=r)] == 1))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
