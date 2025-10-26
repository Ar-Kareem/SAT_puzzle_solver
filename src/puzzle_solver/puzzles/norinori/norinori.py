from dataclasses import dataclass

import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, Shape, get_all_pos, get_char, set_char, in_bounds, get_next_pos, Direction
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution


@dataclass
class ShapeOnBoard:
    is_active: cp_model.IntVar
    orientation: str
    body: set[Pos]
    disallow: set[Pos]


class Board:
    def __init__(self, board: np.ndarray):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        self.board = board
        self.V, self.H = board.shape
        assert all((c == ' ') or str(c).isdecimal() for c in np.nditer(board)), "board must contain space or digits"
        self.block_numbers = set([int(c.item()) for c in np.nditer(board)])
        self.blocks = {i: [pos for pos in get_all_pos(self.V, self.H) if int(get_char(self.board, pos)) == i] for i in self.block_numbers}

        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}
        self.shapes_on_board: list[ShapeOnBoard] = []

        self.create_vars()
        self.init_shapes_on_board()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[pos] = self.model.NewBoolVar(f'{pos}')

    def init_shapes_on_board(self):
        for pos in get_all_pos(self.V, self.H):
            shape = self.get_shape(pos, 'horizontal')
            if shape is not None:
                self.shapes_on_board.append(shape)
            shape = self.get_shape(pos, 'vertical')
            if shape is not None:
                self.shapes_on_board.append(shape)

    def add_all_constraints(self):
        # if a piece is active then all its body is active and the disallow is inactive
        for shape in self.shapes_on_board:
            for pos in shape.body:
                self.model.Add(self.model_vars[pos] == 1).OnlyEnforceIf(shape.is_active)
            for pos in shape.disallow:
                self.model.Add(self.model_vars[pos] == 0).OnlyEnforceIf(shape.is_active)
        # if a spot is active then exactly one piece (with a body there) is active
        for pos in get_all_pos(self.V, self.H):
            pieces_on_pos = [shape for shape in self.shapes_on_board if pos in shape.body]
            # if pos is on then exactly one shape is active. if pos is off then 0 shapes are active.
            self.model.Add(sum(shape.is_active for shape in pieces_on_pos) == self.model_vars[pos])
        # every region must have exactly 2 spots active.
        for block in self.blocks.values():
            self.model.Add(sum(self.model_vars[pos] for pos in block) == 2)

    def get_shape(self, pos: Pos, orientation: str) -> Shape:
        assert orientation in ['horizontal', 'vertical'], 'orientation must be horizontal or vertical'
        if orientation == 'horizontal':
            body = {pos, get_next_pos(pos, Direction.RIGHT)}
        else:
            body = {pos, get_next_pos(pos, Direction.DOWN)}
        if any(not in_bounds(p, self.V, self.H) for p in body):
            return None
        disallow = set(get_next_pos(p, direction) for p in body for direction in Direction)
        disallow = {p for p in disallow if p not in body and in_bounds(p, self.V, self.H)}
        shape_on_board = ShapeOnBoard(
            is_active=self.model.NewBoolVar(f'horizontal:{pos}'),
            orientation='horizontal',
            body=body,
            disallow=disallow,
        )
        return shape_on_board


    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: "Board", solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, int] = {}
            for pos in get_all_pos(self.V, self.H):
                if solver.Value(self.model_vars[pos]) == 1:
                    assignment[pos] = get_char(self.board, pos)
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.full((self.V, self.H), ' ', dtype=object)
            for pos in get_all_pos(self.V, self.H):
                c = get_char(self.board, pos)
                c = 'X' if pos in single_res.assignment else ' '
                set_char(res, pos, c)
            print('[')
            for row in res:
                print("    [ '" + "', '".join(row.tolist()) + "' ],")
            print(']')
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
