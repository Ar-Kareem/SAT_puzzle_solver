from enum import Enum

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from core.utils import Pos, get_all_pos, get_char, set_char, in_bounds, get_next_pos, Direction, get_row_pos, get_col_pos
from core.utils_ortools import generic_solve_all, SingleSolution


class State(Enum):
    BLANK = ('BLANK', ' ')
    POSITIVE = ('POSITIVE', '+')
    NEGATIVE = ('NEGATIVE', '-')


class Board:
    def __init__(self, board: np.array, sides: dict[str, np.array]):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert len(sides) == 4, '4 sides must be provided'
        assert all(s.ndim == 1 for s in sides.values()), 'all sides must be 1d'
        assert set(sides.keys()) == set(['pos_v', 'neg_v', 'pos_h', 'neg_h'])
        assert sides['pos_h'].shape[0] == board.shape[0], 'pos_h dim must equal vertical board size'
        assert sides['neg_h'].shape[0] == board.shape[0], 'neg_h dim must equal vertical board size'
        assert sides['pos_v'].shape[0] == board.shape[1], 'pos_v dim must equal horizontal board size'
        assert sides['neg_v'].shape[0] == board.shape[1], 'neg_v dim must equal horizontal board size'
        self.board = board
        self.sides = sides
        self.V = board.shape[0]
        self.H = board.shape[1]
        self.model = cp_model.CpModel()
        self.pairs: set[tuple[Pos, Pos]] = set()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        # init vars
        for pos in get_all_pos(V=self.V, H=self.H):
            var_list = []
            for state in State:
                v = self.model.NewBoolVar(f'{pos}:{state.value[0]}')
                self.model_vars[(pos, state)] = v
                var_list.append(v)
            self.model.AddExactlyOne(var_list)
        # init pairs. traverse from top left and V indicates vertical domino (2x1) while H is horizontal (1x2)
        seen_pos = set()
        for pos in get_all_pos(V=self.V, H=self.H):
            if pos in seen_pos:
                continue
            seen_pos.add(pos)
            c = get_char(self.board, pos)
            direction = {'V': Direction.DOWN, 'H': Direction.RIGHT}[c]
            other_pos = get_next_pos(pos, direction)
            seen_pos.add(other_pos)
            self.pairs.add((pos, other_pos))
        assert len(self.pairs)*2 == self.V*self.H

    def add_all_constraints(self):
        # pairs must be matching
        for pair in self.pairs:
            a, b = pair
            self.model.add(self.model_vars[(a, State.BLANK)] == self.model_vars[(b, State.BLANK)])
            self.model.add(self.model_vars[(a, State.POSITIVE)] == self.model_vars[(b, State.NEGATIVE)])
            self.model.add(self.model_vars[(a, State.NEGATIVE)] == self.model_vars[(b, State.POSITIVE)])
        # no orthoginal matching poles
        for pos in get_all_pos(V=self.V, H=self.H):
            right_pos = get_next_pos(pos, Direction.RIGHT)
            down_pos = get_next_pos(pos, Direction.DOWN)
            if in_bounds(right_pos, H=self.H, V=self.V):
                self.model.add(self.model_vars[(pos, State.POSITIVE)] == 0).OnlyEnforceIf(self.model_vars[(right_pos, State.POSITIVE)])
                self.model.add(self.model_vars[(right_pos, State.POSITIVE)] == 0).OnlyEnforceIf(self.model_vars[(pos, State.POSITIVE)])
                self.model.add(self.model_vars[(pos, State.NEGATIVE)] == 0).OnlyEnforceIf(self.model_vars[(right_pos, State.NEGATIVE)])
                self.model.add(self.model_vars[(right_pos, State.NEGATIVE)] == 0).OnlyEnforceIf(self.model_vars[(pos, State.NEGATIVE)])
            if in_bounds(down_pos, H=self.H, V=self.V):
                self.model.add(self.model_vars[(pos, State.POSITIVE)] == 0).OnlyEnforceIf(self.model_vars[(down_pos, State.POSITIVE)])
                self.model.add(self.model_vars[(down_pos, State.POSITIVE)] == 0).OnlyEnforceIf(self.model_vars[(pos, State.POSITIVE)])
                self.model.add(self.model_vars[(pos, State.NEGATIVE)] == 0).OnlyEnforceIf(self.model_vars[(down_pos, State.NEGATIVE)])
                self.model.add(self.model_vars[(down_pos, State.NEGATIVE)] == 0).OnlyEnforceIf(self.model_vars[(pos, State.NEGATIVE)])

        # sides counts must equal actual count
        for row_i in range(self.V):
            sum_pos = lxp.sum([self.model_vars[(pos, State.POSITIVE)] for pos in get_row_pos(row_i, self.H)])
            sum_neg = lxp.sum([self.model_vars[(pos, State.NEGATIVE)] for pos in get_row_pos(row_i, self.H)])
            ground_pos = self.sides['pos_h'][row_i]
            ground_neg = self.sides['neg_h'][row_i]
            if ground_pos != -1:
                self.model.Add(sum_pos == ground_pos)
            if ground_neg != -1:
                self.model.Add(sum_neg == ground_neg)
        for col_i in range(self.H):
            sum_pos = lxp.sum([self.model_vars[(pos, State.POSITIVE)] for pos in get_col_pos(col_i, self.V)])
            sum_neg = lxp.sum([self.model_vars[(pos, State.NEGATIVE)] for pos in get_col_pos(col_i, self.V)])
            ground_pos = self.sides['pos_v'][col_i]
            ground_neg = self.sides['neg_v'][col_i]
            if ground_pos != -1:
                self.model.Add(sum_pos == ground_pos)
            if ground_neg != -1:
                self.model.Add(sum_neg == ground_neg)

    def solve_and_print(self):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, str] = {}
            for (pos, state), var in board.model_vars.items():
                if solver.BooleanValue(var):
                    assignment[pos] = state.value[1]
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.full((self.V, self.H), ' ', dtype=object)
            for pos in get_all_pos(V=self.V, H=self.H):
                c = get_char(self.board, pos)
                c = single_res.assignment[pos]
                set_char(res, pos, c)
            print(res)
        return generic_solve_all(self, board_to_solution, callback=callback)
