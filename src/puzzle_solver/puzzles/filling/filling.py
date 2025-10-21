from dataclasses import dataclass

import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, Shape, get_all_pos, get_char, set_char, polyominoes, in_bounds, get_next_pos, Direction
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution, and_constraint


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
        # len_shapes = sum(len(shapes) for shapes in self.polyominoes.values())
        # print(f'total number of shapes: {len_shapes}')

        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}
        self.digit_to_shapes = {d: [] for d in self.digits}
        self.body_loc_to_shape = {(d,p): [] for d in self.digits for p in get_all_pos(self.V, self.H)}
        self.forced_pos: dict[Pos, int] = {}

        self.create_vars()
        self.constrain_numbers_on_board()
        self.init_polyominoes_on_board()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            for d in self.digits:
                self.model_vars[(d,pos)] = self.model.NewBoolVar(f'{d}:{pos}')

    def constrain_numbers_on_board(self):
        # force numbers already on the board
        for pos in get_all_pos(self.V, self.H):
            c = get_char(self.board, pos)
            if c.isdecimal():
                self.model.Add(self.model_vars[(int(c),pos)] == 1)
                self.forced_pos[pos] = int(c)

    def init_polyominoes_on_board(self):
        # total_count = 0
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
        #             total_count += 1
        #             if total_count % 1000 == 0:
        #                 print(f'{total_count} shapes on board')
        # print(f'total number of shapes on board: {total_count}')

    def add_all_constraints(self):
        for pos in get_all_pos(self.V, self.H):
            # exactly one digit is active at every position
            self.model.AddExactlyOne(self.model_vars[(d,pos)] for d in self.digits)
            # exactly one shape is active at that position
            self.model.AddExactlyOne(s.is_active for d in self.digits for s in self.body_loc_to_shape[(d,pos)])
        # if a shape is active then all its body is active
        
        for s_list in self.body_loc_to_shape.values():
            for s in s_list:
                for p in s.body:
                    self.model.Add(self.model_vars[(s.N,p)] == 1).OnlyEnforceIf(s.is_active)

        # same shape cannot touch
        for d, s_list in self.digit_to_shapes.items():
            for s in s_list:
                for disallow_pos in s.disallow_same_shape:
                    self.model.Add(self.model_vars[(d,disallow_pos)] == 0).OnlyEnforceIf(s.is_active)

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: "Board", solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, int] = {}
            for pos in get_all_pos(self.V, self.H):
                for d in self.digits:
                    if solver.Value(self.model_vars[(d,pos)]) == 1:
                        assignment[pos] = d
                        break
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.full((self.V, self.H), ' ', dtype=object)
            for pos in get_all_pos(self.V, self.H):
                c = get_char(self.board, pos)
                c = single_res.assignment[pos]
                set_char(res, pos, c)
            print(res)
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
