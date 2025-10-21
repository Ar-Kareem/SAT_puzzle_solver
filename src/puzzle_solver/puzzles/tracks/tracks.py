from collections import defaultdict
import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, set_char, get_char, Direction, in_bounds, get_next_pos, get_row_pos, get_col_pos, get_opposite_direction
from puzzle_solver.core.utils_ortools import force_connected_component, generic_solve_all, SingleSolution


class Board:
    def __init__(self, board: np.array, side: np.array, top: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all((len(c.item()) == 2) and all(ch in [' ', 'U', 'L', 'D', 'R'] for ch in c.item()) for c in np.nditer(board)), 'board must contain only digits or space'
        self.board = board
        self.V = board.shape[0]
        self.H = board.shape[1]
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
                self.cell_direction[(pos, direction)] = self.model.NewBoolVar(f'{pos}:{direction}')

    def add_all_constraints(self):
        self.force_hints()
        self.force_sides()
        self.force_0_or_2_active()
        self.force_direction_constraints()
        self.force_connected_component()


    def force_hints(self):
        # force the already given hints
        for pos in get_all_pos(self.V, self.H):
            c = get_char(self.board, pos)
            if 'U' in c:
                self.model.Add(self.cell_direction[(pos, Direction.UP)] == 1)
            if 'L' in c:
                self.model.Add(self.cell_direction[(pos, Direction.LEFT)] == 1)
            if 'D' in c:
                self.model.Add(self.cell_direction[(pos, Direction.DOWN)] == 1)
            if 'R' in c:
                self.model.Add(self.cell_direction[(pos, Direction.RIGHT)] == 1)

    def force_sides(self):
        # force the already given sides
        for i in range(self.V):
            self.model.Add(sum([self.cell_active[pos] for pos in get_row_pos(i, self.H)]) == self.side[i])
        for i in range(self.H):
            self.model.Add(sum([self.cell_active[pos] for pos in get_col_pos(i, self.V)]) == self.top[i])

    def force_0_or_2_active(self):
        # cell active means exactly 2 directions are active, cell not active means no directions are active
        for pos in get_all_pos(self.V, self.H):
            s = sum([self.cell_direction[(pos, direction)] for direction in Direction])
            self.model.Add(s == 2).OnlyEnforceIf(self.cell_active[pos])
            self.model.Add(s == 0).OnlyEnforceIf(self.cell_active[pos].Not())

    def force_direction_constraints(self):
        # X having right means the cell to its right has left and so on for all directions
        for pos in get_all_pos(self.V, self.H):
            right_pos = get_next_pos(pos, Direction.RIGHT)
            if in_bounds(right_pos, self.V, self.H):
                self.model.Add(self.cell_direction[(pos, Direction.RIGHT)] == self.cell_direction[(right_pos, Direction.LEFT)])
            down_pos = get_next_pos(pos, Direction.DOWN)
            if in_bounds(down_pos, self.V, self.H):
                self.model.Add(self.cell_direction[(pos, Direction.DOWN)] == self.cell_direction[(down_pos, Direction.UP)])
            left_pos = get_next_pos(pos, Direction.LEFT)
            if in_bounds(left_pos, self.V, self.H):
                self.model.Add(self.cell_direction[(pos, Direction.LEFT)] == self.cell_direction[(left_pos, Direction.RIGHT)])
            top_pos = get_next_pos(pos, Direction.UP)
            if in_bounds(top_pos, self.V, self.H):
                self.model.Add(self.cell_direction[(pos, Direction.UP)] == self.cell_direction[(top_pos, Direction.DOWN)])

        # first column cant have L unless it is the start position
        for pos in get_col_pos(0, self.V):
            if pos != self.first_col_start_pos:
                self.model.Add(self.cell_direction[(pos, Direction.LEFT)] == 0)
        # last column cant have R
        for pos in get_col_pos(self.H - 1, self.V):
            self.model.Add(self.cell_direction[(pos, Direction.RIGHT)] == 0)
        # last row cant have D unless it is the end position
        for pos in get_row_pos(self.V - 1, self.H):
            if pos != self.last_row_end_pos:
                self.model.Add(self.cell_direction[(pos, Direction.DOWN)] == 0)
        # first row cant have U
        for pos in get_row_pos(0, self.H):
            self.model.Add(self.cell_direction[(pos, Direction.UP)] == 0)

    def force_connected_component(self):
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
            for pos in get_all_pos(self.V, self.H):
                if len(assignment[pos]) == 0:
                    assignment[pos] = '  '
                else:
                    assignment[pos] = ''.join(sorted(assignment[pos]))
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(single_res.assignment)
            res = np.full((self.V, self.H), ' ', dtype=object)
            pretty_dict = {'DU': '┃ ', 'LR': '━━', 'DL': '━┒', 'DR': '┏━', 'RU': '┗━', 'LU': '━┛', '  ': '  '}
            for pos in get_all_pos(self.V, self.H):
                c = get_char(self.board, pos)
                c = single_res.assignment[pos]
                c = pretty_dict[c]
                set_char(res, pos, c)
            print(res)
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose, max_solutions=20)
