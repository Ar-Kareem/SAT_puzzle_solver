from collections import defaultdict

import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, set_char, Direction, get_next_pos, in_bounds
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution, or_constraint


def get_bool_var(model: cp_model.CpModel, var: cp_model.IntVar, eq_val: int, name: str) -> cp_model.IntVar:
    res = model.NewBoolVar(name)
    model.Add(var == eq_val).OnlyEnforceIf(res)
    model.Add(var != eq_val).OnlyEnforceIf(res.Not())
    return res


class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all(0 <= int(i.item()) <= 9 for i in np.nditer(board)), 'board must contain only alphanumeric characters or space'
        assert np.min(board) == 0, 'expected board to start from 0'
        self.board = board
        self.max_val = np.max(board)

        self.V = board.shape[0]
        self.H = board.shape[1]

        # for every pair, list where to find it on the board and which direction to go
        # no need for left and up directions as the pairs are unordered (so right and down would have already captured both)
        self.pair_to_pos_list: dict[tuple[int, int], list[tuple[Pos, Direction]]] = defaultdict(list)
        for pos in get_all_pos(self.V, self.H):
            right_pos = get_next_pos(pos, Direction.RIGHT)
            if in_bounds(right_pos, self.V, self.H):
                cur_pair = (int(get_char(self.board, pos)), int(get_char(self.board, right_pos)))
                cur_pair = tuple(sorted(cur_pair))  # pairs are unordered
                self.pair_to_pos_list[cur_pair].append((pos, Direction.RIGHT))
            down_pos = get_next_pos(pos, Direction.DOWN)
            if in_bounds(down_pos, self.V, self.H):
                cur_pair = (int(get_char(self.board, pos)), int(get_char(self.board, down_pos)))
                cur_pair = tuple(sorted(cur_pair))  # pairs are unordered
                self.pair_to_pos_list[cur_pair].append((pos, Direction.DOWN))

        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}
        self.pair_vars: dict[tuple[int, int], cp_model.BoolVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[pos] = self.model.NewIntVar(1, 4, f'{pos}')  # directions
        # for even pair, boolean variable to indicate if it appears
        for i in range(self.max_val + 1):
            for j in range(i, self.max_val + 1):
                if (i, j) in self.pair_vars:
                    print('already in pair_vars')
                    continue
                self.pair_vars[(i, j)] = self.model.NewBoolVar(f'{i}_{j}')

    def add_all_constraints(self):
        # all pairs must be used
        self.all_pairs_used()
        self.constrain_domino_shape()
        self.constrain_pair_activation()


        # for pos in get_all_pos(self.V, self.H):
        #     # to the right
        #     right_pos = get_next_pos(pos, Direction.RIGHT)
        #     if not in_bounds(right_pos, self.V, self.H):
        #         continue
        #     v = self.model.NewBoolVar(f'{pos}:right')
        #     and_constraint(self.model, v, [self.model_vars[pos] == Direction.RIGHT.value, self.model_vars[right_pos] == Direction.LEFT.value])

    def all_pairs_used(self):
        for pair in self.pair_vars:
            self.model.Add(self.pair_vars[pair] == 1)

    def constrain_domino_shape(self):
        # if X is right then the cell to its right must be left
        # if X is down then the cell to its down must be up
        # if X is left then the cell to its left must be right
        # if X is up then the cell to its up must be down
        for pos in get_all_pos(self.V, self.H):
            right_pos = get_next_pos(pos, Direction.RIGHT)
            if in_bounds(right_pos, self.V, self.H):
                aux = get_bool_var(self.model, self.model_vars[right_pos], Direction.LEFT.value, f'{pos}:right')
                self.model.Add(self.model_vars[pos] == Direction.RIGHT.value).OnlyEnforceIf([aux])
                self.model.Add(self.model_vars[pos] != Direction.RIGHT.value).OnlyEnforceIf([aux.Not()])
            else:
                self.model.Add(self.model_vars[pos] != Direction.RIGHT.value)
            down_pos = get_next_pos(pos, Direction.DOWN)
            if in_bounds(down_pos, self.V, self.H):
                aux = get_bool_var(self.model, self.model_vars[down_pos], Direction.UP.value, f'{pos}:down')
                self.model.Add(self.model_vars[pos] == Direction.DOWN.value).OnlyEnforceIf([aux])
                self.model.Add(self.model_vars[pos] != Direction.DOWN.value).OnlyEnforceIf([aux.Not()])
            else:
                self.model.Add(self.model_vars[pos] != Direction.DOWN.value)
            left_pos = get_next_pos(pos, Direction.LEFT)
            if in_bounds(left_pos, self.V, self.H):
                aux = get_bool_var(self.model, self.model_vars[left_pos], Direction.RIGHT.value, f'{pos}:left')
                self.model.Add(self.model_vars[pos] == Direction.LEFT.value).OnlyEnforceIf([aux])
                self.model.Add(self.model_vars[pos] != Direction.LEFT.value).OnlyEnforceIf([aux.Not()])
            else:
                self.model.Add(self.model_vars[pos] != Direction.LEFT.value)
            top_pos = get_next_pos(pos, Direction.UP)
            if in_bounds(top_pos, self.V, self.H):
                aux = get_bool_var(self.model, self.model_vars[top_pos], Direction.DOWN.value, f'{pos}:top')
                self.model.Add(self.model_vars[pos] == Direction.UP.value).OnlyEnforceIf([aux])
                self.model.Add(self.model_vars[pos] != Direction.UP.value).OnlyEnforceIf([aux.Not()])
            else:
                self.model.Add(self.model_vars[pos] != Direction.UP.value)

    def constrain_pair_activation(self):
        for pair, pos_list in self.pair_to_pos_list.items():
            aux_list = []
            for pos, direction in pos_list:
                aux_list.append(get_bool_var(self.model, self.model_vars[pos], direction.value, f'{pos}:{direction.name}'))
            or_constraint(self.model, self.pair_vars[pair], aux_list)

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
                c = Direction(single_res.assignment[pos]).name[:1]
                set_char(res, pos, c)
            print(res)
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
