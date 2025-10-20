import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, set_char, in_bounds, get_next_pos, Direction8
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution


CHAR_TO_DIRECTION8 = {
    'Q': Direction8.UP_LEFT,
    'W': Direction8.UP,
    'E': Direction8.UP_RIGHT,
    'A': Direction8.LEFT,
    'D': Direction8.RIGHT,
    'Z': Direction8.DOWN_LEFT,
    'X': Direction8.DOWN,
    'C': Direction8.DOWN_RIGHT,
}


def beam(pos: Pos, V: int, H: int, direction: Direction8) -> list[Pos]:
    out = []
    while True:
        pos = get_next_pos(pos, direction)
        if not in_bounds(pos, V, H):
            break
        out.append(pos)
    return out

class Board:
    def __init__(self, board: np.array, values: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert values.ndim == 2, f'values must be 2d, got {values.ndim}'
        assert board.shape == values.shape, f'board and values must have the same shape, got {board.shape} and {values.shape}'
        self.board = board
        self.values = values
        self.V = board.shape[0]
        self.H = board.shape[1]
        self.N = self.V * self.H
        assert all(int(c.item()) >= 0 and int(c.item()) <= self.N for c in np.nditer(values)), 'values must contain only integers between 0 and N'

        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(V=self.V, H=self.H):
            self.model_vars[pos] = self.model.NewIntVar(1, self.N, f'{pos}')

    def add_all_constraints(self):
        # constrain clues
        for pos in get_all_pos(V=self.V, H=self.H):
            c = int(get_char(self.values, pos))
            if c == 0:
                continue
            self.model.Add(self.model_vars[pos] == c)
        # all values are unique
        self.model.AddAllDifferent(list(self.model_vars.values()))
        # arrow for x points to x+1
        for pos in get_all_pos(V=self.V, H=self.H):
            c = get_char(self.board, pos)
            if c == ' ':
                continue
            direction = CHAR_TO_DIRECTION8[c]
            self.constrain_plus_one(pos, direction)
    
    def constrain_plus_one(self, pos: Pos, direction: Direction8):
        beam_res = beam(pos, self.V, self.H, direction)
        is_eq_list = []
        for p in beam_res:
            aux = self.model.NewBoolVar(f'{pos}:{p}')
            self.model.Add(self.model_vars[p] == self.model_vars[pos] + 1).OnlyEnforceIf(aux)
            self.model.Add(self.model_vars[p] != self.model_vars[pos] + 1).OnlyEnforceIf(aux.Not())
            is_eq_list.append(aux)
        self.model.Add(lxp.Sum(is_eq_list) == 1)
    
    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, str] = {}
            for pos, var in board.model_vars.items():
                assignment[pos] = solver.Value(var)
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.full((self.V, self.H), ' ', dtype=object)
            for pos in get_all_pos(V=self.V, H=self.H):
                c = get_char(self.board, pos)
                c = single_res.assignment[pos]
                set_char(res, pos, c)
            print(res)
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose, max_solutions=20)
