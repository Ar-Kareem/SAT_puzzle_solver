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
        self.root: dict[Pos, cp_model.IntVar] = {}
        self.dist: dict[Pos, cp_model.IntVar] = {}
        # Directed adjacency arc use (q -> p)
        self.arc: dict[Tuple[Pos, Pos], cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        M = self.V * self.H  # big enough distance bound

        # Cell color vars
        for pos in get_all_pos(self.V, self.H):
            self.b[pos] = self.model.NewBoolVar(f"b[{pos.x},{pos.y}]")
            self.w[pos] = self.model.NewBoolVar(f"w[{pos.x},{pos.y}]")
            self.model.AddExactlyOne([self.b[pos], self.w[pos]])

        # Root and distance for connectivity over white cells
        for pos in get_all_pos(self.V, self.H):
            self.root[pos] = self.model.NewBoolVar(f"root[{pos.x},{pos.y}]")
            # Distances in [0, M]
            self.dist[pos] = self.model.NewIntVar(0, M, f"d[{pos.x},{pos.y}]")

        # Directed arcs on 4-neighborhood
        for p in get_all_pos(self.V, self.H):
            for q in get_neighbors4(p, self.V, self.H):
                self.arc[(q, p)] = self.model.NewBoolVar(f"arc[{q.x},{q.y}]->[{p.x},{p.y}]")
                # Arc can only be used if both endpoints are white
                self.model.Add(self.arc[(q, p)] <= self.w[p])
                self.model.Add(self.arc[(q, p)] <= self.w[q])

    def add_all_constraints(self):
        self.no_adjacent_blacks()
        self.white_connectivity_single_component()
        self.range_clues()

    def no_adjacent_blacks(self):
        cache = set()
        for p in get_all_pos(self.V, self.H):
            for q in get_neighbors4(p, self.V, self.H):
                if (p, q) in cache:
                    continue
                cache.add((p, q))
                self.model.Add(self.b[p] + self.b[q] <= 1)

    def white_connectivity_single_component(self):
        # three rules for arcs (which are between any two white neighbors p and q) (arc (q, p) means an arc from q to p)
        # 1. If either is black, the arc is false
        # 2. Every non-root white cell has exactly one incoming arc
        # 3. If you have an incoming arc from q, then your distance is > dist[q]

        # to find unique solutions easily, we make only 1 possible root allowed; root implies the first white cell and all previous cells are black
        prev_cells: List[cp_model.IntVar] = []
        for pos in get_all_pos(self.V, self.H):
            self.model.Add(self.root[pos] == 1).OnlyEnforceIf([self.w[pos]] + prev_cells)
            prev_cells.append(self.b[pos])

        # Exactly one root overall (assumes at least one white exists)
        self.model.Add(sum(self.root.values()) == 1)

        # basic distance constraints
        for pos in get_all_pos(self.V, self.H):
            # If root, distance==0
            self.model.Add(self.dist[pos] == 0).OnlyEnforceIf(self.root[pos])
            # If white and not root, distance >= 1
            self.model.Add(self.dist[pos] >= 1).OnlyEnforceIf([self.w[pos], self.root[pos].Not()])
            # If black, distance==0 (not strictly needed but helps tighten)
            self.model.Add(self.dist[pos] == 0).OnlyEnforceIf(self.b[pos])

        # Each white cell has exactly one incoming arc unless it is the unique root (then zero).
        for p in get_all_pos(self.V, self.H):
            incoming = [self.arc[(q, p)] for q in get_neighbors4(p, self.V, self.H)]
            self.model.Add(sum(incoming) == self.w[p] - self.root[p])

        # Distance strictly increases along chosen arcs (breaks cycles; ensures reachability from root)
        for (q, p), a in self.arc.items():
            self.model.Add(self.dist[p] == self.dist[q] + 1).OnlyEnforceIf(a)

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
