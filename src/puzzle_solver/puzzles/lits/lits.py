import json
import time
from dataclasses import dataclass
from typing import Optional, Union

from ortools.sat.python import cp_model
import numpy as np

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, set_char, get_pos, in_bounds, Direction, get_next_pos, polyominoes_with_shape_id
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution, force_connected_component


# a shape on the 2d board is just a set of positions
Shape = frozenset[Pos]


@dataclass(frozen=True)
class SingleSolution:
    assignment: dict[Pos, Union[str, int]]
    all_other_variables: dict

    def get_hashable_solution(self) -> str:
        result = []
        for pos, v in self.assignment.items():
            result.append((pos.x, pos.y, v))
        return json.dumps(result, sort_keys=True)



@dataclass
class ShapeOnBoard:
    is_active: cp_model.IntVar
    shape: Shape
    shape_id: int
    body: set[Pos]
    disallow_same_shape: set[Pos]


class Board:
    def __init__(self, board: np.array, polyomino_degrees: int = 4):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        self.V = board.shape[0]
        self.H = board.shape[1]
        assert all((str(c.item()).isdecimal() for c in np.nditer(board))), 'board must contain only digits'
        self.board = board
        self.polyomino_degrees = polyomino_degrees
        self.polyominoes = polyominoes_with_shape_id(self.polyomino_degrees)

        self.block_numbers = set([int(c.item()) for c in np.nditer(board)])
        self.blocks = {i: set() for i in self.block_numbers}
        for cell in get_all_pos(self.V, self.H):
            self.blocks[int(get_char(self.board, cell))].add(cell)

        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}
        self.connected_components: dict[Pos, cp_model.IntVar] = {}
        self.shapes_on_board: list[ShapeOnBoard] = []  # will contain every possible shape on the board based on polyomino degrees

        self.create_vars()
        self.init_shapes_on_board()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[pos] = self.model.NewBoolVar(f'{pos}')
        # print('base vars:', len(self.model_vars))

    def init_shapes_on_board(self):
        for idx, (shape, shape_id) in enumerate(self.polyominoes):
            for translate in get_all_pos(self.V, self.H):  # body of shape is translated to be at pos
                body = {get_pos(x=p.x + translate.x, y=p.y + translate.y) for p in shape}
                if any(not in_bounds(p, self.V, self.H) for p in body):
                    continue
                # shape must be fully contained in one block
                if len(set(get_char(self.board, p) for p in body)) > 1:
                    continue
                # 2 tetrominoes of matching types cannot touch each other horizontally or vertically. Rotations and reflections count as matching.
                disallow_same_shape = set(get_next_pos(p, direction) for p in body for direction in Direction)
                disallow_same_shape -= body
                self.shapes_on_board.append(ShapeOnBoard(
                    is_active=self.model.NewBoolVar(f'{idx}:{translate}:is_active'),
                    shape=shape,
                    shape_id=shape_id,
                    body=body,
                    disallow_same_shape=disallow_same_shape,
                ))
        # print('shapes on board:', len(self.shapes_on_board))

    def add_all_constraints(self):
        # RULES:
        # 1- You have to place one tetromino in each region in such a way that:
        # 2- 2 tetrominoes of matching types cannot touch each other horizontally or vertically. Rotations and reflections count as matching.
        # 3- The shaded cells should form a single connected area.
        # 4- 2x2 shaded areas are not allowed

        # each cell must be part of a shape, every shape must be fully on the board. Core constraint, otherwise shapes on the board make no sense.
        self.only_allow_shapes_on_board()

        self.force_one_shape_per_block()  # Rule #1
        self.disallow_same_shape_touching()  # Rule #2
        self.fc = force_connected_component(self.model, self.model_vars)  # Rule #3
        # print('force connected vars:', len(fc))
        shape_2_by_2 = frozenset({Pos(0, 0), Pos(0, 1), Pos(1, 0), Pos(1, 1)})
        self.disallow_shape(shape_2_by_2)  # Rule #4


    def only_allow_shapes_on_board(self):
        for shape_on_board in self.shapes_on_board:
            # if shape is active then all its body cells must be active
            self.model.Add(sum(self.model_vars[p] for p in shape_on_board.body) == len(shape_on_board.body)).OnlyEnforceIf(shape_on_board.is_active)
        # each cell must be part of a shape
        for p in get_all_pos(self.V, self.H):
            shapes_on_p = [s for s in self.shapes_on_board if p in s.body]
            self.model.Add(sum(s.is_active for s in shapes_on_p) == 1).OnlyEnforceIf(self.model_vars[p])

    def force_one_shape_per_block(self):
        # You have to place exactly one tetromino in each region
        for block_i in self.block_numbers:
            shapes_on_block = [s for s in self.shapes_on_board if s.body & self.blocks[block_i]]
            assert all(s.body.issubset(self.blocks[block_i]) for s in shapes_on_block), 'expected all shapes on block to be fully contained in the block'
            # print(f'shapes on block {block_i} has {len(shapes_on_block)} shapes')
            self.model.Add(sum(s.is_active for s in shapes_on_block) == 1)

    def disallow_same_shape_touching(self):
        # if shape is active then it must not touch any other shape of the same type
        for shape_on_board in self.shapes_on_board:
            similar_shapes = [s for s in self.shapes_on_board if s.shape_id == shape_on_board.shape_id]
            for s in similar_shapes:
                if shape_on_board.disallow_same_shape & s.body:  # this shape disallows having s be on the board
                    self.model.Add(s.is_active == 0).OnlyEnforceIf(shape_on_board.is_active)

    def disallow_shape(self, shape_to_disallow: Shape):
        # for every position in the board, force sum of body < len(body)
        for translate in get_all_pos(self.V, self.H):
            cur_body = {get_pos(x=p.x + translate.x, y=p.y + translate.y) for p in shape_to_disallow}
            if any(not in_bounds(p, self.V, self.H) for p in cur_body):
                continue
            self.model.Add(sum(self.model_vars[p] for p in cur_body) < len(cur_body))




    def solve_and_print(self, verbose: bool = True, max_solutions: Optional[int] = None, verbose_callback: Optional[bool] = None):
        if verbose_callback is None:
            verbose_callback = verbose
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, int] = {}
            for pos, var in board.model_vars.items():
                assignment[pos] = solver.Value(var)
            all_other_variables = {
                'fc': {k: solver.Value(v) for k, v in board.fc.items()}
            }
            return SingleSolution(assignment=assignment, all_other_variables=all_other_variables)
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.full((self.V, self.H), ' ', dtype=str)
            for pos, val in single_res.assignment.items():
                c = 'X' if val == 1 else ' '
                set_char(res, pos, c)
            print('[\n' + '\n'.join(['  ' + str(res[row].tolist()) + ',' for row in range(self.V)]) + '\n]')
            pass
        return generic_solve_all(self, board_to_solution, callback=callback if verbose_callback else None, verbose=verbose, max_solutions=max_solutions)
