from dataclasses import dataclass

import numpy as np

from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, in_bounds, set_char, get_char, Direction, get_next_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import render_grid


def factor_pairs(N: int, upper_limit_i: int, upper_limit_j: int):
    """Return all unique pairs (a, b) such that a * b == N, with a, b <= upper_limit."""
    if N <= 0 or upper_limit_i <= 0 or upper_limit_j <= 0:
        return []

    pairs = []
    i = 1
    while i * i <= N:
        if N % i == 0:
            j = N // i
            if i <= upper_limit_i and j <= upper_limit_j:
                pairs.append((i, j))
            if i != j and j <= upper_limit_i and i <= upper_limit_j:
                pairs.append((j, i))
        i += 1
    return pairs


@dataclass
class Rectangle:
    active: cp_model.IntVar
    N: int
    clue_id: int
    width: int
    height: int
    body: set[Pos]


class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all((c.item() == ' ') or str(c.item()).isdecimal() for c in np.nditer(board)), 'board must contain only space or digits'
        self.board = board
        self.V, self.H = board.shape
        self.clue_pos: list[Pos] = [pos for pos in get_all_pos(self.V, self.H) if str(get_char(self.board, pos)).isdecimal()]
        self.clue_pos_to_id: dict[Pos, int] = {pos: i for i, pos in enumerate(self.clue_pos)}
        self.clue_pos_to_value: dict[Pos, int] = {pos: int(get_char(self.board, pos)) for pos in self.clue_pos}

        self.model = cp_model.CpModel()
        self.model_vars: dict[tuple[Pos, Pos], cp_model.IntVar] = {}
        self.rectangles: list[Rectangle] = []

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        self.init_rectangles()
        # for each position it belongs to exactly 1 clue
        # instead of iterating over all clues, we only look at the clues that are possible for this position (by looking at the rectangles that contain this position)
        for pos in get_all_pos(self.V, self.H):
            possible_clue_here = {rectangle.clue_id for rectangle in self.rectangles if pos in rectangle.body}  # get the clue position for any rectangle that contains this position
            for possible_clue in possible_clue_here:
                self.model_vars[(pos, possible_clue)] = self.model.NewBoolVar(f'{pos}:{possible_clue}')

    def init_rectangles(self) -> list[Rectangle]:
        self.fixed_pos: set[Pos] = set(self.clue_pos)
        for pos in self.clue_pos:  # for each clue on the board
            clue_id = self.clue_pos_to_id[pos]
            clue_num = self.clue_pos_to_value[pos]
            other_fixed_pos = self.fixed_pos - {pos}
            for width, height in factor_pairs(clue_num, self.V, self.H):  # for each possible width x height rectangle that can fit the clue
                # if the digit is at pos and we have a width x height rectangle then we can translate the rectangle "0 to width" to the left and "0 to height" to the top
                for dx in range(width):
                    for dy in range(height):
                        body = {Pos(x=pos.x - dx + i, y=pos.y - dy + j) for i in range(width) for j in range(height)}
                        if any(not in_bounds(p, self.V, self.H) for p in body):  # a rectangle cannot be out of bounds
                            continue
                        if any(p in other_fixed_pos for p in body):  # a rectangle cannot contain a different clue; each clue is 1 rectangle only
                            continue
                        rectangle = Rectangle(active=self.model.NewBoolVar(f'{clue_id}'), N=clue_num, clue_id=clue_id, width=width, height=height, body=body)
                        self.rectangles.append(rectangle)

    def add_all_constraints(self):
        # each pos has only 1 rectangle active
        for pos in get_all_pos(self.V, self.H):
            self.model.AddExactlyOne(rectangle.active for rectangle in self.rectangles if pos in rectangle.body)
        # each pos has only 1 clue active
        for pos in get_all_pos(self.V, self.H):
            self.model.AddExactlyOne(self.model_vars[(pos, clue_id)] for clue_id in self.clue_pos_to_id.values() if (pos, clue_id) in self.model_vars)
        # a rectangle being active means all its body ponts to the clue
        for rectangle in self.rectangles:
            is_active = rectangle.active
            for pos in rectangle.body:
                self.model.Add(self.model_vars[(pos, rectangle.clue_id)] == 1).OnlyEnforceIf(is_active)

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, int] = {}
            for rectangle in self.rectangles:
                if solver.Value(rectangle.active) == 1:
                    for pos in rectangle.body:
                        assignment[pos] = f'id{rectangle.clue_id}:N={rectangle.N}:{rectangle.height}x{rectangle.width}'
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.full((self.V, self.H), '', dtype=object)
            id_board = np.full((self.V, self.H), '', dtype=object)
            for pos in get_all_pos(self.V, self.H):
                cur = single_res.assignment[pos]
                set_char(id_board, pos, cur)
                left_pos = get_next_pos(pos, Direction.LEFT)
                right_pos = get_next_pos(pos, Direction.RIGHT)
                top_pos = get_next_pos(pos, Direction.UP)
                bottom_pos = get_next_pos(pos, Direction.DOWN)
                if left_pos not in single_res.assignment or single_res.assignment[left_pos] != cur:
                    set_char(res, pos, get_char(res, pos) + 'L')
                if right_pos not in single_res.assignment or single_res.assignment[right_pos] != cur:
                    set_char(res, pos, get_char(res, pos) + 'R')
                if top_pos not in single_res.assignment or single_res.assignment[top_pos] != cur:
                    set_char(res, pos, get_char(res, pos) + 'U')
                if bottom_pos not in single_res.assignment or single_res.assignment[bottom_pos] != cur:
                    set_char(res, pos, get_char(res, pos) + 'D')
            print(render_grid(res, center_char=lambda r, c: self.board[r, c] if self.board[r, c] != ' ' else ' '))

        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
