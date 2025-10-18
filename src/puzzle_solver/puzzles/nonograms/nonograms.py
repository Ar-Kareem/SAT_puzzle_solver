import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, set_char, get_row_pos, get_col_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution


class Board:
    def __init__(self, top: list[list[int]], side: list[list[int]]):
        assert all(isinstance(i, int) for l in top for i in l), 'top must be a list of lists of integers'
        assert all(isinstance(i, int) for l in side for i in l), 'side must be a list of lists of integers'
        self.top = top
        self.side = side
        self.V = len(side)
        self.H = len(top)
        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}
        self.extra_vars = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[pos] = self.model.NewBoolVar(f'{pos}')

    def add_all_constraints(self):
        for i in range(self.V):
            ground_sequence = self.side[i]
            if ground_sequence == -1:
                continue
            current_sequence = [self.model_vars[pos] for pos in get_row_pos(i, self.H)]
            self.constrain_nonogram_sequence(ground_sequence, current_sequence, f'ngm_side_{i}')
        for i in range(self.H):
            ground_sequence = self.top[i]
            if ground_sequence == -1:
                continue
            current_sequence = [self.model_vars[pos] for pos in get_col_pos(i, self.V)]
            self.constrain_nonogram_sequence(ground_sequence, current_sequence, f'ngm_top_{i}')

    def constrain_nonogram_sequence(self, clues: list[int], current_sequence: list[cp_model.IntVar], ns: str):
        """
        Constrain a binary sequence (current_sequence) to match the nonogram clues in clues.

        clues: e.g., [3,1] means: a run of 3 ones, >=1 zero, then a run of 1 one.
        current_sequence: list of IntVar in {0,1}.
        extra_vars: dict for storing helper vars safely across multiple calls.

        steps:
        - Create start position s_i for each run i.
        - Enforce order and >=1 separation between runs.
        - Link each cell j to exactly one run interval (or none) via coverage booleans.
        - Force sum of ones to equal sum(clues).
        """
        L = len(current_sequence)

        # not needed but useful for debugging: any clue longer than the line ⇒ unsat.
        if sum(clues) + len(clues) - 1 > L:
            print(f"Infeasible: clue {clues} longer than line length {L} for {ns}")
            self.model.Add(0 == 1)
            return

        # Start variables for each run. This is the most critical variable for the problem.
        starts = []
        self.extra_vars[f"{ns}_starts"] = starts
        for i, c in enumerate(clues):
            s = self.model.NewIntVar(0, L, f"{ns}_s[{i}]")
            starts.append(s)
        # Enforce order and >=1 blank between consecutive runs.
        for i in range(len(clues) - 1):
            self.model.Add(starts[i + 1] >= starts[i] + clues[i] + 1)
        # enforce that every run is fully contained in the board
        for i in range(len(clues)):
            self.model.Add(starts[i] + clues[i] <= L)

        # For each cell j, create booleans cover[i][j] that indicate
        # whether run i covers cell j:  (starts[i] <= j) AND (j < starts[i] + clues[i])
        cover = [[None] * L for _ in range(len(clues))]
        list_b_le = [[None] * L for _ in range(len(clues))]
        list_b_lt_end = [[None] * L for _ in range(len(clues))]
        self.extra_vars[f"{ns}_cover"] = cover
        self.extra_vars[f"{ns}_list_b_le"] = list_b_le
        self.extra_vars[f"{ns}_list_b_lt_end"] = list_b_lt_end

        for i, c in enumerate(clues):
            s_i = starts[i]
            for j in range(L):
                # b_le: s_i <= j [is start[i] <= j]
                b_le = self.model.NewBoolVar(f"{ns}_le[{i},{j}]")
                self.model.Add(s_i <= j).OnlyEnforceIf(b_le)
                self.model.Add(s_i >= j + 1).OnlyEnforceIf(b_le.Not())

                # b_lt_end: j < s_i + c  ⇔  s_i + c - 1 >= j [is start[i] + clues[i] - 1 (aka end[i]) >= j]
                b_lt_end = self.model.NewBoolVar(f"{ns}_lt_end[{i},{j}]")
                end_expr = s_i + c - 1
                self.model.Add(end_expr >= j).OnlyEnforceIf(b_lt_end)
                self.model.Add(end_expr <= j - 1).OnlyEnforceIf(b_lt_end.Not())  # (s_i + c - 1) < j

                b_cov = self.model.NewBoolVar(f"{ns}_cov[{i},{j}]")
                # If covered ⇒ both comparisons true
                self.model.AddBoolAnd([b_le, b_lt_end]).OnlyEnforceIf(b_cov)
                # If both comparisons true ⇒ covered
                self.model.AddBoolOr([b_cov, b_le.Not(), b_lt_end.Not()])
                cover[i][j] = b_cov
                list_b_le[i][j] = b_le
                list_b_lt_end[i][j] = b_lt_end

        # Each cell j is 1 iff it is covered by exactly one run.
        # (Because runs are separated by >=1 zero, these coverage intervals cannot overlap,
        for j in range(L):
            self.model.Add(sum(cover[i][j] for i in range(len(clues))) == current_sequence[j])

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, int] = {}
            for pos, var in board.model_vars.items():
                assignment[pos] = solver.value(var)
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.full((self.V, self.H), ' ', dtype=object)
            for pos in get_all_pos(self.V, self.H):
                c = 'B' if single_res.assignment[pos] == 1 else ' '
                set_char(res, pos, c)
            print(res)
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
