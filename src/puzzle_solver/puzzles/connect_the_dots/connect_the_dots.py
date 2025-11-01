import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, get_pos, get_neighbors4
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution, force_connected_component
from puzzle_solver.core.utils_visualizer import combined_function, id_board_to_wall_fn


class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        self.board = board
        self.V, self.H = board.shape
        self.unique_colors = set([str(c.item()).strip() for c in np.nditer(board) if str(c.item()).strip() not in ['', '#']])
        assert all(np.count_nonzero(board == color) == 2 for color in self.unique_colors), f'each color must appear == 2 times, got {self.unique_colors}'
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
            c = get_char(self.board, pos).strip()
            if c == '#':  # a wall, thus no color
                self.model.Add(sum([self.model_vars[(pos, color)] for color in self.unique_colors]) == 0)
                continue
            self.model.AddExactlyOne([self.model_vars[(pos, color)] for color in self.unique_colors])
            if c != '':  # an endpoint, thus must be the color
                self.model.Add(self.model_vars[(pos, c)] == 1)
                self.model.Add(sum([self.model_vars[(n, c)] for n in get_neighbors4(pos, self.V, self.H)]) == 1)  # endpoits must have exactly 1 neighbor
            else:  # not an endpoint, thus must have exactly 2 neighbors
                for color in self.unique_colors:
                    self.model.Add(sum([self.model_vars[(n, color)] for n in get_neighbors4(pos, self.V, self.H)]) == 2).OnlyEnforceIf(self.model_vars[(pos, color)])
        for color in self.unique_colors:
            force_connected_component(self.model, {pos: self.model_vars[(pos, color)] for pos in get_all_pos(self.V, self.H)})

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: color for (pos, color), var in board.model_vars.items() if solver.Value(var) == 1})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H,
                cell_flags=id_board_to_wall_fn(np.array([[single_res.assignment.get(get_pos(x=c, y=r), '') for c in range(self.H)] for r in range(self.V)])),
                center_char=lambda r, c: single_res.assignment.get(get_pos(x=c, y=r), self.board[r, c])))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
