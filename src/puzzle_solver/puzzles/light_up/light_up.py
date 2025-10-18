from enum import Enum

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, set_char, in_bounds, get_next_pos, get_neighbors4, Direction
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution


class State(Enum):
    BLACK = ('BLACK', 'B')
    SHINE = ('SHINE', 'S')
    LIGHT = ('LIGHT', 'L')


def laser_out(board: np.array, init_pos: Pos) -> list[Pos]:
    'laser out in all 4 directions until we hit a wall or out of bounds'
    N = board.shape[0]
    result = []
    for direction in Direction:
        cur_pos = init_pos
        while True:
            cur_pos = get_next_pos(cur_pos, direction)
            if not in_bounds(cur_pos, N) or get_char(board, cur_pos) != '*':
                break
            result.append(cur_pos)
    return result


class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert board.shape[0] == board.shape[1], 'board must be square'
        assert all((c in ['*', 'W']) or str(c).isdecimal() for c in np.nditer(board)), 'board must contain only * or W or numbers'
        self.board = board
        self.N = board.shape[0]
        self.star_positions: set[Pos] = {pos for pos in get_all_pos(self.N) if get_char(self.board, pos) == '*'}
        self.number_position: set[Pos] = {pos for pos in get_all_pos(self.N) if str(get_char(self.board, pos)).isdecimal()}
        self.model = cp_model.CpModel()
        self.model_vars: dict[tuple[Pos, State], cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in self.star_positions:
            var_list = []
            for state in State:
                v = self.model.NewBoolVar(f'{pos}:{state.value[0]}')
                self.model_vars[(pos, state)] = v
                var_list.append(v)
            self.model.AddExactlyOne(var_list)

    def add_all_constraints(self):
        # goal: no black squares
        for pos in self.star_positions:
            self.model.Add(self.model_vars[(pos, State.BLACK)] == 0)
        # number of lights touching a decimal is = decimal
        for pos in self.number_position:
            ground = int(get_char(self.board, pos))
            neighbour_list = get_neighbors4(pos, self.N, self.N)
            neighbour_list = [p for p in neighbour_list if p in self.star_positions]
            neighbour_light_count = lxp.Sum([self.model_vars[(p, State.LIGHT)] for p in neighbour_list])
            self.model.Add(neighbour_light_count == ground)
        # if a square is a light then everything it touches shines
        for pos in self.star_positions:
            orthoginals = laser_out(self.board, pos)
            for ortho in orthoginals:
                self.model.Add(self.model_vars[(ortho, State.SHINE)] == 1).OnlyEnforceIf([self.model_vars[(pos, State.LIGHT)]])
        # a square is black if all of it's laser_out is not light AND itself isnot a light
        for pos in self.star_positions:
            orthoginals = laser_out(self.board, pos)
            i_am_not_light = [self.model_vars[(pos, State.LIGHT)].Not()]
            no_light_in_laser = [self.model_vars[(p, State.LIGHT)].Not() for p in orthoginals]
            self.model.Add(self.model_vars[(pos, State.BLACK)] == 1).OnlyEnforceIf(i_am_not_light + no_light_in_laser)

    def solve_and_print(self):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, str] = {}
            for (pos, state), var in board.model_vars.items():
                if solver.BooleanValue(var):
                    assignment[pos] = state.value[1]
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.full((self.N, self.N), ' ', dtype=object)
            for pos in get_all_pos(self.N):
                c = get_char(self.board, pos)
                if c == '*':
                    c = single_res.assignment[pos]
                    c = 'L' if c == 'L' else ' '
                set_char(res, pos, c)
            print(res)
        return generic_solve_all(self, board_to_solution, callback=callback)
