from dataclasses import dataclass
from typing import Optional, Union
import json

import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_row_pos, get_col_pos, in_bounds, get_opposite_direction, get_next_pos, Direction
from puzzle_solver.core.utils_ortools import generic_solve_all


@dataclass(frozen=True)
class SingleSolution:
    assignment: dict[Pos, Union[str, int]]
    beam_assignments: dict[Pos, list[tuple[int, Pos, Direction]]]

    def get_hashable_solution(self) -> str:
        result = []
        for pos, v in self.assignment.items():
            result.append((pos.x, pos.y, v))
        return json.dumps(result, sort_keys=True)


class Board:
    def __init__(self, top: list, right: list, bottom: list, left: list, ball_count: Optional[tuple[int, int]] = None, max_travel_steps: Optional[int] = None):
        assert len(top) == len(bottom), 'top and bottom must be the same length'
        assert len(left) == len(right), 'left and right must be the same length'
        self.K = len(top) + len(right) + len(bottom) + len(left)  # side count
        self.H = len(top)
        self.V = len(left)
        if max_travel_steps is None:
            self.T = self.V * self.H  # maximum travel steps for a beam that bounces an undefined number of times
        else:
            self.T = max_travel_steps
        self.ball_count = ball_count

        # top and bottom entry cells are at -1 and V
        self.top_cells = set(get_row_pos(row_idx=-1, H=self.H))
        self.bottom_cells = set(get_row_pos(row_idx=self.V, H=self.H))
        # left and right entry cells are at -1 and H
        self.left_cells = set(get_col_pos(col_idx=-1, V=self.V))
        self.right_cells = set(get_col_pos(col_idx=self.H, V=self.V))
        # self.top_cells = set([Pos(x=1, y=-1)])
        # self.bottom_cells = set()
        # self.left_cells = set()
        # self.right_cells = set()
        # print(self.top_cells)

        self.top_values = top
        self.right_values = right
        self.bottom_values = bottom
        self.left_values = left

        self.model = cp_model.CpModel()
        self.ball_states: dict[Pos, cp_model.IntVar] = {}
        # (entry_pos, T, cell_pos, direction) -> True if the beam that entered from the board at "entry_pos" is present in "cell_pos" and is going in the direction "direction" at time T
        self.beam_states: dict[tuple[Pos, int, Pos, Direction], cp_model.IntVar] = {}
        # self.beam_states_ending_at: dict[Pos, cp_model.IntVar] = {}
        self.beam_states_at_t: dict[int, dict[Pos, dict[tuple[Pos, Direction], cp_model.IntVar]]] = {}
        self.create_vars()
        print('Total number of variables:', len(self.ball_states), len(self.beam_states))
        self.add_all_constraints()
        print('Solving...')

    def get_outside_border(self):
        top_border = tuple(get_row_pos(row_idx=-1, H=self.H))
        bottom_border = tuple(get_row_pos(row_idx=self.V, H=self.H))
        left_border = tuple(get_col_pos(col_idx=-1, V=self.V))
        right_border = tuple(get_col_pos(col_idx=self.H, V=self.V))
        return (*top_border, *bottom_border, *left_border, *right_border)

    def get_all_pos_extended(self):
        return (*self.get_outside_border(), *get_all_pos(self.V, self.H))

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.ball_states[pos] = self.model.NewBoolVar(f'ball_at:{pos}')
        for pos in self.get_all_pos_extended():  # NxN board + 4 edges
            if pos not in self.ball_states:  # pos is not in the board -> its on the edge
                self.ball_states[pos] = None  # balls cant be on the edge

        for entry_pos in (self.top_cells | self.right_cells | self.bottom_cells | self.left_cells):

            for t in range(self.T):
                self.beam_states[(entry_pos, t, 'HIT', 'HIT')] = self.model.NewBoolVar(f'beam:{entry_pos}:{t}:HIT:HIT')
                for cell in self.get_all_pos_extended():
                    for direction in Direction:
                        self.beam_states[(entry_pos, t, cell, direction)] = self.model.NewBoolVar(f'beam:{entry_pos}:{t}:{cell}:{direction}')

        for (entry_pos, t, cell, direction) in self.beam_states.keys():
            if t not in self.beam_states_at_t:
                self.beam_states_at_t[t] = {}
            if entry_pos not in self.beam_states_at_t[t]:
                self.beam_states_at_t[t][entry_pos] = {}
            self.beam_states_at_t[t][entry_pos][(cell, direction)] = self.beam_states[(entry_pos, t, cell, direction)]

    def add_all_constraints(self):
        self.init_beams()
        self.constrain_beam_movement()
        self.constrain_final_beam_states()
        if self.ball_count is not None:
            s = sum([b for b in self.ball_states.values() if b is not None])
            b_min, b_max = self.ball_count
            self.model.Add(s >= b_min)
            self.model.Add(s <= b_max)

    def init_beams(self):
        beam_ids = []
        beam_ids.extend((beam_id, Direction.DOWN) for beam_id in self.top_cells)
        beam_ids.extend((beam_id, Direction.LEFT) for beam_id in self.right_cells)
        beam_ids.extend((beam_id, Direction.UP) for beam_id in self.bottom_cells)
        beam_ids.extend((beam_id, Direction.RIGHT) for beam_id in self.left_cells)

        for (beam_id, direction) in beam_ids:
            # beam at t=0 is present at beam_id and facing direction
            self.model.Add(self.beam_states[(beam_id, 0, beam_id, direction)] == 1)
            for p in self.get_all_pos_extended():
                # print(f'beam can be at {p}')
                for direction in Direction:
                    if (p, direction) != (beam_id, direction):
                        self.model.Add(self.beam_states[(beam_id, 0, p, direction)] == 0)
        # for p in self.get_all_pos_extended():
        #     print(f'beam can be at {p}')


    def constrain_beam_movement(self):
        for t in range(self.T):
            for entry_pos in self.beam_states_at_t[t].keys():
                next_state_dict = self.beam_states_at_t[t][entry_pos]
                self.model.AddExactlyOne(list(next_state_dict.values()))
                # print('add exactly one constraint for beam id', entry_pos, 'at time', t, next_state_dict.keys(), '\n')
                if t == self.T - 1:
                    continue
                for (cell, direction), prev_state in next_state_dict.items():
                    # print(f'for beam id {entry_pos}, time {t}\nif its at {cell} facing {direction}')
                    self.constrain_next_beam_state(entry_pos, t+1, cell, direction, prev_state)


    def constrain_next_beam_state(self, entry_pos: Pos, t: int, cur_pos: Pos, direction: Direction, prev_state: cp_model.IntVar):
        # print(f"constraining next beam state for {entry_pos}, {t}, {cur_pos}, {direction}")
        if cur_pos == "HIT":  # a beam that was "HIT" stays "HIT"
            # print(f'                                        HIT -> stays HIT')
            self.model.Add(self.beam_states[(entry_pos, t, "HIT", "HIT")] == 1).OnlyEnforceIf(prev_state)
            return
        # if a beam is outside the board AND it is not facing the board -> it maintains its state
        pos_ahead = get_next_pos(cur_pos, direction)
        if not in_bounds(pos_ahead, self.V, self.H) and not in_bounds(cur_pos, self.V, self.H):
            # print(f'                                        OUTSIDE BOARD -> beam stays in the same state')
            self.model.Add(self.beam_states[(entry_pos, t, cur_pos, direction)] == 1).OnlyEnforceIf(prev_state)
            return

        # look at the 3 balls ahead of the beam: thus 8 possible scenarios
        # A beam with no balls ahead of it -> moves forward in the same direction (1 scenario)
        # A beam that hits a ball head-on -> beam is "HIT" (4 scenarios)
        # A beam with a ball in its front-left square and no ball ahead of it -> gets deflected 90 degrees to the right (1 scenario)
        # A beam with a ball in its front-right square and no ball ahead of it -> gets similarly deflected to the left (1 scenario)
        # A beam that would in its front-left AND front-right squares -> is reflected (1 scenarios)

        direction_left = {
            Direction.UP: Direction.LEFT,
            Direction.LEFT: Direction.DOWN,
            Direction.DOWN: Direction.RIGHT,
            Direction.RIGHT: Direction.UP,
        }[direction]
        direction_right = {
            Direction.UP: Direction.RIGHT,
            Direction.RIGHT: Direction.DOWN,
            Direction.DOWN: Direction.LEFT,
            Direction.LEFT: Direction.UP,
        }[direction]
        reflected = get_opposite_direction(direction)
        ball_left_pos = get_next_pos(pos_ahead, direction_left)
        ball_right_pos = get_next_pos(pos_ahead, direction_right)
        if in_bounds(pos_ahead, self.V, self.H):
            ball_ahead = self.ball_states[pos_ahead]
            ball_ahead_not = ball_ahead.Not()
        else:
            ball_ahead = False
            ball_ahead_not = True
        if in_bounds(ball_left_pos, self.V, self.H):
            ball_left = self.ball_states[ball_left_pos]
            ball_left_not = ball_left.Not()
        else:
            ball_left = False
            ball_left_not = True
        if in_bounds(ball_right_pos, self.V, self.H):
            ball_right = self.ball_states[ball_right_pos]
            ball_right_not = ball_right.Not()
        else:
            ball_right = False
            ball_right_not = True

        pos_left = get_next_pos(cur_pos, direction_left)
        pos_right = get_next_pos(cur_pos, direction_right)
        pos_reflected = get_next_pos(cur_pos, reflected)
        if not in_bounds(pos_left, self.V, self.H):
            pos_left = cur_pos
        if not in_bounds(pos_right, self.V, self.H):
            pos_right = cur_pos
        if not in_bounds(pos_reflected, self.V, self.H):
            pos_reflected = cur_pos

        # debug_states = {
        #     'if ball head': (entry_pos, t, "HIT", "HIT"),
        #     'if ball in front-left': (entry_pos, t, get_next_pos(cur_pos, direction_right), direction_right),
        #     'if ball in front-right': (entry_pos, t, get_next_pos(cur_pos, direction_left), direction_left),
        #     'if ball in front-left and front-right': (entry_pos, t, get_next_pos(cur_pos, reflected), reflected),
        #     'if no ball ahead': (entry_pos, t, pos_ahead, direction),
        # }
        # for k,v in debug_states.items():
        #     print(f'                                        {k} -> {v}')

        # ball head-on -> beam is "HIT"
        self.model.Add(self.beam_states[(entry_pos, t, "HIT", "HIT")] == 1).OnlyEnforceIf([
            ball_ahead,
            prev_state,
        ])
        # ball in front-left -> beam is deflected right
        self.model.Add(self.beam_states[(entry_pos, t, pos_right, direction_right)] == 1).OnlyEnforceIf([
            ball_ahead_not,
            ball_left,
            ball_right_not,
            prev_state,
        ])
        # ball in front-right -> beam is deflected left
        self.model.Add(self.beam_states[(entry_pos, t, pos_left, direction_left)] == 1).OnlyEnforceIf([
            ball_ahead_not,
            ball_left_not,
            ball_right,
            prev_state,
        ])
        # ball in front-left and front-right -> beam is reflected
        self.model.Add(self.beam_states[(entry_pos, t, pos_reflected, reflected)] == 1).OnlyEnforceIf([
            ball_ahead_not,
            ball_left,
            ball_right,
            prev_state,
        ])
        # no ball ahead -> beam moves forward in the same direction
        self.model.Add(self.beam_states[(entry_pos, t, pos_ahead, direction)] == 1).OnlyEnforceIf([
            ball_ahead_not,
            ball_left_not,
            ball_right_not,
            prev_state,
        ])

    def constrain_final_beam_states(self):
        all_values = []
        all_values.extend([(Pos(x=c, y=-1), top_value) for c, top_value in enumerate(self.top_values)])
        all_values.extend([(Pos(x=self.H, y=c), right_value) for c, right_value in enumerate(self.right_values)])
        all_values.extend([(Pos(x=c, y=self.V), bottom_value) for c, bottom_value in enumerate(self.bottom_values)])
        all_values.extend([(Pos(x=-1, y=c), left_value) for c, left_value in enumerate(self.left_values)])
        digits = {}
        hits = []
        reflects = []
        for pos, value in all_values:
            value = str(value)
            if value.isdecimal():
                digits.setdefault(value, []).append(pos)
            elif value == 'H':
                hits.append(pos)
            elif value == 'R':
                reflects.append(pos)
            else:
                raise ValueError(f'Invalid value: {value}')
        for digit, pos_list in digits.items():
            assert len(pos_list) == 2, f'digit {digit} has {len(pos_list)} positions: {pos_list}'
            p1, p2 = pos_list
            self.model.AddExactlyOne([self.beam_states[(p1, self.T-1, p2, direction)] for direction in Direction])
            self.model.AddExactlyOne([self.beam_states[(p2, self.T-1, p1, direction)] for direction in Direction])
        for hit in hits:
            self.model.AddExactlyOne([self.beam_states[(hit, self.T-1, 'HIT', 'HIT')]])
        for reflect in reflects:
            self.model.AddExactlyOne([self.beam_states[(reflect, self.T-1, reflect, direction)] for direction in Direction])


    def solve_and_print(self, verbose: bool = True):
        count = 0
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            nonlocal count
            count += 1
            # if count > 99:
            #     import sys
            #     sys.exit(0)
            assignment = {}
            for pos in get_all_pos(self.V, self.H):
                assignment[pos] = solver.value(self.ball_states[pos])
            beam_assignments = {}
            # for (entry_pos, t, cell, direction), v in self.beam_states.items():
            #     if entry_pos not in beam_assignments:
            #         beam_assignments[entry_pos] = []
            #     if solver.value(v):  # for every beam it can only be present in one state at a time
            #         beam_assignments[entry_pos].append((t, cell, direction))
            # for k,v in beam_assignments.items():
            #     beam_assignments[k] = sorted(v, key=lambda x: x[0])
            #     print(k, beam_assignments[k], '\n')
            # print(beam_assignments)
            return SingleSolution(assignment=assignment, beam_assignments=beam_assignments)

        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.full((self.V, self.H), ' ', dtype=object)
            for pos in get_all_pos(self.V, self.H):
                ball_state = 'O' if single_res.assignment[pos] else ' '
                res[pos.y][pos.x] = ball_state
            print(res)
        r = generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
        # print('non unique count:', count)





