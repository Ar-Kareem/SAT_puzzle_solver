from collections import defaultdict

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from core.utils import Pos, get_all_pos, set_char, in_bounds, Direction, get_next_pos, get_char, get_opposite_direction
from core.utils_ortools import and_constraint, or_constraint, generic_solve_all, SingleSolution


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
        self.reach_layers: list[dict[Pos, cp_model.IntVar]] = []  # R_t[p] booleans, t = 0..T

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.cell_active[pos] = self.model.NewBoolVar(f"a[{pos}]")
            for direction in Direction:
                self.cell_direction[(pos, direction)] = self.model.NewBoolVar(f"b[{pos}]->({direction.name})")
        # Percolation layers R_t (monotone flood fill)
        T = self.V * self.H  # large enough to cover whole board
        for t in range(T + 1):
            Rt: dict[Pos, cp_model.IntVar] = {}
            for pos in get_all_pos(self.V, self.H):
                Rt[pos] = self.model.NewBoolVar(f"R[{t}][{pos}]")
            self.reach_layers.append(Rt)

    def add_all_constraints(self):
        self.force_direction_constraints()
        self.force_wb_constraints()
        self.connectivity_percolation()

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

    def connectivity_percolation(self):
        """
        Layered percolation:
            - root is exactly the first cell
            - R_t is monotone nondecreasing in t (R_t+1 >= R_t)
            - A cell can 'turn on' at layer t+1 iff has a neighbor on at layer t and the neighbor is pointing to it (or is root)
            - Final layer is all connected
        """
        # Seed: R0 = root
        for i, pos in enumerate(get_all_pos(self.V, self.H)):
            if i == 0:
                self.model.Add(self.reach_layers[0][pos] == 1)  # first cell is root
            else:
                self.model.Add(self.reach_layers[0][pos] == 0)

        for t in range(1, len(self.reach_layers)):
            Rt_prev = self.reach_layers[t - 1]
            Rt = self.reach_layers[t]
            for p in get_all_pos(self.V, self.H):
                # Rt[p] = Rt_prev[p] | (white[p] & Rt_prev[neighbour #1]) | (white[p] & Rt_prev[neighbour #2]) | ...
                # Create helper (white[p] & Rt_prev[neighbour #X]) for each neighbor q
                neigh_helpers: list[cp_model.IntVar] = []
                for direction in Direction:
                    q = get_next_pos(p, direction)
                    if not in_bounds(q, self.V, self.H):
                        continue
                    a = self.model.NewBoolVar(f"A[{t}][{p}]<-({q})")
                    and_constraint(self.model, target=a, cs=[Rt_prev[q], self.cell_direction[(q, get_opposite_direction(direction))]])
                    neigh_helpers.append(a)
                or_constraint(self.model, target=Rt[p], cs=[Rt_prev[p]] + neigh_helpers)

        # every pearl must be reached by the final layer
        for p in get_all_pos(self.V, self.H):
            self.model.Add(self.reach_layers[-1][p] == 1).OnlyEnforceIf(self.cell_active[p])


    def solve_and_print(self):
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
        return generic_solve_all(self, board_to_solution, callback=callback, max_solutions=20)
