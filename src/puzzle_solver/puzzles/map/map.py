import json
from dataclasses import dataclass

from ortools.sat.python import cp_model

from puzzle_solver.core.utils_ortools import generic_solve_all


@dataclass(frozen=True)
class SingleSolution:
    assignment: dict[int, int]

    def get_hashable_solution(self) -> str:
        return json.dumps(self.assignment, sort_keys=True)


class Board:
    def __init__(self, regions: dict[int, set[int]], fixed_colors: dict[int, str]):
        self.regions = regions
        self.fixed_colors = fixed_colors
        self.N = len(regions)
        assert max(max(region) for region in regions.values() if region) == self.N - 1, 'region indices must be 0..N-1'
        assert set(fixed_colors.keys()).issubset(set(range(self.N))), 'fixed colors must be a subset of region indices'
        assert all(color in ['Y', 'R', 'G', 'B'] for color in fixed_colors.values()), 'fixed colors must be Y, R, G, or B'
        self.color_to_int = {c: i for i, c in enumerate(set(fixed_colors.values()))}
        self.int_to_color = {i: c for c, i in self.color_to_int.items()}

        self.model = cp_model.CpModel()
        self.model_vars: dict[int, cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for region_idx in self.regions.keys():
            self.model_vars[region_idx] = self.model.NewIntVar(0, 3, f'{region_idx}')

    def add_all_constraints(self):
        # fix given colors
        for region_idx, color in self.fixed_colors.items():
            self.model.Add(self.model_vars[region_idx] == self.color_to_int[color])
        # neighboring regions must have different colors
        for region_idx, region_connections in self.regions.items():
            for other_region_idx in region_connections:  # neighboring regions must have different colors
                self.model.Add(self.model_vars[region_idx] != self.model_vars[other_region_idx])

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[int, int] = {}
            for region_idx, var in board.model_vars.items():
                assignment[region_idx] = solver.Value(var)
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            print({k: self.int_to_color[v] for k, v in single_res.assignment.items()})
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
