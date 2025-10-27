import time
import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, get_next_pos, Direction


class Board:
    def __init__(self, board: np.array, time_horizon: int = 10):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all(str(c.item()).isdecimal() for c in np.nditer(board)), 'board must contain only digits'
        self.board = board
        self.target_state = np.sort(board, axis=None).reshape(board.shape)
        self.V, self.H = board.shape
        self.min_value = int(np.min(board.flatten()))
        self.max_value = int(np.max(board.flatten()))
        self.time_horizon = time_horizon

        self.model = cp_model.CpModel()
        self.state: dict[tuple[Pos, int], cp_model.IntVar] = {}
        self.decision: dict[int, dict[Pos, cp_model.IntVar]] = {t: {} for t in range(self.time_horizon - 1)}

        self.create_vars()
        self.add_all_constraints()
        self.minimize_actions()
        self.constrain_final_state()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            for t in range(self.time_horizon):
                self.state[pos, t] = self.model.NewIntVar(self.min_value, self.max_value, f'state:{pos}:{t}')
        for t in range(self.time_horizon - 1):
            self.decision[t]['NOOP'] = self.model.NewBoolVar(f'decision:NOOP:{t}')
            for pos in get_all_pos(self.V, self.H):
                if pos.x == self.H - 1 or pos.y == self.V - 1:
                    continue
                self.decision[t][pos] = self.model.NewBoolVar(f'decision:{pos}:{t}')

    def add_all_constraints(self):
        # one action at most every time
        for decision_at_t in self.decision.values():
            self.model.AddExactlyOne(list(decision_at_t.values()))
        # constrain the state at t=0
        for pos in get_all_pos(self.V, self.H):
            self.model.Add(self.state[pos, 0] == get_char(self.board, pos))
        # constrain the state dynamics at t=1..T
        for action_pos in get_all_pos(self.V, self.H):
            if action_pos.x == self.H - 1 or action_pos.y == self.V - 1:
                continue
            self.constrain_state(action_pos)
        # state does not change if NOOP is chosen
        for t in range(1, self.time_horizon):
            noop_var = self.decision[t - 1]['NOOP']
            for pos in get_all_pos(self.V, self.H):
                self.model.Add(self.state[pos, t] == self.state[pos, t - 1]).OnlyEnforceIf(noop_var)

    def constrain_state(self, action: Pos):
        tl = action
        tr = get_next_pos(tl, Direction.RIGHT)
        bl = get_next_pos(tl, Direction.DOWN)
        br = get_next_pos(tr, Direction.DOWN)
        two_by_two = (tl, tr, br, bl)
        # lock state outside the two by two
        for pos in get_all_pos(self.V, self.H):
            if pos in two_by_two:
                continue
            for t in range(1, self.time_horizon):
                self.model.Add(self.state[pos, t] == self.state[pos, t - 1]).OnlyEnforceIf(self.decision[t - 1][action])
        # rotate clockwise inside the two by two
        clockwise = two_by_two[-1:] + two_by_two[:-1]
        # print('action', action)
        # print('two_by_two', two_by_two)
        # print('clockwise', clockwise)
        for pre_pos, post_pos in zip(clockwise, two_by_two):
            for t in range(1, self.time_horizon):
                # print(f'IF self.decision[{t - 1}][{action}] THEN self.state[{post_pos}, {t}] == self.state[{pre_pos}, {t - 1}]')
                self.model.Add(self.state[post_pos, t] == self.state[pre_pos, t - 1]).OnlyEnforceIf(self.decision[t - 1][action])

    def constrain_final_state(self):
        final_time = self.time_horizon - 1
        for pos in get_all_pos(self.V, self.H):
            self.model.Add(self.state[pos, final_time] == get_char(self.target_state, pos))

    def minimize_actions(self):
        flat_decisions = [(var, t+1) for t, tvs in self.decision.items() for pos, var in tvs.items() if pos != 'NOOP']
        self.model.Minimize(lxp.weighted_sum([p[0] for p in flat_decisions], [p[1] for p in flat_decisions]))

    def solve_and_print(self, verbose: bool = True):
        solver = cp_model.CpSolver()
        tic = time.time()
        solver.solve(self.model)
        assignment: dict[Pos] = [None for _ in range(self.time_horizon - 1)]
        if solver.StatusName() in ['OPTIMAL', 'FEASIBLE']:
            for t, tvs in self.decision.items():
                for pos, var in tvs.items():
                    if solver.Value(var) == 1:
                        assignment[t] = (pos.x, pos.y) if pos != 'NOOP' else 'NOOP'
            for t in range(self.time_horizon):
                res_at_t = np.full((self.V, self.H), ' ', dtype=object)
                for pos in get_all_pos(self.V, self.H):
                    res_at_t[pos.y][pos.x] = solver.Value(self.state[pos, t])
                print(f't={t}')
                print(res_at_t)
            if verbose:
                print("Solution found:", assignment)
        if verbose:
            print("status:", solver.StatusName())
            toc = time.time()
            print(f"Time taken: {toc - tic:.2f} seconds")
        return assignment

