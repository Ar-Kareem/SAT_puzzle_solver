from collections import defaultdict

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, set_char, get_row_pos, get_col_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution


class Board:
    def __init__(self, board: np.array, max_bridges_per_direction: int = 2):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all(c.item() == ' ' or str(c.item()).isdecimal() for c in np.nditer(board)), 'board must contain only spaces or digits'
        self.board = board
        self.V = board.shape[0]
        self.H = board.shape[1]
        self.max_bridges_per_direction = max_bridges_per_direction
        self.horiz_bridges: set[tuple[Pos, Pos]] = set()
        self.vert_bridges: set[tuple[Pos, Pos]] = set()

        self.model = cp_model.CpModel()
        self.model_vars: dict[tuple[Pos, Pos], cp_model.IntVar] = {}
        self.is_bridge_active: dict[tuple[Pos, Pos], cp_model.IntVar] = {}

        self.init_bridges()
        self.create_vars()
        self.add_all_constraints()

    def init_bridges(self):
        for row_i in range(self.V):
            cells_in_row = [i for i in get_row_pos(row_i, self.H) if get_char(self.board, i) != ' ']
            for cell_i in range(len(cells_in_row) - 1):
                self.horiz_bridges.add((cells_in_row[cell_i], cells_in_row[cell_i + 1]))
        for col_i in range(self.H):
            cells_in_col = [i for i in get_col_pos(col_i, self.V) if get_char(self.board, i) != ' ']
            for cell_i in range(len(cells_in_col) - 1):
                self.vert_bridges.add((cells_in_col[cell_i], cells_in_col[cell_i + 1]))

    def create_vars(self):
        for bridge in self.horiz_bridges | self.vert_bridges:
            self.model_vars[bridge] = self.model.NewIntVar(0, self.max_bridges_per_direction, f'{bridge}')
            self.is_bridge_active[bridge] = self.model.NewBoolVar(f'{bridge}:is_active')
            self.model.Add(self.model_vars[bridge] == 0).OnlyEnforceIf(self.is_bridge_active[bridge].Not())
            self.model.Add(self.model_vars[bridge] > 0).OnlyEnforceIf(self.is_bridge_active[bridge])

    def add_all_constraints(self):
        self.constrain_sums()
        self.constrain_no_overlapping_bridges()

    def constrain_sums(self):
        for pos in get_all_pos(self.V, self.H):
            c = get_char(self.board, pos)
            if c == ' ':
                continue
            all_pos_bridges = [bridge for bridge in self.horiz_bridges if pos in bridge] + [bridge for bridge in self.vert_bridges if pos in bridge]
            self.model.Add(lxp.sum([self.model_vars[bridge] for bridge in all_pos_bridges]) == int(c))

    def constrain_no_overlapping_bridges(self):
        for horiz_bridge in self.horiz_bridges:
            for vert_bridge in self.vert_bridges:
                if self.is_overlapping(horiz_bridge, vert_bridge):
                    self.model.AddImplication(self.is_bridge_active[horiz_bridge], self.is_bridge_active[vert_bridge].Not())
                    self.model.AddImplication(self.is_bridge_active[vert_bridge], self.is_bridge_active[horiz_bridge].Not())

    def is_overlapping(self, horiz_bridge: tuple[Pos, Pos], vert_bridge: tuple[Pos, Pos]) -> bool:
        assert vert_bridge[0].x == vert_bridge[1].x, 'vertical bridge must have constant x'
        assert horiz_bridge[0].y == horiz_bridge[1].y, 'horizontal bridge must have constant y'
        xvert = vert_bridge[0].x
        yvert_min = min(vert_bridge[0].y, vert_bridge[1].y)
        yvert_max = max(vert_bridge[0].y, vert_bridge[1].y)

        xhoriz_min = min(horiz_bridge[0].x, horiz_bridge[1].x)
        xhoriz_max = max(horiz_bridge[0].x, horiz_bridge[1].x)
        yhoriz = horiz_bridge[0].y
        
        # no equals because thats what the puzzle says
        x_contained = xhoriz_min < xvert < xhoriz_max
        y_contained = yvert_min < yhoriz < yvert_max
        return x_contained and y_contained

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment = defaultdict(lambda: [0, 0, 0, 0])
            for bridge in board.horiz_bridges:
                v = solver.Value(board.model_vars[bridge])
                assignment[bridge[0]][0] += v
                assignment[bridge[1]][1] += v
            for bridge in board.vert_bridges:
                v = solver.Value(board.model_vars[bridge])
                assignment[bridge[0]][2] += v
                assignment[bridge[1]][3] += v
            # convert to tuples
            assignment = {pos: tuple(assignment[pos]) for pos in assignment.keys()}
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.full((self.V, self.H), '    ', dtype=object)
            for pos, (h1, h2, v1, v2) in single_res.assignment.items():
                c = str(h1) + str(h2) + str(v1) + str(v2)
                set_char(res, pos, c)
            for row in res:
                print('|' + '|'.join(row) + '|\n')
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose, max_solutions=20)
