from collections import defaultdict
from typing import Optional

from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Pos, get_all_pos, get_pos, get_row_pos, get_col_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


def assert_input(lines: list[list[tuple[int, str]]]):
    for line in lines:
        for i,c in enumerate(line):
            if c == -1:
                continue
            elif isinstance(c, str):
                assert c[:-1].isdigit(), f'strings must begin with a digit, got {c}'
                line[i] = (int(c[:-1]), c[-1])
            elif isinstance(c, tuple):
                assert len(c) == 2 and isinstance(c[0], int) and isinstance(c[1], str), f'tuples must be (int, str), got {c}'
            else:
                raise ValueError(f'invalid cell value: {c}')


class Board:
    def __init__(self, top: list[list[tuple[int, str]]], side: list[list[tuple[int, str]]]):
        assert_input(top)
        assert_input(side)
        self.top = top
        self.side = side
        self.V = len(side)
        self.H = len(top)
        self.unique_colors = list(set([i[1] for line in top for i in line if i != -1] + [i[1] for line in side for i in line if i != -1]))
        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, dict[str, cp_model.IntVar]] = defaultdict(dict)
        self.extra_vars = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            for color in self.unique_colors:
                self.model_vars[pos][color] = self.model.NewBoolVar(f'{pos}:{color}')

    def add_all_constraints(self):
        for pos in get_all_pos(self.V, self.H):
            self.model.Add(lxp.sum(list(self.model_vars[pos].values())) <= 1)
        for i in range(self.V):
            ground_sequence = self.side[i]
            if tuple(ground_sequence) == (-1,):
                continue
            current_sequence = [self.model_vars[pos] for pos in get_row_pos(i, self.H)]
            self.constrain_nonogram_sequence(ground_sequence, current_sequence, f'ngm_side_{i}')
        for i in range(self.H):
            ground_sequence = self.top[i]
            if tuple(ground_sequence) == (-1,):
                continue
            current_sequence = [self.model_vars[pos] for pos in get_col_pos(i, self.V)]
            self.constrain_nonogram_sequence(ground_sequence, current_sequence, f'ngm_top_{i}')

    def constrain_nonogram_sequence(self, clues: list[tuple[int, str]], current_sequence: list[dict[str, cp_model.IntVar]], ns: str):
        """
        Constrain a colored sequence (current_sequence) to match the nonogram clues in clues.

        clues: e.g., [(3, 'R'), (1, 'G')] means: a run of 3 red ones, then a run of 1 green one. If two clues are next to each other and have the same color, they must be separated by at least one blank.
        current_sequence: list of dicts of IntVar in {0,1} for each color.

        steps:
        - Create start position s_i for each run i.
        - Enforce order and >=1 separation between runs.
        - Link each cell j to exactly one run interval (or none) via coverage booleans.
        - Force sum of ones to equal sum(clues).
        """
        L = len(current_sequence)
        R = len(clues)

        # Early infeasibility check:
        # Minimum required blanks equals number of adjacent pairs with same color.
        same_color_separators = sum(1 for (len_i, col_i), (len_j, col_j) in zip(clues, clues[1:]) if col_i == col_j)
        min_needed = sum(len_i for len_i, _ in clues) + same_color_separators
        if min_needed > L:
            print(f"Infeasible: clues {clues} need {min_needed} cells but line length is {L} for {ns}")
            self.model.Add(0 == 1)
            return

        # Collect the color set present in clues and in the line vars
        clue_colors = {c for _, c in clues}
        seq_colors = set()
        for j in range(L):
            seq_colors.update(current_sequence[j].keys())
        colors = sorted(clue_colors | seq_colors)

        # Start vars per run
        starts: list[cp_model.IntVar] = []
        self.extra_vars[f"{ns}_starts"] = starts
        for i in range(len(clues)):
            # s_i in [0, L] but we will bound by containment constraint below
            s = self.model.NewIntVar(0, L, f"{ns}_s[{i}]")
            starts.append(s)

        # Ordering + separation:
        # If same color: s[i+1] >= s[i] + len[i] + 1
        # If different color: s[i+1] >= s[i] + len[i]
        for i in range(R - 1):
            len_i, col_i = clues[i]
            _, col_next = clues[i + 1]
            gap = 1 if col_i == col_next else 0
            self.model.Add(starts[i + 1] >= starts[i] + len_i + gap)

        # Containment: s[i] + len[i] <= L
        for i, (run_len, _) in enumerate(clues):
            self.model.Add(starts[i] + run_len <= L)

        # Coverage booleans: cover[i][j] <=> (starts[i] <= j) AND (j < starts[i] + run_len)
        cover = [[None] * L for _ in range(R)]
        list_b_le = [[None] * L for _ in range(R)]
        list_b_lt_end = [[None] * L for _ in range(R)]
        self.extra_vars[f"{ns}_cover"] = cover
        self.extra_vars[f"{ns}_list_b_le"] = list_b_le
        self.extra_vars[f"{ns}_list_b_lt_end"] = list_b_lt_end

        for i, (run_len, _) in enumerate(clues):
            s_i = starts[i]
            for j in range(L):
                b_le = self.model.NewBoolVar(f"{ns}_le[{i},{j}]")  # s_i <= j
                self.model.Add(s_i <= j).OnlyEnforceIf(b_le)
                self.model.Add(s_i >= j + 1).OnlyEnforceIf(b_le.Not())

                b_lt_end = self.model.NewBoolVar(f"{ns}_lt_end[{i},{j}]")  # j < s_i + run_len  <=>  s_i + run_len - 1 >= j
                end_expr = s_i + run_len - 1
                self.model.Add(end_expr >= j).OnlyEnforceIf(b_lt_end)
                self.model.Add(end_expr <= j - 1).OnlyEnforceIf(b_lt_end.Not())

                b_cov = self.model.NewBoolVar(f"{ns}_cov[{i},{j}]")
                self.model.AddBoolAnd([b_le, b_lt_end]).OnlyEnforceIf(b_cov)
                self.model.AddBoolOr([b_cov, b_le.Not(), b_lt_end.Not()])

                cover[i][j] = b_cov
                list_b_le[i][j] = b_le
                list_b_lt_end[i][j] = b_lt_end

        # Link coverage to per-cell, per-color variables.
        # For each color k and cell j:
        #   sum_{i: color_i == k} cover[i][j] == current_sequence[j][k]
        # Also tie the total cover at j to the sum over all colors at j:
        #   sum_i cover[i][j] == sum_k current_sequence[j][k]
        # This enforces that at most one color is active per cell (since the LHS is in {0,1} due to non-overlap).
        # If a color var is missing in current_sequence[j], assume it’s an implicit 0 by creating a fixed zero var.
        # (Alternatively, require the caller to provide all colors per cell.)
        zero_cache = {}
        def get_zero(name: str):
            if name not in zero_cache:
                z = self.model.NewConstant(0)
                zero_cache[name] = z
            return zero_cache[name]

        # Pre-index runs by color for efficiency
        runs_by_color = {k: [] for k in colors}
        for i, (_, k) in enumerate(clues):
            runs_by_color[k].append(i)

        for j in range(L):
            # Total coverage at cell j
            total_cov_j = sum(cover[i][j] for i in range(R)) if R > 0 else 0

            # Sum of color vars at cell j
            color_vars_j = []
            for k in colors:
                v = current_sequence[j].get(k, None)
                if v is None:
                    v = get_zero(f"{ns}_zero_{k}")
                color_vars_j.append(v)

                # Per-color coverage equality
                if runs_by_color[k]:
                    self.model.Add(sum(cover[i][j] for i in runs_by_color[k]) == v)
                else:
                    # No runs of this color -> force cell color var to 0
                    self.model.Add(v == 0)

            # Tie total coverage to sum of color vars (blank vs exactly-one color)
            if R > 0:
                self.model.Add(total_cov_j == sum(color_vars_j))
            else:
                # No runs at all: all cells must be blank across all colors
                for v in color_vars_j:
                    self.model.Add(v == 0)

        # Optional but strong propagation: per-color totals must match total clue lengths of that color
        total_len_by_color = {k: 0 for k in colors}
        for length, k in clues:
            total_len_by_color[k] += length

        for k in colors:
            total_cells_k = sum(current_sequence[j].get(k, get_zero(f"{ns}_zero_{k}")) for j in range(L))
            self.model.Add(total_cells_k == total_len_by_color[k])

    def solve_and_print(self, verbose: bool = True, visualize_colors: Optional[dict[str, str]] = None):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: color for pos, d in board.model_vars.items() for color, var in d.items() if solver.value(var) == 1})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H, center_char=lambda r, c: single_res.assignment.get(get_pos(x=c, y=r), ' ')))
            if visualize_colors is not None:
                from matplotlib import pyplot as plt
                from matplotlib.colors import ListedColormap
                visualize_colors[' '] = 'black'
                visualize_colors_keys = list(visualize_colors.keys())
                char_to_int = {c: i for i, c in enumerate(visualize_colors_keys)}
                nums = [[char_to_int[single_res.assignment.get(get_pos(x=c, y=r), ' ')] for c in range(self.H)] for r in range(self.V)]
                plt.imshow(nums,
                        aspect='equal',
                        cmap=ListedColormap([visualize_colors[c] for c in visualize_colors_keys]),
                        extent=[0, self.H, self.V, 0])
                plt.colorbar()
                # plt.grid(True)
                plt.show()
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
