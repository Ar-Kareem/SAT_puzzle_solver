import numpy as np
from collections import defaultdict
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, set_char, Direction, get_row_pos, get_col_pos, get_next_pos, in_bounds, get_opposite_direction
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution, force_connected_component
from puzzle_solver.core.utils_visualizer import render_grid


CellBorder = tuple[Pos, Direction]
Corner = Pos


class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all(c.item() == ' ' or str(c.item()).isdecimal() for c in np.nditer(board)), 'board must contain only spaces or digits'
        self.V = board.shape[0]
        self.H = board.shape[1]
        self.board = board
        self.cell_borders_to_corners: dict[CellBorder, set[Corner]] = defaultdict(set)  # for every cell border, a set of all corners it is connected to
        self.corners_to_cell_borders: dict[Corner, set[CellBorder]] = defaultdict(set)  # opposite direction

        # 2N^2 + 2N edges
        # 4*edges (fully connected component)
        # model variables = edges (on/off) + 4*edges (fully connected component)
        # = 9N^2 + 9N
        self.model = cp_model.CpModel()
        self.model_vars: dict[CellBorder, cp_model.IntVar] = {}  # one entry for every unique variable in the model
        self.cell_borders: dict[CellBorder, cp_model.IntVar] = {}  # for every position and direction, one entry for that edge (thus the same edge variables are used in opposite directions of neighboring cells)
        self.corner_vars: dict[Corner, set[cp_model.IntVar]] = defaultdict(set)  # for every corner, one entry for each edge that touches the corner (i.e. 4 per corner unless on the border)

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            for direction in [Direction.RIGHT, Direction.DOWN]:
                self.add_var(pos, direction)
        for pos in get_row_pos(0, self.H):
            self.add_var(pos, Direction.UP)
        for pos in get_col_pos(0, self.V):
            self.add_var(pos, Direction.LEFT)

    def add_var(self, pos: Pos, direction: Direction):
        cell_border = (pos, direction)
        v = self.model.NewBoolVar(f'main:{cell_border}')
        self.model_vars[cell_border] = v
        self.add_cell_border_var(cell_border, v)
        self.add_corner_vars(cell_border, v)

    def add_cell_border_var(self, cell_border: CellBorder, var: cp_model.IntVar):
        """An edge belongs to two cells unless its on the border in which case it only belongs to one."""
        pos, direction = cell_border
        self.cell_borders[cell_border] = var
        next_pos = get_next_pos(pos, direction)
        if in_bounds(next_pos, self.V, self.H):
            self.cell_borders[(next_pos, get_opposite_direction(direction))] = var
    
    def add_corner_vars(self, cell_border: CellBorder, var: cp_model.IntVar):
        """
        An edge always belongs to two corners. Note that the cell xi,yi has the 4 corners (xi,yi), (xi+1,yi), (xi,yi+1), (xi+1,yi+1). (memorize these 4 coordinates or the function wont make sense)
        Thus corner index is +1 of board coordinates.
        Never check for bounds here because an edge ALWAYS touches two corners AND because the +1 will make in_bounds return False when its still in bounds.
        """
        pos, direction = cell_border
        if direction == Direction.LEFT:  # it touches me and (xi,yi+1)
            corner1 = pos
            corner2 = get_next_pos(pos, Direction.DOWN)
        elif direction == Direction.UP:  # it touches me and (xi+1,yi)
            corner1 = pos
            corner2 = get_next_pos(pos, Direction.RIGHT)
        elif direction == Direction.RIGHT:  # it touches (xi+1,yi) and (xi+1,yi+1)
            corner1 = get_next_pos(pos, Direction.RIGHT)
            corner2 = get_next_pos(corner1, Direction.DOWN)
        elif direction == Direction.DOWN:  # it touches (xi,yi+1) and (xi+1,yi+1)
            corner1 = get_next_pos(pos, Direction.DOWN)
            corner2 = get_next_pos(corner1, Direction.RIGHT)
        else:
            raise ValueError(f'Invalid direction: {direction}')
        self.corner_vars[corner1].add(var)
        self.corner_vars[corner2].add(var)
        self.cell_borders_to_corners[cell_border].add(corner1)
        self.cell_borders_to_corners[cell_border].add(corner2)
        self.corners_to_cell_borders[corner1].add(cell_border)
        self.corners_to_cell_borders[corner2].add(cell_border)

    def add_all_constraints(self):
        for pos in get_all_pos(self.V, self.H):  # enforce cells with numbers
            variables = [self.cell_borders[(pos, direction)] for direction in Direction if (pos, direction) in self.cell_borders]
            val = get_char(self.board, pos)
            if not val.isdecimal():
                continue
            self.model.Add(sum(variables) == int(val))

        corner_sum_domain = cp_model.Domain.FromValues([0, 2])  # sum of edges touching a corner is 0 or 2
        for corner in self.corner_vars:  # a corder always has 0 or 2 active edges
            self.model.AddLinearExpressionInDomain(sum(self.corner_vars[corner]), corner_sum_domain)

        # single connected component
        def is_neighbor(cb1: CellBorder, cb2: CellBorder) -> bool:
            cb1_corners = self.cell_borders_to_corners[cb1]
            cb2_corners = self.cell_borders_to_corners[cb2]
            return len(cb1_corners & cb2_corners) > 0
        force_connected_component(self.model, self.model_vars, is_neighbor=is_neighbor)




    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, str] = {}
            for (pos, direction), var in board.model_vars.items():
                if solver.value(var) == 1:
                    if pos not in assignment:
                        assignment[pos] = ''
                    assignment[pos] += direction.name[0]
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.full((self.V, self.H), ' ', dtype=object)
            for pos in get_all_pos(self.V, self.H):
                if pos not in single_res.assignment:
                    continue
                c = ''.join(sorted(single_res.assignment[pos]))
                set_char(res, pos, c)
            # replace " " with "·"
            board = np.where(self.board == ' ', '·', self.board)
            print(render_grid(cell_flags=res, center_char=board))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose, max_solutions=999)
