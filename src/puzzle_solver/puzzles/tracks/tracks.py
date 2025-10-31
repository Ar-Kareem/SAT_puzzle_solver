from collections import defaultdict
import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, Direction, get_next_pos, get_row_pos, get_col_pos, get_opposite_direction, get_pos
from puzzle_solver.core.utils_ortools import force_connected_component, generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


class Board:
    def __init__(self, board: np.array, side: np.array, top: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all((len(c.item()) == 2) and all(ch in [' ', 'U', 'L', 'D', 'R'] for ch in c.item()) for c in np.nditer(board)), 'board must contain only digits or space'
        self.board = board
        self.V, self.H = board.shape
        self.side = side
        self.top = top
        self.first_col_start_pos = [p for p in get_col_pos(0, self.V) if 'L' in get_char(self.board, p)]
        assert len(self.first_col_start_pos) == 1, 'first column must have exactly one start position'
        self.first_col_start_pos = self.first_col_start_pos[0]
        self.last_row_end_pos = [p for p in get_row_pos(self.V - 1, self.H) if 'D' in get_char(self.board, p)]
        assert len(self.last_row_end_pos) == 1, 'last row must have exactly one end position'
        self.last_row_end_pos = self.last_row_end_pos[0]

        self.model = cp_model.CpModel()
        self.cell_active: dict[Pos, cp_model.IntVar] = {}
        self.cell_direction: dict[tuple[Pos, Direction], cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.cell_active[pos] = self.model.NewBoolVar(f'{pos}')
            for direction in Direction:
                next_pos = get_next_pos(pos, direction)
                opposite_direction = get_opposite_direction(direction)
                if (next_pos, opposite_direction) in self.cell_direction:
                    self.cell_direction[(pos, direction)] = self.cell_direction[(next_pos, opposite_direction)]
                else:
                    self.cell_direction[(pos, direction)] = self.model.NewBoolVar(f'{pos}:{direction}')

    def add_all_constraints(self):
        # force the already given hints
        str_to_direction = {'U': Direction.UP, 'L': Direction.LEFT, 'D': Direction.DOWN, 'R': Direction.RIGHT}
        for pos in get_all_pos(self.V, self.H):
            for char in get_char(self.board, pos).strip():
                self.model.Add(self.cell_direction[(pos, str_to_direction[char])] == 1)

        # force the already given sides
        for i in range(self.V):
            self.model.Add(sum([self.cell_active[pos] for pos in get_row_pos(i, self.H)]) == self.side[i])
        for i in range(self.H):
            self.model.Add(sum([self.cell_active[pos] for pos in get_col_pos(i, self.V)]) == self.top[i])

        # cell active means exactly 2 directions are active, cell not active means no directions are active
        for pos in get_all_pos(self.V, self.H):
            s = sum([self.cell_direction[(pos, direction)] for direction in Direction])
            self.model.Add(s == 2).OnlyEnforceIf(self.cell_active[pos])
            self.model.Add(s == 0).OnlyEnforceIf(self.cell_active[pos].Not())

        # force borders
        for pos in get_col_pos(0, self.V):  # first column cant have L unless it is the start position
            if pos != self.first_col_start_pos:
                self.model.Add(self.cell_direction[(pos, Direction.LEFT)] == 0)
        for pos in get_col_pos(self.H - 1, self.V):  # last column cant have R
            self.model.Add(self.cell_direction[(pos, Direction.RIGHT)] == 0)
        for pos in get_row_pos(self.V - 1, self.H):  # last row cant have D unless it is the end position
            if pos != self.last_row_end_pos:
                self.model.Add(self.cell_direction[(pos, Direction.DOWN)] == 0)
        for pos in get_row_pos(0, self.H):  # first row cant have U
            self.model.Add(self.cell_direction[(pos, Direction.UP)] == 0)

        # force single connected component
        def is_neighbor(pd1: tuple[Pos, Direction], pd2: tuple[Pos, Direction]) -> bool:
            p1, d1 = pd1
            p2, d2 = pd2
            if p1 == p2:  # same position, different direction, is neighbor
                return True
            if get_next_pos(p1, d1) == p2 and d2 == get_opposite_direction(d1):
                return True
            return False
        force_connected_component(self.model, self.cell_direction, is_neighbor=is_neighbor)

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, str] = defaultdict(str)
            for (pos, direction), var in board.cell_direction.items():
                assignment[pos] += direction.name[0] if solver.BooleanValue(var) else ''
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H, show_grid=False, special_content=lambda r, c: single_res.assignment[get_pos(x=c, y=r)].strip(), center_char=lambda r, c: '.', text_on_shaded_cells=False))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose, max_solutions=20)
