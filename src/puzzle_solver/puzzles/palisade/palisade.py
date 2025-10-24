import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Pos, get_all_pos, get_neighbors4, id_board_to_wall_board, render_grid, set_char, get_char, get_neighbors8, in_bounds, get_next_pos, Direction
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution, force_connected_component


class Board:
    def __init__(self, board: np.array, region_size: int):
        assert region_size >= 1 and isinstance(region_size, int), 'region_size must be an integer greater than or equal to 1'
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all((c.item() == ' ') or str(c.item()).isdecimal() for c in np.nditer(board)), 'board must contain only space or digits'
        self.board = board
        self.V, self.H = board.shape
        self.region_size = region_size
        self.region_count = (self.V * self.H) // self.region_size
        assert self.region_count * self.region_size == self.V * self.H, f'region_size must be a factor of the board size, got {self.region_size} and {self.region_count}'

        self.model = cp_model.CpModel()
        self.pos_region_indicator: dict[tuple[Pos, int], cp_model.IntVar] = {}
        self.pos_val: dict[Pos, cp_model.IntVar] = {}
        self.walls: dict[frozenset[Pos], cp_model.IntVar] = {}
        self.roots: list[list[cp_model.IntVar]] = []  # for each region, for each pos, 1/0 if this pos is root of this region

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.pos_val[pos] = self.model.NewIntVar(0, self.region_count, f'{pos}')
            for region_idx in range(self.region_count):
                self.pos_region_indicator[(pos, region_idx)] = self.model.NewBoolVar(f'{pos}:{region_idx}')
            
            for direction in [Direction.RIGHT, Direction.DOWN]:
                next_pos = get_next_pos(pos, direction)
                if not in_bounds(next_pos, self.V, self.H):
                    continue
                self.walls[frozenset((pos, next_pos))] = self.model.NewBoolVar(f'{pos}:{next_pos}')

    def add_all_constraints(self):
        self.enforce_regions()  # sets up variables
        self.enforce_clues()  # enforces clues are correct
        self.enforce_connected_components()  # forces regions to be connected otherwise solutions will contain disconnected subgraphs that belong to the same region
        self.break_region_symmetry()  # forces regions to be in order to break symmetry
    
    def enforce_regions(self):
        # each pos belongs to exactly one region
        for pos in get_all_pos(self.V, self.H):
            self.model.AddExactlyOne([self.pos_region_indicator[(pos, region_idx)] for region_idx in range(self.region_count)])
        # region sizes are correct
        for region_idx in range(self.region_count):
            region_vars = [self.pos_region_indicator[(pos, region_idx)] for pos in get_all_pos(self.V, self.H)]
            self.model.Add(lxp.Sum(region_vars) == self.region_size)
        # setup pos val variables: pos val is equal to the region that is on
        for pos in get_all_pos(self.V, self.H):
            for region_idx in range(self.region_count):
                self.model.Add(self.pos_val[pos] == region_idx).OnlyEnforceIf(self.pos_region_indicator[(pos, region_idx)])
        # setup walls variable: walls is true if the two positions are different regions
        for (pos1, pos2), var in self.walls.items():
            self.model.Add(self.pos_val[pos1] != self.pos_val[pos2]).OnlyEnforceIf(var)
            self.model.Add(self.pos_val[pos1] == self.pos_val[pos2]).OnlyEnforceIf(var.Not())

    def enforce_clues(self):
        # the clue is how many neighbours are different than me (a border is an automatic +1)
        for pos in get_all_pos(self.V, self.H):
            c = get_char(self.board, pos)
            if not str(c).isdecimal():
                continue
            clue = int(c)
            wall_vars = [self.walls[frozenset((pos, n))] for n in get_neighbors4(pos, self.V, self.H)]
            border_count = 4 - len(wall_vars)
            self.model.Add(lxp.Sum(wall_vars) + border_count == clue)

    def enforce_connected_components(self):
        # each region is connected
        for region_idx in range(self.region_count):
            region_vars = {pos: self.pos_region_indicator[(pos, region_idx)] for pos in get_all_pos(self.V, self.H)}
            fc_vars = force_connected_component(self.model, region_vars)
            self.roots.append([fc_vars["is_root"][pos] for pos in get_all_pos(self.V, self.H)])

    def break_region_symmetry(self):
        assert len(self.roots) == self.region_count, f'expected {self.region_count} roots, got {len(self.roots)} (are you sure self.roots is initialized?)'
        # enforce strict root order to break symmetry
        for k in range(self.region_count - 1):
            lhs = sum(i * self.roots[k][i]     for i in range(self.V * self.H))  # index of root in region k
            rhs = sum(i * self.roots[k + 1][i] for i in range(self.V * self.H))  # index of root in region k+1
            self.model.Add(lhs < rhs)  # strictly before


    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, int] = {}
            for pos, var in board.pos_val.items():
                assignment[pos] = solver.Value(var)
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            id_board = np.full((self.V, self.H), ' ', dtype=object)
            for pos in get_all_pos(self.V, self.H):
                region_idx = single_res.assignment[pos]
                set_char(id_board, pos, region_idx)
            print('[')
            for row in id_board:
                print('       ', row.tolist(), end=',\n')
            print('    ])')
            print(render_grid(id_board_to_wall_board(id_board), center_char=self.board))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
