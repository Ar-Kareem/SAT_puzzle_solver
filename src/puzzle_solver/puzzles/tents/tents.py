from collections import defaultdict

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, set_char, get_neighbors8, get_next_pos, Direction, get_row_pos, get_col_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution


class Board:
    def __init__(self, board: np.array, sides: dict[str, np.array]):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert board.shape[0] == board.shape[1], 'board must be square'
        assert len(sides) == 2, '2 sides must be provided'
        assert set(sides.keys()) == set(['top', 'side'])
        assert all(s.ndim == 1 and s.shape[0] == board.shape[0] for s in sides.values()), 'all sides must be equal to board size'
        assert all(c.item() in [' ', 'T'] for c in np.nditer(board)), 'board must contain only space or T'
        self.board = board
        self.N = board.shape[0]
        self.star_positions: set[Pos] = {pos for pos in get_all_pos(self.N) if get_char(self.board, pos) == ' '}
        self.tree_positions: set[Pos] = {pos for pos in get_all_pos(self.N) if get_char(self.board, pos) == 'T'}
        self.model = cp_model.CpModel()
        self.is_tent = defaultdict(int)
        self.tent_direction = defaultdict(int)
        self.sides = sides
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in self.star_positions:
            is_tent = self.model.NewBoolVar(f'{pos}:is_tent')
            tent_direction = self.model.NewIntVar(0, 4, f'{pos}:tent_direction')
            self.model.Add(tent_direction == 0).OnlyEnforceIf(is_tent.Not())
            self.model.Add(tent_direction > 0).OnlyEnforceIf(is_tent)
            self.is_tent[pos] = is_tent
            self.tent_direction[pos] = tent_direction

    def add_all_constraints(self):
        # - There are exactly as many tents as trees.
        self.model.Add(lxp.sum([self.is_tent[pos] for pos in self.star_positions]) == len(self.tree_positions))
        # - no two tents are adjacent horizontally, vertically or diagonally
        for pos in self.star_positions:
            for neighbour in get_neighbors8(pos, V=self.N, H=self.N, include_self=False):
                if get_char(self.board, neighbour) != ' ':
                    continue
                self.model.Add(self.is_tent[neighbour] == 0).OnlyEnforceIf(self.is_tent[pos])
        # - the number of tents in each row and column matches the numbers around the edge of the grid 
        for row in range(self.N):
            row_vars = [self.is_tent[pos] for pos in get_row_pos(row, self.N)]
            self.model.Add(lxp.sum(row_vars) == self.sides['side'][row])
        for col in range(self.N):
            col_vars = [self.is_tent[pos] for pos in get_col_pos(col, self.N)]
            self.model.Add(lxp.sum(col_vars) == self.sides['top'][col])
        # - it is possible to match tents to trees so that each tree is orthogonally adjacent to its own tent (but may also be adjacent to other tents). 
        # for each tree, one of the following must be true:
        # a tent on its left has direction RIGHT
        # a tent on its right has direction LEFT
        # a tent on its top has direction DOWN
        # a tent on its bottom has direction UP
        for tree in self.tree_positions:
            self.add_tree_constraints(tree)

    def add_tree_constraints(self, tree_pos: Pos):
        left_pos = get_next_pos(tree_pos, Direction.LEFT)
        right_pos = get_next_pos(tree_pos, Direction.RIGHT)
        top_pos = get_next_pos(tree_pos, Direction.UP)
        bottom_pos = get_next_pos(tree_pos, Direction.DOWN)
        var_list = []
        if left_pos in self.star_positions:
            aux = self.model.NewBoolVar(f'{tree_pos}:left')
            self.model.Add(self.tent_direction[left_pos] == Direction.RIGHT.value).OnlyEnforceIf(aux)
            self.model.Add(self.tent_direction[left_pos] != Direction.RIGHT.value).OnlyEnforceIf(aux.Not())
            var_list.append(aux)
        if right_pos in self.star_positions:
            aux = self.model.NewBoolVar(f'{tree_pos}:right')
            self.model.Add(self.tent_direction[right_pos] == Direction.LEFT.value).OnlyEnforceIf(aux)
            self.model.Add(self.tent_direction[right_pos] != Direction.LEFT.value).OnlyEnforceIf(aux.Not())
            var_list.append(aux)
        if top_pos in self.star_positions:
            aux = self.model.NewBoolVar(f'{tree_pos}:top')
            self.model.Add(self.tent_direction[top_pos] == Direction.DOWN.value).OnlyEnforceIf(aux)
            self.model.Add(self.tent_direction[top_pos] != Direction.DOWN.value).OnlyEnforceIf(aux.Not())
            var_list.append(aux)
        if bottom_pos in self.star_positions:
            aux = self.model.NewBoolVar(f'{tree_pos}:bottom')
            self.model.Add(self.tent_direction[bottom_pos] == Direction.UP.value).OnlyEnforceIf(aux)
            self.model.Add(self.tent_direction[bottom_pos] != Direction.UP.value).OnlyEnforceIf(aux.Not())
            var_list.append(aux)
        self.model.AddBoolOr(var_list)

    def solve_and_print(self):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, int] = {}
            for pos, var in board.is_tent.items():
                if isinstance(var, int):
                    continue
                assignment[pos] = solver.value(var)
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.full((self.N, self.N), ' ', dtype=object)
            for pos in get_all_pos(self.N):
                c = get_char(self.board, pos)
                if c == ' ':
                    c = single_res.assignment[pos]
                    c = 'E' if c == 1 else ' '
                set_char(res, pos, c)
            print(res)
        return generic_solve_all(self, board_to_solution, callback=callback)
