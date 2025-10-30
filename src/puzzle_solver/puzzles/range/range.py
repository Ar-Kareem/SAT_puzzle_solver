import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_pos, get_neighbors4, in_bounds, Direction, get_next_pos, get_char
from puzzle_solver.core.utils_ortools import and_constraint, generic_solve_all, SingleSolution, force_connected_component
from puzzle_solver.core.utils_visualizer import combined_function


def get_ray(pos: Pos, V: int, H: int, direction: Direction) -> list[Pos]:
    out = []
    while True:
        pos = get_next_pos(pos, direction)
        if not in_bounds(pos, V, H):
            break
        out.append(pos)
    return out


class Board:
    def __init__(self, clues: np.ndarray):
        assert clues.ndim == 2 and clues.shape[0] > 0 and clues.shape[1] > 0, f'clues must be 2d, got {clues.ndim}'
        assert all(str(i.item()).strip() == '' or str(i.item()).strip().isdecimal() for i in np.nditer(clues)), f'clues must be empty or a decimal number, got {list(np.nditer(clues))}'
        self.V, self.H = clues.shape
        self.clues = clues

        self.model = cp_model.CpModel()
        self.b: dict[Pos, cp_model.IntVar] = {}
        self.w: dict[Pos, cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.b[pos] = self.model.NewBoolVar(f"b[{pos}]")
            self.w[pos] = self.b[pos].Not()

    def add_all_constraints(self):
        self.no_adjacent_blacks()
        self.range_clues()
        force_connected_component(self.model, self.w)

    def no_adjacent_blacks(self):
        for p in get_all_pos(self.V, self.H):
            for q in get_neighbors4(p, self.V, self.H):
                self.model.Add(self.b[p] + self.b[q] <= 1)

    def range_clues(self):
        for pos in get_all_pos(self.V, self.H):  # For each numbered cell c with value k
            k = str(get_char(self.clues, pos)).strip()
            if not k:
                continue
            self.model.Add(self.w[pos] == 1)  # Force it white
            vis_vars: list[cp_model.IntVar] = []
            for direction in Direction:  # Build visibility chains in four direction
                ray = get_ray(pos, self.V, self.H, direction)  # cells outward
                for idx in range(len(ray)):
                    v = self.model.NewBoolVar(f"vis[{pos}]->({direction.name})[{idx}]")
                    and_constraint(self.model, target=v, cs=[self.w[p] for p in ray[:idx+1]])
                    vis_vars.append(v)
            self.model.Add(1 + sum(vis_vars) == int(k))  # Sum of visible whites = 1 (itself) + sum(chains) == k

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: solver.Value(board.b[pos]) for pos in get_all_pos(board.V, board.H)})
        def callback(single_res: SingleSolution):
            print("Solution:")
            print(combined_function(self.V, self.H, is_shaded=lambda r, c: single_res.assignment[get_pos(x=c, y=r)] == 1, center_char=lambda r, c: self.clues[r, c].strip(), text_on_shaded_cells=False))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
