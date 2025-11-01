from collections import defaultdict
from typing import Optional

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, get_pos, get_row_pos, get_col_pos, Direction8, in_bounds, get_next_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


def get_ray(pos: Pos, direction: Direction8, V: int, H: int) -> list[Pos]:
    out = []
    while True:
        out.append(pos)
        pos = get_next_pos(pos, direction)
        if not in_bounds(pos, V, H):
            break
    return out


class Board:
    def __init__(self, board: np.array, id_to_count: Optional[dict[int, int]] = None):
        """
        board is a 2d array of location ids
        id_to_count is a dict of int to int, where the key is the id of the location and the value is the count of the queens on that location
        """
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all(str(c.item()).isdecimal() for c in np.nditer(board)), 'board must contain only digits'
        assert id_to_count is None or (isinstance(id_to_count, dict) and all(isinstance(k, int) and isinstance(v, int) for k, v in id_to_count.items())), 'id_to_count must be a dict of int to int'
        self.board = board
        self.V, self.H = board.shape
        self.location_ids = set([int(c.item()) for c in np.nditer(board)])
        self.location_ids_to_pos: dict[int, set[Pos]] = defaultdict(set)
        for pos in get_all_pos(self.V, self.H):
            self.location_ids_to_pos[int(get_char(self.board, pos))].add(pos)
        self.id_to_count = id_to_count
        if self.id_to_count is None:
            self.id_to_count = {id_: 1 for id_ in self.location_ids}

        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[pos] = self.model.NewBoolVar(f'{pos}')

    def add_all_constraints(self):
        # every row has at most one queen
        for row in range(self.V):
            self.model.Add(lxp.Sum([self.model_vars[pos] for pos in get_row_pos(row, self.H)]) <= 1)
        # every column has at most one queen
        for col in range(self.H):
            self.model.Add(lxp.Sum([self.model_vars[pos] for pos in get_col_pos(col, self.V)]) <= 1)
        # every diagonal has at most one queen
        for pos in get_col_pos(0, self.V):  # down-right diagonal on left border
            ray = get_ray(pos, Direction8.DOWN_RIGHT, self.V, self.H)
            self.model.Add(lxp.Sum([self.model_vars[pos] for pos in ray]) <= 1)
        for pos in get_row_pos(0, self.H):  # down-right diagonal on top border
            ray = get_ray(pos, Direction8.DOWN_RIGHT, self.V, self.H)
            self.model.Add(lxp.Sum([self.model_vars[pos] for pos in ray]) <= 1)
        for pos in get_row_pos(0, self.H):  # down-left diagonal on top
            ray = get_ray(pos, Direction8.DOWN_LEFT, self.V, self.H)
            self.model.Add(lxp.Sum([self.model_vars[pos] for pos in ray]) <= 1)
        for pos in get_col_pos(self.H - 1, self.V):  # down-left diagonal on right border
            ray = get_ray(pos, Direction8.DOWN_LEFT, self.V, self.H)
            self.model.Add(lxp.Sum([self.model_vars[pos] for pos in ray]) <= 1)
        # every id has at most count queens
        for id_ in self.location_ids:
            self.model.Add(lxp.Sum([self.model_vars[pos] for pos in self.location_ids_to_pos[id_]]) == self.id_to_count[id_])

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: solver.Value(var) for pos, var in board.model_vars.items()})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H, is_shaded=lambda r, c: single_res.assignment[get_pos(x=c, y=r)] == 1))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
