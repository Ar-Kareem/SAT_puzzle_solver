import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, set_char, get_neighbors4, get_all_pos_to_idx_dict, get_row_pos, get_col_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution, and_constraint, or_constraint


class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert board.shape[0] == board.shape[1], 'board must be square'
        self.board = board
        self.V = board.shape[0]
        self.H = board.shape[1]
        self.N = self.V * self.H
        self.idx_of: dict[Pos, int] = get_all_pos_to_idx_dict(self.V, self.H)

        self.model = cp_model.CpModel()
        self.B = {} # black squares
        self.Num = {} # value of squares (Num = N + idx if black, else board[pos])
        # Connectivity helpers
        self.root: dict[Pos, cp_model.IntVar] = {}       # exactly one root; root <= w
        self.reach_layers: list[dict[Pos, cp_model.IntVar]] = []  # R_t[p] booleans, t = 0..T

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.B[pos] = self.model.NewBoolVar(f'{pos}')
            self.Num[pos] = self.model.NewIntVar(0, 2*self.N, f'{pos}')
            self.model.Add(self.Num[pos] == self.N + self.idx_of[pos]).OnlyEnforceIf(self.B[pos])
            self.model.Add(self.Num[pos] == int(get_char(self.board, pos))).OnlyEnforceIf(self.B[pos].Not())
        # Root
        for pos in get_all_pos(self.V, self.H):
            self.root[pos] = self.model.NewBoolVar(f"root[{pos}]")
        # Percolation layers R_t (monotone flood fill)
        for t in range(self.N + 1):
            Rt: dict[Pos, cp_model.IntVar] = {}
            for pos in get_all_pos(self.V, self.H):
                Rt[pos] = self.model.NewBoolVar(f"R[{t}][{pos}]")
            self.reach_layers.append(Rt)

    def add_all_constraints(self):
        self.no_adjacent_blacks()
        self.no_number_appears_twice()
        self.white_connectivity_percolation()

    def no_adjacent_blacks(self):
        # no two black squares are adjacent 
        for pos in get_all_pos(self.V, self.H):
            for neighbor in get_neighbors4(pos, self.V, self.H):
                self.model.Add(self.B[pos] + self.B[neighbor] <= 1)

    def no_number_appears_twice(self):
        # no number appears twice in any row or column (numbers are ignored if black)
        for row in range(self.V):
            var_list = [self.Num[pos] for pos in get_row_pos(row, self.H)]
            self.model.AddAllDifferent(var_list)
        for col in range(self.H):
            var_list = [self.Num[pos] for pos in get_col_pos(col, self.V)]
            self.model.AddAllDifferent(var_list)

    def white_connectivity_percolation(self):
        """
        Layered percolation:
          - root is exactly the first white cell
          - R_t is monotone nondecreasing in t (R_t+1 >= R_t)
          - A cell can 'turn on' at layer t+1 iff it's white and has a neighbor on at layer t (or is root)
          - Final layer is equal to the white mask: R_T[p] == w[p]  => all whites are connected to the unique root
        """
        # to find unique solutions easily, we make only 1 possible root allowed; root is exactly the first white cell
        prev_cells_black: list[cp_model.IntVar] = []
        for pos in get_all_pos(self.V, self.H):
            and_constraint(self.model, target=self.root[pos], cs=[self.B[pos].Not()] + prev_cells_black)
            prev_cells_black.append(self.B[pos])

        # Seed: R0 = root
        for pos in get_all_pos(self.V, self.H):
            self.model.Add(self.reach_layers[0][pos] == self.root[pos])

        T = len(self.reach_layers)
        for t in range(1, T):
            Rt_prev = self.reach_layers[t - 1]
            Rt = self.reach_layers[t]
            for p in get_all_pos(self.V, self.H):
                # Rt[p] = Rt_prev[p] | (white[p] & Rt_prev[neighbour #1]) | (white[p] & Rt_prev[neighbour #2]) | ...
                # Create helper (white[p] & Rt_prev[neighbour #X]) for each neighbor q
                neigh_helpers: list[cp_model.IntVar] = []
                for q in get_neighbors4(p, self.V, self.H):
                    a = self.model.NewBoolVar(f"A[{t}][{p}]<-({q})")
                    and_constraint(self.model, target=a, cs=[self.B[p].Not(), Rt_prev[q]])
                    neigh_helpers.append(a)
                or_constraint(self.model, target=Rt[p], cs=[Rt_prev[p]] + neigh_helpers)

        # All whites must be reached by the final layer
        RT = self.reach_layers[T - 1]
        for p in get_all_pos(self.V, self.H):
            self.model.Add(RT[p] == self.B[p].Not())


    def solve_and_print(self):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, int] = {}
            for pos, var in board.B.items():
                assignment[pos] = solver.value(var)
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.full((self.V, self.H), ' ', dtype=object)
            for pos in get_all_pos(self.V, self.H):
                c = get_char(self.board, pos)
                c = 'B' if single_res.assignment[pos] == 1 else ' '
                set_char(res, pos, c)
            print(res)
        return generic_solve_all(self, board_to_solution, callback=callback)
