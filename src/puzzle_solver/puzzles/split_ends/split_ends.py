import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Direction8, Pos, get_all_pos, get_char, get_neighbors8, get_pos, get_row_pos, get_col_pos, Direction, get_opposite_direction, get_next_pos, in_bounds
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all(c.item() in ['L', 'R', 'U', 'D', 'O', ' '] for c in np.nditer(board)), 'board must contain only L, R, U, D, O, or space'
        self.STATES = list(Direction) + ['O']
        self.board = board
        self.V, self.H = board.shape
        assert self.V == 6 and self.H == 6, f'board must be 6x6, got {self.V}x{self.H}'
        self.model = cp_model.CpModel()
        self.model_vars: dict[tuple[Pos, str], cp_model.IntVar] = {}
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            for direction in self.STATES:
                self.model_vars[(pos, direction)] = self.model.NewBoolVar(f'{pos}:{direction}')
            self.model.AddExactlyOne([self.model_vars[(pos, direction)] for direction in self.STATES])

    def add_all_constraints(self):
        for pos in get_all_pos(self.V, self.H):  # force clues
            c = get_char(self.board, pos)
            c = {'L': Direction.LEFT, 'R': Direction.RIGHT, 'U': Direction.UP, 'D': Direction.DOWN, 'O': 'O'}.get(c, None)
            if c is not None:
                self.model.Add(self.model_vars[(pos, c)] == 1)
        for row in range(self.V):  # each row, 1 of each direction and 2 O's
            for direction in Direction:
                self.model.AddExactlyOne([self.model_vars[(pos, direction)] for pos in get_row_pos(row, self.H)])
        for col in range(self.H):  # each column, 1 of each direction and 2 O's
            for direction in Direction:
                self.model.AddExactlyOne([self.model_vars[(pos, direction)] for pos in get_col_pos(col, self.V)])
        for pos in get_all_pos(self.V, self.H):
            for direction in Direction:
                self.apply_orientation_rule(pos, direction)

    def apply_orientation_rule(self, pos: Pos, direction: Direction):
        # if cell is direction (for example L), then the cell to its left must not be R, and the cell to its up-right and down-right must also not be R
        # and the cell to its up-right cant be U and the cell to its down-right cant be D. You have to see the triangles visually for it to make sense.
        assert direction in Direction, f'direction must be in Direction, got {direction}'
        if direction == Direction.LEFT:
            disallow_pairs = [
                (get_next_pos(pos, Direction8.LEFT), Direction.RIGHT),
                (get_next_pos(pos, Direction8.UP_RIGHT), Direction.RIGHT),
                (get_next_pos(pos, Direction8.DOWN_RIGHT), Direction.RIGHT),
                (get_next_pos(pos, Direction8.UP_RIGHT), Direction.UP),
                (get_next_pos(pos, Direction8.DOWN_RIGHT), Direction.DOWN),
            ]
        elif direction == Direction.RIGHT:
            disallow_pairs = [
                (get_next_pos(pos, Direction8.RIGHT), Direction.LEFT),
                (get_next_pos(pos, Direction8.UP_LEFT), Direction.LEFT),
                (get_next_pos(pos, Direction8.DOWN_LEFT), Direction.LEFT),
                (get_next_pos(pos, Direction8.UP_LEFT), Direction.UP),
                (get_next_pos(pos, Direction8.DOWN_LEFT), Direction.DOWN),
            ]
        elif direction == Direction.UP:
            disallow_pairs = [
                (get_next_pos(pos, Direction8.UP), Direction.DOWN),
                (get_next_pos(pos, Direction8.DOWN_LEFT), Direction.DOWN),
                (get_next_pos(pos, Direction8.DOWN_RIGHT), Direction.DOWN),
                (get_next_pos(pos, Direction8.DOWN_LEFT), Direction.LEFT),
                (get_next_pos(pos, Direction8.DOWN_RIGHT), Direction.RIGHT),
            ]
        elif direction == Direction.DOWN:
            disallow_pairs = [
                (get_next_pos(pos, Direction8.DOWN), Direction.UP),
                (get_next_pos(pos, Direction8.UP_LEFT), Direction.UP),
                (get_next_pos(pos, Direction8.UP_RIGHT), Direction.UP),
                (get_next_pos(pos, Direction8.UP_LEFT), Direction.LEFT),
                (get_next_pos(pos, Direction8.UP_RIGHT), Direction.RIGHT),
            ]
        else:
            raise ValueError(f'invalid direction: {direction}')
        disallow_pairs = [d_pair for d_pair in disallow_pairs if in_bounds(d_pair[0], self.V, self.H)]
        for d_pos, d_direction in disallow_pairs:
            self.model.Add(self.model_vars[(d_pos, d_direction)] == 0).OnlyEnforceIf(self.model_vars[(pos, direction)])


    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: 'O' if direction == 'O' else direction.name[0] for (pos, direction), var in board.model_vars.items() if solver.Value(var) == 1})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H, center_char=lambda r, c: single_res.assignment.get(get_pos(x=c, y=r), ' ')))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
