from typing import Optional

import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, set_char, Direction, get_opposite_direction, get_next_pos, in_bounds, get_row_pos, get_col_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution

def get_direction(pos: Pos, board: np.array) -> Optional[Direction]:
    if get_char(board, pos) == 'R':
        return Direction.RIGHT
    elif get_char(board, pos) == 'D':
        return Direction.DOWN
    elif get_char(board, pos) == 'U':
        return Direction.UP
    elif get_char(board, pos) == 'L':
        return Direction.LEFT
    return None

def move_backward(pos: Pos, board: np.array) -> Pos:
    for direction in Direction:
        opposite_direction = get_opposite_direction(direction)
        neighbor = get_next_pos(pos, direction)
        if in_bounds(neighbor, board.shape[0], board.shape[1]) and get_direction(neighbor, board) == opposite_direction:  # the neighbor is pointing to me
            return neighbor
    return None

class Board:
    def __init__(self, board: np.array, top: np.array, side: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        self.V = board.shape[0]
        self.H = board.shape[1]
        assert top.ndim == 1 and top.shape[0] == self.H, 'top must be a 1d array of length board width'
        assert side.ndim == 1 and side.shape[0] == self.V, 'side must be a 1d array of length board height'
        assert all((c in ['R', 'D', 'U', 'X', 'L']) for c in np.nditer(board)), 'board must contain only valid characters: R, D, U, X, L'
        self.board = board
        self.top = top
        self.side = side
        self.tip: set[Pos] = {pos for pos in get_all_pos(self.V, self.H) if get_char(self.board, pos) == 'X'}

        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[pos] = self.model.NewBoolVar(f'{pos}')
    
    def add_all_constraints(self):
        visited: set[Pos] = set()
        for cur_pos in self.tip:
            visited.add(cur_pos)
            while cur_pos is not None:
                backward_pos = move_backward(cur_pos, self.board)
                if backward_pos is None:
                    break
                self.model.Add(self.model_vars[backward_pos] == 1).OnlyEnforceIf(self.model_vars[cur_pos])
                cur_pos = backward_pos
                visited.add(cur_pos)
        assert len(visited) == self.V * self.H, f'all positions must be visited, got {len(visited)}. missing {set(get_all_pos(self.V, self.H)) - visited}'
        for row in range(self.V):
            self.model.Add(sum([self.model_vars[pos] for pos in get_row_pos(row, self.H)]) == self.side[row])
        for col in range(self.H):
            self.model.Add(sum([self.model_vars[pos] for pos in get_col_pos(col, self.V)]) == self.top[col])

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, int] = {}
            for pos, var in board.model_vars.items():
                assignment[pos] = solver.value(var)
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.full((self.V, self.H), ' ', dtype=object)
            for pos in get_all_pos(self.V, self.H):
                c = get_char(self.board, pos)
                c = 'X' if single_res.assignment[pos] == 1 else ' '
                set_char(res, pos, c)
            print(res)
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
