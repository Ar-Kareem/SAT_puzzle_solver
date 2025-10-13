import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Optional, Callable
from dataclasses import dataclass

import numpy as np
from numpy.core.defchararray import isdecimal
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp
from ortools.sat.python.cp_model import CpSolverSolutionCallback

sys.path.append(str(Path(__file__).parent.parent))
from core.utils import Pos, get_pos, get_all_pos, set_char, SingleSolution, get_hashable_solution


class AllSolutionsCollector(CpSolverSolutionCallback):
    def __init__(self, board: 'Board', out: List[SingleSolution], max_solutions: Optional[int] = None, callback: Optional[Callable[[SingleSolution], None]] = None):
        super().__init__()
        self.out = out
        self.unique_solutions = set()
        self.max_solutions = max_solutions
        self.callback = callback
        self.vars_by_pos: Dict[Pos, cp_model.IntVar] = board.model_vars.copy()

    def on_solution_callback(self):
        try:
            assignment: Dict[Pos, int] = {}
            for pos, var in self.vars_by_pos.items():
                assignment[pos] = self.value(var)
            result = SingleSolution(assignment=assignment)
            result_json = get_hashable_solution(result)
            if result_json in self.unique_solutions:
                return
            self.unique_solutions.add(result_json)
            self.out.append(result)
            if self.callback is not None:
                self.callback(result)
            if self.max_solutions is not None and len(self.out) >= self.max_solutions:
                self.StopSearch()
        except Exception as e:
            print(e)
            raise e


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
            current_sequence = [self.model_vars[get_pos(x=x, y=i)] for x in range(self.H)]
            self.constrain_nonogram_sequence(ground_sequence, current_sequence, f'ngm_side_{i}')
        for i in range(self.H):
            ground_sequence = self.top[i]
            if ground_sequence == -1:
                continue
            current_sequence = [self.model_vars[get_pos(x=i, y=y)] for y in range(self.V)]
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

    def solve_all(self, max_solutions: Optional[int] = None, callback: Optional[Callable[[SingleSolution], None]] = None) -> List[SingleSolution]:
        solver = cp_model.CpSolver()
        solver.parameters.enumerate_all_solutions = True
        solutions: List[SingleSolution] = []
        collector = AllSolutionsCollector(self, solutions, max_solutions=max_solutions, callback=callback)
        tic = time.time()
        solver.solve(self.model, collector)
        print("Solutions found:", len(solutions))
        print("status:", solver.StatusName())
        toc = time.time()
        print(f"Time taken: {toc - tic:.2f} seconds")
        return solutions

    def solve_and_print(self):
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = [[None] * self.H for _ in range(self.V)]
            for pos in get_all_pos(self.V, self.H):
                c = 'B ' if single_res.assignment[pos] == 1 else '. '
                set_char(res, pos, c)
            for row in res:
                print(''.join(row))
        return self.solve_all(callback=callback)
