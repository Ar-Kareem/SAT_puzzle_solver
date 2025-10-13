import json
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import CpSolverSolutionCallback


@dataclass(frozen=True)
class Pos:
    x: int
    y: int


@dataclass(frozen=True)
class SingleSolution:
    assignment: dict[Pos, int]  # 1 = black, 0 = white


def get_pos(x: int, y: int) -> Pos:
    return Pos(x=x, y=y)


def get_all_pos(V: int, H: int):
    for y in range(V):
        for x in range(H):
            yield get_pos(x=x, y=y)


def set_char(board: np.ndarray, pos: Pos, char: str):
    board[pos.y][pos.x] = char


def in_bounds(pos: Pos, V: int, H: int) -> bool:
    return 0 <= pos.y < V and 0 <= pos.x < H


def get_neighbors4(pos: Pos, V: int, H: int) -> List[Pos]:
    for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
        p2 = Pos(pos.x+dx, pos.y+dy)
        if in_bounds(p2, V, H):
            yield p2


def get_ray(pos: Pos, V: int, H: int, dx: int, dy: int) -> List[Pos]:
    out = []
    x, y = pos.x + dx, pos.y + dy
    while 0 <= y < V and 0 <= x < H:
        out.append(Pos(x, y))
        x += dx
        y += dy
    return out


class AllSolutionsCollector(CpSolverSolutionCallback):
    def __init__(self, model_vars, out: List[SingleSolution], max_solutions: Optional[int] = None, callback: Optional[Callable[[SingleSolution], None]] = None):
        super().__init__()
        self.out = out
        self.unique = set()
        self.max_solutions = max_solutions
        self.callback = callback
        self.vars_by_pos: Dict[Pos, cp_model.IntVar] = model_vars.copy()
        self.raw_count = 0

    def on_solution_callback(self):
        self.raw_count += 1
        if self.raw_count % 100 == 0:
            print(f"raw count: {self.raw_count}")
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
            layer: dict[Pos, cp_model.IntVar] = {}
            for pos in get_all_pos(self.V, self.H):
                layer[pos] = self.model.NewBoolVar(f"R[{t}][{pos.x},{pos.y}]")
            self.reach_layers.append(layer)

        # Seed: R0 = root
        for pos in get_all_pos(self.V, self.H):
            self.model.Add(self.reach_layers[0][pos] == self.root[pos])

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
          - R_t is monotone nondecreasing in t
          - A cell can 'turn on' at layer t+1 if it's white and has a neighbor on at layer t
          - Final layer equals the white mask: R_T[p] == w[p]  => all whites are connected to the unique root
        """
        # to find unique solutions easily, we make only 1 possible root allowed; root implies the first white cell and all previous cells are black
        prev_cells: List[cp_model.IntVar] = []
        for pos in get_all_pos(self.V, self.H):
            self.model.Add(self.root[pos] == 1).OnlyEnforceIf([self.w[pos]] + prev_cells)
            prev_cells.append(self.b[pos])

        # Exactly one root overall (assumes at least one white exists)
        self.model.Add(sum(self.root.values()) == 1)

        T = len(self.reach_layers) - 1
        for t in range(T):
            Rt = self.reach_layers[t]
            Rt1 = self.reach_layers[t + 1]
            for p in get_all_pos(self.V, self.H):
                # Monotonicity: once reached, stays reached
                self.model.Add(Rt1[p] >= Rt[p])
                # Can only be reached if white
                self.model.Add(Rt1[p] <= self.w[p])

                # Helper "AND" vars for (white[p] AND Rt[q]) for each neighbor q
                neigh_helpers: List[cp_model.IntVar] = []
                for q in get_neighbors4(p, self.V, self.H):
                    a = self.model.NewBoolVar(f"A[{t+1}][{p.x},{p.y}]<-({q.x},{q.y})")
                    # a == w[p] & Rt[q]
                    self.model.Add(a <= self.w[p])
                    self.model.Add(a <= Rt[q])
                    self.model.Add(a >= self.w[p] + Rt[q] - 1)
                    neigh_helpers.append(a)
                    # If supported by any neighbor, you can be reached
                    self.model.Add(Rt1[p] >= a)

                # Upper bound to tighten: Rt1[p] can't exceed previous reach or sum of supports
                self.model.Add(Rt1[p] <= Rt[p] + sum(neigh_helpers))

        # All whites must be reached by the final layer
        RT = self.reach_layers[T]
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
                p = Pos(x, y)
                # Numbered cell must be white
                self.model.Add(self.b[p] == 0)

                # Build visibility chains per direction (exclude self)
                vis_vars: List[cp_model.IntVar] = []
                for (dx, dy) in dirs:
                    ray = get_ray(p, self.V, self.H, dx, dy)  # cells outward
                    if not ray:
                        continue
                    # Chain: v0 = w[ray[0]]; vt = vt-1 & w[ray[t]]
                    prev = None
                    for idx, cell in enumerate(ray):
                        v = self.model.NewBoolVar(f"vis[{x},{y}]->({dx},{dy})[{idx}]")
                        if idx == 0:
                            # v0 == w[cell]
                            self.model.Add(v == self.w[cell])
                        else:
                            self.model.Add(v <= prev)
                            self.model.Add(v <= self.w[cell])
                            self.model.Add(v >= prev + self.w[cell] - 1)
                        vis_vars.append(v)
                        prev = v

                # 1 (self) + sum(vis_vars) == k
                self.model.Add(1 + sum(vis_vars) == k)

    def solve_all(self, max_solutions: Optional[int] = None, callback: Optional[Callable[[SingleSolution], None]] = None) -> List[SingleSolution]:
        solver = cp_model.CpSolver()
        solver.parameters.enumerate_all_solutions = True
        solutions: List[SingleSolution] = []
        collector = AllSolutionsCollector(self.b, solutions, max_solutions=max_solutions, callback=callback)
        solver.Solve(self.model, collector)
        print("Solutions found:", len(solutions))
        print("status:", solver.StatusName())
        return solutions

    def solve_and_print(self):
        H, V = self.H, self.V
        def cb(sol: SingleSolution):
            print("Solution:")
            res = np.full((V, H), '', dtype=object)
            for pos in get_all_pos(V, H):
                c = 'B ' if sol.assignment[pos] == 1 else '. '
                set_char(res, pos, c)
            for row in res:
                print(''.join(row))
        return self.solve_all(callback=cb)
