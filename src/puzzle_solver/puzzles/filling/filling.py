from dataclasses import dataclass

import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, get_pos, polyominoes, in_bounds, get_next_pos, Direction
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function, id_board_to_wall_fn


@dataclass
class ShapeOnBoard:
    is_active: cp_model.IntVar
    N: int
    body: set[Pos]
    disallow_same_shape: set[Pos]


class Board:
    def __init__(self, board: np.ndarray, digits = (1, 2, 3, 4, 5, 6, 7, 8, 9)):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        self.board = board
        self.V, self.H = board.shape
        assert all((c == ' ') or (str(c).isdecimal() and 0 <= int(c) <= 9) for c in np.nditer(board)), "board must contain space or digits 0..9"
        self.digits = digits
        self.polyominoes = {d: polyominoes(d) for d in self.digits}

        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}
        self.digit_to_shapes = {d: [] for d in self.digits}
        self.body_loc_to_shape = {(d,p): [] for d in self.digits for p in get_all_pos(self.V, self.H)}
        self.forced_pos: dict[Pos, int] = {}

        self.create_vars()
        self.force_hints()
        self.init_polyominoes_on_board()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            for d in self.digits:
                self.model_vars[(d,pos)] = self.model.NewBoolVar(f'{d}:{pos}')

    def force_hints(self):
        for pos in get_all_pos(self.V, self.H):
            c = get_char(self.board, pos)
            if c.isdecimal():
                self.model.Add(self.model_vars[(int(c),pos)] == 1)
                self.forced_pos[pos] = int(c)

    def init_polyominoes_on_board(self):
        for d in self.digits:  # all digits
            digit_count = 0
            for pos in get_all_pos(self.V, self.H):  # translate by shape
                for shape in self.polyominoes[d]:  # all shapes of d digits
                    body = {pos + p for p in shape}
                    if any(not in_bounds(p, self.V, self.H) for p in body):
                        continue
                    if any(p in self.forced_pos and self.forced_pos[p] != d for p in body):  # part of this shape's body is already forced to a different digit, skip
                        continue
                    disallow_same_shape = set(get_next_pos(p, direction) for p in body for direction in Direction)
                    disallow_same_shape = {p for p in disallow_same_shape if p not in body and in_bounds(p, self.V, self.H)}
                    shape_on_board = ShapeOnBoard(
                        is_active=self.model.NewBoolVar(f'd{d}:{digit_count}:{pos}:is_active'),
                        N=d,
                        body=body,
                        disallow_same_shape=disallow_same_shape,
                    )
                    self.digit_to_shapes[d].append(shape_on_board)
                    for p in body:
                        self.body_loc_to_shape[(d,p)].append(shape_on_board)
                    digit_count += 1

    def add_all_constraints(self):
        for pos in get_all_pos(self.V, self.H):
            self.model.AddExactlyOne(self.model_vars[(d,pos)] for d in self.digits)  # exactly one digit is active at every position
            self.model.AddExactlyOne(s.is_active for d in self.digits for s in self.body_loc_to_shape[(d,pos)])  # exactly one shape is active at that position
        for s_list in self.body_loc_to_shape.values():  # if a shape is active then all its body is active
            for s in s_list:
                for p in s.body:
                    self.model.Add(self.model_vars[(s.N,p)] == 1).OnlyEnforceIf(s.is_active)
        for d, s_list in self.digit_to_shapes.items():  # same shape cannot touch each other
            for s in s_list:
                for disallow_pos in s.disallow_same_shape:
                    self.model.Add(self.model_vars[(d,disallow_pos)] == 0).OnlyEnforceIf(s.is_active)

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: "Board", solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: d for pos in get_all_pos(self.V, self.H) for d in self.digits if solver.Value(self.model_vars[(d,pos)]) == 1})
        def callback(single_res: SingleSolution):
            print("Solution found")
            res_arr = np.array([[single_res.assignment[get_pos(x=c, y=r)] for c in range(self.H)] for r in range(self.V)])
            print(combined_function(self.V, self.H, cell_flags=id_board_to_wall_fn(res_arr), center_char=lambda r, c: res_arr[r, c]))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
