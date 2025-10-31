from dataclasses import dataclass
from collections import defaultdict

import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_pos, in_bounds, get_next_pos, Direction, polyominoes
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function, id_board_to_wall_fn


Shape = frozenset[Pos]  # a shape on the 2d board is just a set of positions

@dataclass(frozen=True)
class ShapeOnBoard:
    is_active: cp_model.IntVar
    shape: Shape
    shape_id: int
    body: set[Pos]


def get_valid_translations(shape: Shape, board: np.array) -> set[Pos]:
    # give a shape and a board, return all valid translations of the shape that are fully contained in the board AND consistent with the clues on the board
    shape_list = list(shape)
    shape_borders = []  # will contain the number of borders for each pos in the shape; this has to be consistent with the clues on the board
    for pos in shape_list:
        v = 0
        for direction in Direction:
            next_pos = get_next_pos(pos, direction)
            if not in_bounds(next_pos, board.shape[0], board.shape[1]) or next_pos not in shape:
                v += 1
        shape_borders.append(v)
    shape_list = [(p.x, p.y) for p in shape_list]
    # min x/y is always 0
    max_x = max(p[0] for p in shape_list)
    max_y = max(p[1] for p in shape_list)
    for dy in range(0, board.shape[0] - max_y):
        for dx in range(0, board.shape[1] - max_x):
            body = tuple((p[0] + dx, p[1] + dy) for p in shape_list)
            for i, p in enumerate(body):
                c = board[p[1], p[0]]
                if c != ' ' and c != str(shape_borders[i]):  # there is a clue and it doesn't match my translated shape, skip
                    break
            else:
                yield frozenset(get_pos(x=p[0], y=p[1]) for p in body)


class Board:
    def __init__(self, board: np.array, region_size: int):
        assert region_size >= 1 and isinstance(region_size, int), 'region_size must be an integer greater than or equal to 1'
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all((c.item() == ' ') or str(c.item()).isdecimal() for c in np.nditer(board)), 'board must contain only space or digits'
        self.board = board
        self.V, self.H = board.shape
        self.region_size = region_size
        self.region_count = (self.V * self.H) // self.region_size
        assert self.region_count * self.region_size == self.V * self.H, f'region_size must be a factor of the board size, got {self.region_size} and {self.region_count}'
        self.polyominoes = polyominoes(self.region_size)

        self.model = cp_model.CpModel()
        self.shapes_on_board: list[ShapeOnBoard] = []  # will contain every possible shape on the board based on polyomino degrees
        self.pos_to_shapes: dict[Pos, set[ShapeOnBoard]] = defaultdict(set)
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for shape in self.polyominoes:
            for body in get_valid_translations(shape, self.board):
                uid = len(self.shapes_on_board)
                shape_on_board = ShapeOnBoard(
                    is_active=self.model.NewBoolVar(f'{uid}:is_active'),
                    shape=shape, shape_id=uid, body=body
                )
                self.shapes_on_board.append(shape_on_board)
                for pos in body:
                    self.pos_to_shapes[pos].add(shape_on_board)

    def add_all_constraints(self):
        for pos in get_all_pos(self.V, self.H):  # each position has exactly one shape active
            self.model.AddExactlyOne(shape.is_active for shape in self.pos_to_shapes[pos])

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            active_shapes = [shape for shape in board.shapes_on_board if solver.Value(shape.is_active) == 1]
            return SingleSolution(assignment={pos: shape.shape_id for shape in active_shapes for pos in shape.body})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H,
                cell_flags=id_board_to_wall_fn(np.array([[single_res.assignment[get_pos(x=c, y=r)] for c in range(self.H)] for r in range(self.V)])),
                center_char=lambda r, c: self.board[r, c] if self.board[r, c] != ' ' else '·'))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
