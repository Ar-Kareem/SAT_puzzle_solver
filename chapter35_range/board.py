import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import CpSolverSolutionCallback

sys.path.append(str(Path(__file__).parent.parent))
from core.utils import Pos, get_all_pos, set_char, get_pos, get_neighbors4
from core.utils_ortools import and_constraint, or_constraint


@dataclass(frozen=True)
class SingleSolution:
    assignment: dict[Pos, int]  # 1 = black, 0 = white


def get_ray(pos: Pos, V: int, H: int, dx: int, dy: int) -> List[Pos]:
    out = []
    x, y = pos.x + dx, pos.y + dy
    while 0 <= y < V and 0 <= x < H:
        out.append(get_pos(x=x, y=y))
        x += dx
        y += dy
    return out


class AllSolutionsCollector(CpSolverSolutionCallback):
    def __init__(self, board: 'Board', out: List[SingleSolution], max_solutions: Optional[int] = None, callback: Optional[Callable[[SingleSolution], None]] = None):
        super().__init__()
        self.out = out
        self.unique = set()
        self.max_solutions = max_solutions
        self.callback = callback
        self.vars_by_pos: Dict[Pos, cp_model.IntVar] = board.b.copy()
        self.raw_count = 0

    def on_solution_callback(self):
        assignment: Dict[Pos, int] = {}
        for pos, var in self.vars_by_pos.items():
            assignment[pos] = self.Value(var)
        result = SingleSolution(assignment=assignment)
        key = json.dumps(sorted([(p.x, p.y, v) for p, v in assignment.items()]))
        if key in self.unique:
            return
        self.unique.add(key)
        self.out.append(result)
        if self.callback:
            self.callback(result)
        if self.max_solutions is not None and len(self.out) >= self.max_solutions:
            self.StopSearch()


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
        # Connectivity helpers
        self.root: dict[Pos, cp_model.IntVar] = {}       # exactly one root; root <= w
        self.reach_layers: List[dict[Pos, cp_model.IntVar]] = []  # R_t[p] booleans, t = 0..T

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        # Cell color vars
        for pos in get_all_pos(self.V, self.H):
            self.b[pos] = self.model.NewBoolVar(f"b[{pos.x},{pos.y}]")
            self.w[pos] = self.model.NewBoolVar(f"w[{pos.x},{pos.y}]")
            self.model.AddExactlyOne([self.b[pos], self.w[pos]])

        # Root
        for pos in get_all_pos(self.V, self.H):
            self.root[pos] = self.model.NewBoolVar(f"root[{pos.x},{pos.y}]")

        # Percolation layers R_t (monotone flood fill)
        T = self.V * self.H  # large enough to cover whole board
        for t in range(T + 1):
            Rt: dict[Pos, cp_model.IntVar] = {}
            for pos in get_all_pos(self.V, self.H):
                Rt[pos] = self.model.NewBoolVar(f"R[{t}][{pos.x},{pos.y}]")
            self.reach_layers.append(Rt)

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
        """
        Layered percolation:
          - root is exactly the first white cell
          - R_t is monotone nondecreasing in t (R_t+1 >= R_t)
          - A cell can 'turn on' at layer t+1 iff it's white and has a neighbor on at layer t (or is root)
          - Final layer is equal to the white mask: R_T[p] == w[p]  => all whites are connected to the unique root
        """
        # to find unique solutions easily, we make only 1 possible root allowed; root is exactly the first white cell
        prev_cells_black: List[cp_model.IntVar] = []
        for pos in get_all_pos(self.V, self.H):
            and_constraint(self.model, target=self.root[pos], cs=[self.w[pos]] + prev_cells_black)
            prev_cells_black.append(self.b[pos])

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
                neigh_helpers: List[cp_model.IntVar] = []
                for q in get_neighbors4(p, self.V, self.H):
                    a = self.model.NewBoolVar(f"A[{t}][{p.x},{p.y}]<-({q.x},{q.y})")
                    and_constraint(self.model, target=a, cs=[self.w[p], Rt_prev[q]])
                    neigh_helpers.append(a)
                or_constraint(self.model, target=Rt[p], cs=[Rt_prev[p]] + neigh_helpers)

        # All whites must be reached by the final layer
        RT = self.reach_layers[T - 1]
        for p in get_all_pos(self.V, self.H):
            self.model.Add(RT[p] == self.w[p])

    def range_clues(self):
        # For each numbered cell c with value k:
        #   - Force it white (cannot be black)
        #   - Build visibility chains in four directions (excluding the cell itself)
        #   - Sum of visible whites = 1 (itself) + sum(chains) == k
        dirs = [(1,0), (-1,0), (0,1), (0,-1)]
        for y in range(self.V):
            for x in range(self.H):
                k = self.clues[y][x]
                if k == -1:
                    continue
                p = get_pos(x=x, y=y)
                # Numbered cell must be white
                self.model.Add(self.b[p] == 0)

                # Build visibility chains per direction (exclude self)
                vis_vars: List[cp_model.IntVar] = []
                for (dx, dy) in dirs:
                    ray = get_ray(p, self.V, self.H, dx, dy)  # cells outward
                    if not ray:
                        continue
                    # Chain: v0 = w[ray[0]]; vt = w[ray[t]] & vt-1
                    prev = None
                    for idx, cell in enumerate(ray):
                        v = self.model.NewBoolVar(f"vis[{x},{y}]->({dx},{dy})[{idx}]")
                        if idx == 0:
                            # v0 == w[cell]
                            self.model.Add(v == self.w[cell])
                        else:
                            and_constraint(self.model, target=v, cs=[self.w[cell], prev])
                        vis_vars.append(v)
                        prev = v

                # 1 (self) + sum(vis_vars) == k
                self.model.Add(1 + sum(vis_vars) == k)

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
        H, V = self.H, self.V
        def cb(sol: SingleSolution):
            print("Solution:")
            res = np.full((V, H), '', dtype=object)
            for pos in get_all_pos(V, H):
                c = 'B' if sol.assignment[pos] == 1 else '.'
                set_char(res, pos, c)
            for row in res:
                print(' '.join(row))
        return self.solve_all(callback=cb)
