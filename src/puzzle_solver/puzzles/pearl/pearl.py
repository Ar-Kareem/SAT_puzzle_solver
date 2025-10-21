from collections import defaultdict

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Pos, get_all_pos, set_char, in_bounds, Direction, get_next_pos, get_char, get_opposite_direction
from puzzle_solver.core.utils_ortools import and_constraint, generic_solve_all, SingleSolution, force_connected_component


class Board:
    def __init__(self, board: np.ndarray):
        assert board.ndim == 2 and board.shape[0] > 0 and board.shape[1] > 0, f'board must be 2d, got {board.ndim}'
        assert all(i.item() in [' ', 'B', 'W'] for i in np.nditer(board)), f'board must be space, B, or W, got {list(np.nditer(board))}'
        self.V = board.shape[0]
        self.H = board.shape[1]
        self.board = board
        self.model = cp_model.CpModel()
        self.cell_active: dict[Pos, cp_model.IntVar] = {}
        self.cell_direction: dict[tuple[Pos, Direction], cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.cell_active[pos] = self.model.NewBoolVar(f"a[{pos}]")
            for direction in Direction:
                self.cell_direction[(pos, direction)] = self.model.NewBoolVar(f"b[{pos}]->({direction.name})")

    def add_all_constraints(self):
        self.force_direction_constraints()
        self.force_wb_constraints()
        self.force_connected_component()

    def force_wb_constraints(self):
        for pos in get_all_pos(self.V, self.H):
            c = get_char(self.board, pos)
            if c == 'B':
                # must be active
                self.model.Add(self.cell_active[pos] == 1)
                # black circle must be a corner not connected directly to another corner
                # must be a corner
                self.model.Add(self.cell_direction[(pos, Direction.UP)] != self.cell_direction[(pos, Direction.DOWN)])
                self.model.Add(self.cell_direction[(pos, Direction.LEFT)] != self.cell_direction[(pos, Direction.RIGHT)])
                # must not be connected directly to another corner
                for direction in Direction:
                    q = get_next_pos(pos, direction)
                    if not in_bounds(q, self.V, self.H):
                        continue
                    self.model.AddImplication(self.cell_direction[(pos, direction)], self.cell_direction[(q, direction)])
            elif c == 'W':
                # must be active
                self.model.Add(self.cell_active[pos] == 1)
                # white circle must be a straight which is connected to at least one corner
                # must be straight
                self.model.Add(self.cell_direction[(pos, Direction.UP)] == self.cell_direction[(pos, Direction.DOWN)])
                self.model.Add(self.cell_direction[(pos, Direction.LEFT)] == self.cell_direction[(pos, Direction.RIGHT)])
                # must be connected to at least one corner (i.e. UP-RIGHT or UP-LEFT or DOWN-RIGHT or DOWN-LEFT or RIGHT-UP or RIGHT-DOWN or LEFT-UP or LEFT-DOWN)
                aux_list: list[cp_model.IntVar] = []
                for direction in Direction:
                    q = get_next_pos(pos, direction)
                    if not in_bounds(q, self.V, self.H):
                        continue
                    ortho_directions = {Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT} - {direction, get_opposite_direction(direction)}
                    for ortho_direction in ortho_directions:
                        aux = self.model.NewBoolVar(f"A[{pos}]<-({q})")
                        and_constraint(self.model, target=aux, cs=[self.cell_direction[(q, ortho_direction)], self.cell_direction[(pos, direction)]])
                        aux_list.append(aux)
                self.model.Add(lxp.Sum(aux_list) >= 1)

    def force_direction_constraints(self):
        for pos in get_all_pos(self.V, self.H):
            # cell active means exactly 2 directions are active, cell not active means no directions are active
            s = sum([self.cell_direction[(pos, direction)] for direction in Direction])
            self.model.Add(s == 2).OnlyEnforceIf(self.cell_active[pos])
            self.model.Add(s == 0).OnlyEnforceIf(self.cell_active[pos].Not())
            # X having right means the cell to its right has left and so on for all directions
            for direction in Direction:
                q = get_next_pos(pos, direction)
                if in_bounds(q, self.V, self.H):
                    self.model.Add(self.cell_direction[(pos, direction)] == self.cell_direction[(q, get_opposite_direction(direction))])
                else:
                    self.model.Add(self.cell_direction[(pos, direction)] == 0)

    def force_connected_component(self):
        def is_neighbor(pd1: tuple[Pos, Direction], pd2: tuple[Pos, Direction]) -> bool:
            p1, d1 = pd1
            p2, d2 = pd2
            if p1 == p2 and d1 != d2:  # same position, different direction, is neighbor
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
            res = np.full((self.V, self.H), ' ', dtype=object)
            pretty_dict = {'DU': '┃ ', 'LR': '━━', 'DL': '━┒', 'DR': '┏━', 'RU': '┗━', 'LU': '━┛', '  ': '  '}
            for pos in get_all_pos(self.V, self.H):
                c = get_char(self.board, pos)
                c = single_res.assignment[pos]
                c = pretty_dict[c]
                set_char(res, pos, c)
            print(res)
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose, max_solutions=20)
