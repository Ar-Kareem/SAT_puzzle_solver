import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, set_char, get_char
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution, force_connected_component
from puzzle_solver.core.utils_visualizer import combined_function, id_board_to_wall_fn


class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        self.board = board
        self.V, self.H = board.shape
        self.unique_colors = set([str(c.item()).strip() for c in np.nditer(board) if str(c.item()).strip() not in ['', '#']])
        assert all(np.count_nonzero(board == color) >= 2 for color in self.unique_colors), f'each color must appear >= 2 times, got {self.unique_colors}'
        self.model = cp_model.CpModel()
        self.model_vars: dict[tuple[Pos, str], cp_model.IntVar] = {}
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            for color in self.unique_colors:
                self.model_vars[(pos, color)] = self.model.NewBoolVar(f'{pos}:{color}')

    def add_all_constraints(self):
        for pos in get_all_pos(self.V, self.H):
            self.model.AddExactlyOne([self.model_vars[(pos, color)] for color in self.unique_colors])
            c = get_char(self.board, pos)
            if c.strip() not in ['', '#']:
                self.model.Add(self.model_vars[(pos, c)] == 1)
        for color in self.unique_colors:
            force_connected_component(self.model, {pos: self.model_vars[(pos, color)] for pos in get_all_pos(self.V, self.H)})

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, str] = {}
            for (pos, color), var in board.model_vars.items():
                if solver.Value(var) == 1:
                    assignment[pos] = color
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.full((self.V, self.H), ' ', dtype=object)
            for pos in get_all_pos(self.V, self.H):
                set_char(res, pos, single_res.assignment[pos])
            print(combined_function(self.V, self.H,
                cell_flags=id_board_to_wall_fn(res),
                center_char=lambda r, c: res[r][c]))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
