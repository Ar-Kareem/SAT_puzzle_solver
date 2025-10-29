import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Pos, get_all_pos, set_char, get_char, Direction, get_next_pos, get_opposite_direction
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution, force_connected_component
from puzzle_solver.core.utils_visualizer import combined_function


class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all(c.item().strip() in ['1', '2L', '2I', '3', '4'] for c in np.nditer(board)), 'board must contain only 1, 2L, 2I, 3, 4. Found:' + str(set(c.item().strip() for c in np.nditer(board)) - set(['1', '2L', '2I', '3', '4']))
        self.board = board
        self.V, self.H = board.shape
        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            for direction in Direction:
                mirrored = (get_next_pos(pos, direction), get_opposite_direction(direction))
                if mirrored in self.model_vars:
                    self.model_vars[(pos, direction)] = self.model_vars[mirrored]
                else:
                    self.model_vars[(pos, direction)] = self.model.NewBoolVar(f'{pos}:{direction}')

    def add_all_constraints(self):
        for pos in get_all_pos(self.V, self.H):
            self.force_position(pos, get_char(self.board, pos).strip())
        # single connected component
        self.force_connected_component()

    def force_connected_component(self):
        def is_neighbor(pd1: tuple[Pos, Direction], pd2: tuple[Pos, Direction]) -> bool:
            p1, d1 = pd1
            p2, d2 = pd2
            if p1 == p2 and d1 != d2:  # same position, different direction, is neighbor
                return True
            if get_next_pos(p1, d1) == p2 and d2 == get_opposite_direction(d1):
                return True
            return False
        force_connected_component(self.model, self.model_vars, is_neighbor=is_neighbor)

    def force_position(self, pos: Pos, value: str):
        # cells with 1 or 3 or 4 neighbors each only have 1 unique state under rotational symmetry
        # cells with 2 neighbors can either be a straight line (2I) or curved line (2L)
        if value == '1':
            self.model.Add(lxp.sum([self.model_vars[(pos, direction)] for direction in Direction]) == 1)
        elif value == '2L':
            self.model.Add(self.model_vars[(pos, Direction.LEFT)] != self.model_vars[(pos, Direction.RIGHT)])
            self.model.Add(self.model_vars[(pos, Direction.UP)] != self.model_vars[(pos, Direction.DOWN)])
        elif value == '2I':
            self.model.Add(self.model_vars[(pos, Direction.LEFT)] == self.model_vars[(pos, Direction.RIGHT)])
            self.model.Add(self.model_vars[(pos, Direction.UP)] == self.model_vars[(pos, Direction.DOWN)])
            self.model.Add(self.model_vars[(pos, Direction.UP)] != self.model_vars[(pos, Direction.RIGHT)])
        elif value == '3':
            self.model.Add(lxp.sum([self.model_vars[(pos, direction)] for direction in Direction]) == 3)
        elif value == '4':
            self.model.Add(lxp.sum([self.model_vars[(pos, direction)] for direction in Direction]) == 4)
        else:
            raise ValueError(f'invalid value: {value}')

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment = {}
            for pos in get_all_pos(self.V, self.H):
                assignment[pos] = ''
                for direction in Direction:
                    if solver.Value(board.model_vars[(pos, direction)]) == 1:
                        assignment[pos] += direction.name[0]
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.full((self.V, self.H), ' ', dtype=object)
            for pos in get_all_pos(self.V, self.H):
                set_char(res, pos, single_res.assignment[pos])
            print(combined_function(self.V, self.H, show_grid=False, show_axes=True, special_content=lambda r, c: res[r, c], center_char=lambda r, c: '.', text_on_shaded_cells=False)),
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
