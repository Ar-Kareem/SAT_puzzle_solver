from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_pos, get_row_pos, get_col_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


def constrain_nonogram_sequence(model: cp_model.CpModel, clues: list[int], current_sequence: list[cp_model.IntVar], ns: str):
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
        model.Add(0 == 1)
        return

    result = {}
    # Start variables for each run. This is the most critical variable for the problem.
    starts = []
    result[f"{ns}_starts"] = starts
    for i in range(len(clues)):
        s = model.NewIntVar(0, L, f"{ns}_s[{i}]")
        starts.append(s)
    # Enforce order and >=1 blank between consecutive runs.
    for i in range(len(clues) - 1):
        model.Add(starts[i + 1] >= starts[i] + clues[i] + 1)
    # enforce that every run is fully contained in the board
    for i in range(len(clues)):
        model.Add(starts[i] + clues[i] <= L)

    # For each cell j, create booleans cover[i][j] that indicate
    # whether run i covers cell j:  (starts[i] <= j) AND (j < starts[i] + clues[i])
    cover = [[None] * L for _ in range(len(clues))]
    list_b_le = [[None] * L for _ in range(len(clues))]
    list_b_lt_end = [[None] * L for _ in range(len(clues))]
    result[f"{ns}_cover"] = cover
    result[f"{ns}_list_b_le"] = list_b_le
    result[f"{ns}_list_b_lt_end"] = list_b_lt_end

    for i, c in enumerate(clues):
        s_i = starts[i]
        for j in range(L):
            # b_le: s_i <= j [is start[i] <= j]
            b_le = model.NewBoolVar(f"{ns}_le[{i},{j}]")
            model.Add(s_i <= j).OnlyEnforceIf(b_le)
            model.Add(s_i >= j + 1).OnlyEnforceIf(b_le.Not())

            # b_lt_end: j < s_i + c  ⇔  s_i + c - 1 >= j [is start[i] + clues[i] - 1 (aka end[i]) >= j]
            b_lt_end = model.NewBoolVar(f"{ns}_lt_end[{i},{j}]")
            end_expr = s_i + c - 1
            model.Add(end_expr >= j).OnlyEnforceIf(b_lt_end)
            model.Add(end_expr <= j - 1).OnlyEnforceIf(b_lt_end.Not())  # (s_i + c - 1) < j

            b_cov = model.NewBoolVar(f"{ns}_cov[{i},{j}]")
            # If covered ⇒ both comparisons true
            model.AddBoolAnd([b_le, b_lt_end]).OnlyEnforceIf(b_cov)
            # If both comparisons true ⇒ covered
            model.AddBoolOr([b_cov, b_le.Not(), b_lt_end.Not()])
            cover[i][j] = b_cov
            list_b_le[i][j] = b_le
            list_b_lt_end[i][j] = b_lt_end

    # Each cell j is 1 iff it is covered by exactly one run.
    # (Because runs are separated by >=1 zero, these coverage intervals cannot overlap,
    for j in range(L):
        model.Add(sum(cover[i][j] for i in range(len(clues))) == current_sequence[j])


class Board:
    def __init__(self, top: list[list[int]], side: list[list[int]]):
        assert all(isinstance(i, int) for line in top for i in line), 'top must be a list of lists of integers'
        assert all(isinstance(i, int) for line in side for i in line), 'side must be a list of lists of integers'
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
            constrain_nonogram_sequence(self.model, ground_sequence, current_sequence, f'ngm_side_{i}')
        for i in range(self.H):
            ground_sequence = self.top[i]
            if ground_sequence == -1:
                continue
            current_sequence = [self.model_vars[pos] for pos in get_col_pos(i, self.V)]
            constrain_nonogram_sequence(self.model, ground_sequence, current_sequence, f'ngm_top_{i}')

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: solver.value(var) for pos, var in board.model_vars.items()})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H, is_shaded=lambda r, c: single_res.assignment[get_pos(x=c, y=r)]))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
