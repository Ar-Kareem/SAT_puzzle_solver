import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, set_char, get_neighbors4, in_bounds, Direction, get_next_pos, get_char
from puzzle_solver.core.utils_ortools import and_constraint, or_constraint, generic_solve_all, SingleSolution, force_connected_component


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
        assert all(isinstance(i.item(), int) and i.item() >= -1 for i in np.nditer(clues)), f'clues must be -1 or >= 0, got {list(np.nditer(clues))}'
        self.V = clues.shape[0]
        self.H = clues.shape[1]
        self.clues = clues
        self.model = cp_model.CpModel()

        # Core vars
        self.b: dict[Pos, cp_model.IntVar] = {}  # 1=black, 0=white
        self.w: dict[Pos, cp_model.IntVar] = {}  # 1=white, 0=black

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        # Cell color vars
        for pos in get_all_pos(self.V, self.H):
            self.b[pos] = self.model.NewBoolVar(f"b[{pos}]")
            self.w[pos] = self.model.NewBoolVar(f"w[{pos}]")
            self.model.AddExactlyOne([self.b[pos], self.w[pos]])

    def add_all_constraints(self):
        self.no_adjacent_blacks()
        self.white_connectivity_percolation()
        self.range_clues()

    def no_adjacent_blacks(self):
        cache = set()
        for p in get_all_pos(self.V, self.H):
            for q in get_neighbors4(p, self.V, self.H):
                if (p, q) in cache:
                    continue
                cache.add((p, q))
                self.model.Add(self.b[p] + self.b[q] <= 1)


    def white_connectivity_percolation(self):
        force_connected_component(self.model, self.w)

    def range_clues(self):
        # For each numbered cell c with value k:
        #   - Force it white (cannot be black)
        #   - Build visibility chains in four directions (excluding the cell itself)
        #   - Sum of visible whites = 1 (itself) + sum(chains) == k
        for pos in get_all_pos(self.V, self.H):
            k = get_char(self.clues, pos)
            if k == -1:
                continue
            # Numbered cell must be white
            self.model.Add(self.b[pos] == 0)

            # Build visibility chains per direction (exclude self)
            vis_vars: list[cp_model.IntVar] = []
            for direction in Direction:
                ray = get_ray(pos, self.V, self.H, direction)  # cells outward
                if not ray:
                    continue
                # Chain: v0 = w[ray[0]]; vt = w[ray[t]] & vt-1
                prev = None
                for idx, cell in enumerate(ray):
                    v = self.model.NewBoolVar(f"vis[{pos}]->({direction.name})[{idx}]")
                    vis_vars.append(v)
                    if idx == 0:
                        # v0 == w[cell]
                        self.model.Add(v == self.w[cell])
                    else:
                        and_constraint(self.model, target=v, cs=[self.w[cell], prev])
                    prev = v

            # 1 (self) + sum(vis_vars) == k
            self.model.Add(1 + sum(vis_vars) == k)

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, int] = {}
            for pos, var in board.b.items():
                assignment[pos] = solver.Value(var)
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution:")
            res = np.full((self.V, self.H), ' ', dtype=object)
            for pos in get_all_pos(self.V, self.H):
                c = 'B' if single_res.assignment[pos] == 1 else ' '
                set_char(res, pos, c)
            print(res)
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
