from dataclasses import dataclass

import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_neighbors4, get_pos, in_bounds, set_char, get_char, polyominoes, Shape, Direction, get_next_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution, force_connected_component
from puzzle_solver.core.utils_visualizer import render_shaded_grid


@dataclass
class ShapeOnBoard:
    is_active: cp_model.IntVar
    N: int
    body: set[Pos]
    force_water: set[Pos]


class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all((c.item() == ' ') or str(c.item()).isdecimal() or c.item() == '#' for c in np.nditer(board)), 'board must contain only space, #, or digits'
        self.board = board
        self.V, self.H = board.shape
        self.illegal_positions: set[Pos] = {pos for pos in get_all_pos(self.V, self.H) if get_char(self.board, pos) == '#'}

        unique_numbers: set[int] = {int(c) for c in np.nditer(board) if str(c).isdecimal()}
        self.polyominoes: dict[int, set[Shape]] = {n: polyominoes(n) for n in unique_numbers}
        self.hints = {pos: int(get_char(self.board, pos)) for pos in get_all_pos(self.V, self.H) if str(get_char(self.board, pos)).isdecimal()}
        self.all_hint_pos: set[Pos] = set(self.hints.keys())

        self.model = cp_model.CpModel()
        self.W: dict[Pos, cp_model.IntVar] = {}
        self.B: dict[Pos, cp_model.IntVar] = {}
        self.shapes_on_board: list[ShapeOnBoard] = []

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in self.get_all_legal_pos():
            self.W[pos] = self.model.NewBoolVar(f'W:{pos}')
            self.B[pos] = self.model.NewBoolVar(f'B:{pos}')
            self.model.AddExactlyOne([self.W[pos], self.B[pos]])

    def get_all_legal_pos(self) -> set[Pos]:
        return {pos for pos in get_all_pos(self.V, self.H) if pos not in self.illegal_positions}

    def in_bounds_and_legal(self, pos: Pos) -> bool:
        return in_bounds(pos, self.V, self.H) and pos not in self.illegal_positions

    def add_all_constraints(self):
        for pos in self.W.keys():
            self.model.AddExactlyOne([self.W[pos], self.B[pos]])

        # init shapes on board for each hint
        for hint_pos, hint_value in self.hints.items():
            hint_shapes = []
            for shape in self.polyominoes[hint_value]:
                hint_single_shape = self.init_shape_on_board(shape, hint_pos, hint_value)  # a "single shape" is translated many times
                hint_shapes.extend(hint_single_shape)
            assert len(hint_shapes) > 0, f'no shapes found for hint {hint_pos} with value {hint_value}'
            self.model.AddExactlyOne([s.is_active for s in hint_shapes])
            self.shapes_on_board.extend(hint_shapes)

        # if no shape is active on the spot then it must be black
        for pos in self.get_all_legal_pos():
            shapes_here = [s for s in self.shapes_on_board if pos in s.body]
            self.model.AddExactlyOne([s.is_active for s in shapes_here] + [self.B[pos]])

        # if a shape is active, then all its body must be white and force water must be black
        for shape_on_board in self.shapes_on_board:
            for pos in shape_on_board.body:
                self.model.Add(self.W[pos] == 1).OnlyEnforceIf(shape_on_board.is_active)
            for pos in shape_on_board.force_water:
                self.model.Add(self.B[pos] == 1).OnlyEnforceIf(shape_on_board.is_active)

        # disallow 2x2 blacks
        for pos in get_all_pos(self.V, self.H):
            tl = pos
            tr = get_next_pos(pos, Direction.RIGHT)
            bl = get_next_pos(pos, Direction.DOWN)
            br = get_next_pos(bl, Direction.RIGHT)
            if any(not in_bounds(p, self.V, self.H) for p in [tl, tr, bl, br]):
                continue
            self.model.AddBoolOr([self.B[tl].Not(), self.B[tr].Not(), self.B[bl].Not(), self.B[br].Not()])

        # all black is single connected component
        force_connected_component(self.model, self.B)

    def init_shape_on_board(self, shape: Shape, hint_pos: Pos, hint_value: int):
        other_hint_pos: set[Pos] = self.all_hint_pos - {hint_pos}
        max_x = max(p.x for p in shape)
        max_y = max(p.y for p in shape)
        hint_shapes = []
        for dx in range(0, max_x + 1):
            for dy in range(0, max_y + 1):
                body = {get_pos(x=p.x + hint_pos.x - dx, y=p.y + hint_pos.y - dy) for p in shape}  # translate shape by fixed hint position then dynamic moving dx and dy
                if hint_pos not in body:  # the hint must still be in the body after translation
                    continue
                if any(not self.in_bounds_and_legal(p) for p in body):  # illegal shape
                    continue
                water = set(p for pos in body for p in get_neighbors4(pos, self.V, self.H))
                water -= body
                water -= self.illegal_positions
                if any(p in other_hint_pos for p in body) or any(w in other_hint_pos for w in water):  # shape touches another hint or forces water on another hint, illegal
                    continue
                shape_on_board = ShapeOnBoard(
                    is_active=self.model.NewBoolVar(f'{hint_pos}:{dx}:{dy}:is_active'),
                    N=hint_value,
                    body=body,
                    force_water=water,
                )
                hint_shapes.append(shape_on_board)
        return hint_shapes

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, int] = {}
            for pos, var in board.B.items():
                assignment[pos] = solver.Value(var)
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(render_shaded_grid(self.V, self.H, lambda r, c: single_res.assignment[get_pos(x=c, y=r)] == 1, empty_text=lambda r, c: str(self.board[r, c])))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
