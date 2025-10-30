from collections import defaultdict

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Direction, Pos, get_all_pos, get_char, get_neighbors8, get_next_pos, get_row_pos, get_col_pos, get_opposite_direction, get_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


class Board:
    def __init__(self, board: np.array, side: np.array, top: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert side.ndim == 1 and side.shape[0] == board.shape[0], 'side must be 1d and equal to board size'
        assert top.ndim == 1 and top.shape[0] == board.shape[1], 'top must be 1d and equal to board size'
        assert all(c.item() in [' ', 'T'] for c in np.nditer(board)), 'board must contain only space or T'
        self.board = board
        self.V, self.H = board.shape
        self.side = side
        self.top = top
        self.non_tree_positions: set[Pos] = {pos for pos in get_all_pos(self.V, self.H) if get_char(self.board, pos) == ' '}
        self.tree_positions: set[Pos] = {pos for pos in get_all_pos(self.V, self.H) if get_char(self.board, pos) == 'T'}

        self.model = cp_model.CpModel()
        self.is_tent: dict[Pos, cp_model.IntVar] = defaultdict(int)
        self.tent_direction: dict[tuple[Pos, Direction], cp_model.IntVar] = defaultdict(int)
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in self.non_tree_positions:
            self.is_tent[pos] = self.model.NewBoolVar(f'{pos}:is_tent')
        for pos in self.tree_positions:
            for direction in Direction:
                tent_pos = get_next_pos(pos, direction)
                if tent_pos not in self.is_tent:
                    continue
                opposite_direction = get_opposite_direction(direction)
                tent_direction = self.model.NewBoolVar(f'{pos}:{direction}')
                self.model.Add(tent_direction == 0).OnlyEnforceIf(self.is_tent[tent_pos].Not())
                self.tent_direction[(pos, direction)] = tent_direction
                self.tent_direction[(tent_pos, opposite_direction)] = tent_direction

    def add_all_constraints(self):
        # - There are exactly as many tents as trees.
        self.model.Add(lxp.sum([self.is_tent[pos] for pos in self.non_tree_positions]) == len(self.tree_positions))
        # - no two tents are adjacent horizontally, vertically or diagonally
        for pos in self.non_tree_positions:
            for neighbour in get_neighbors8(pos, V=self.V, H=self.H, include_self=False):
                self.model.Add(self.is_tent[neighbour] == 0).OnlyEnforceIf(self.is_tent[pos])
        # - the number of tents in each row and column matches the numbers around the edge of the grid
        for row in range(self.V):
            if self.side[row] == -1:
                continue
            row_vars = [self.is_tent[pos] for pos in get_row_pos(row, H=self.H)]
            self.model.Add(lxp.sum(row_vars) == self.side[row])
        for col in range(self.H):
            if self.top[col] == -1:
                continue
            col_vars = [self.is_tent[pos] for pos in get_col_pos(col, V=self.V)]
            self.model.Add(lxp.sum(col_vars) == self.top[col])
        # - it is possible to match tents to trees so that each tree is orthogonally adjacent to its own tent (but may also be adjacent to other tents).
        # each tent is pointing exactly once at a tree
        for pos in self.non_tree_positions:
            var_list = [self.tent_direction[(pos, direction)] for direction in Direction]
            self.model.Add(lxp.sum(var_list) == 1).OnlyEnforceIf(self.is_tent[pos])
            self.model.Add(lxp.sum(var_list) == 0).OnlyEnforceIf(self.is_tent[pos].Not())
        # each tree is pointed at by exactly one tent
        for pos in self.tree_positions:
            var_list = [self.tent_direction[(pos, direction)] for direction in Direction]
            self.model.Add(lxp.sum(var_list) == 1)

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: solver.value(var) for pos, var in board.is_tent.items() if not isinstance(var, int)})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H, center_char=lambda r, c: ('|' if self.board[r][c].strip() else ('▲' if single_res.assignment[get_pos(c, r)] == 1 else ' '))))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose, max_solutions=5)
