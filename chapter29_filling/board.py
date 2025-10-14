import json
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import CpSolverSolutionCallback
from tqdm import tqdm

@dataclass(frozen=True)
class Pos:
    x: int
    y: int


@dataclass(frozen=True)
class SingleSolution:
    assignment: dict[Pos, int]  # digit at each cell (1..9)


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
        key = json.dumps(sorted([(p.x, p.y, v) for p, v in assignment.items()]))
        if key in self.unique:
            return
        self.unique.add(key)
        result = SingleSolution(assignment=assignment)
        self.out.append(result)
        if self.callback:
            self.callback(result)
        if self.max_solutions is not None and len(self.out) >= self.max_solutions:
            self.StopSearch()


class Board:
    """
    Chapter 29: Filling
    clues: 2D numpy array of strings: '*' for empty, or '1'..'9' for fixed digits.
    Output: assign digit 1..9 to every cell.
    Each 4-connected region of equal digits d must have area exactly d.
    """
    def __init__(self, clues: np.ndarray):
        assert clues.ndim == 2 and clues.shape[0] > 0 and clues.shape[1] > 0, 'clues must be 2d'
        # Your requested assertion:
        assert all(isinstance(i.item(), str) and (i.item() == '*' or 1 <= int(i.item()) <= 9)
                   for i in np.nditer(clues)), 'clues must be -1 or digit 1..9'
        self.V = clues.shape[0]
        self.H = clues.shape[1]
        self.N = self.V * self.H
        self.clues = clues
        self.model = cp_model.CpModel()

        # Vars
        self.digit: dict[Pos, cp_model.IntVar] = {}  # 1..9
        # a[p,k] ∈ {0,1}: p belongs to component whose anchor is cell k (k in 0..N-1)
        self.a: dict[Tuple[Pos, int], cp_model.BoolVar] = {}
        # z_k = a[kpos,k] (label k used?)
        self.z: List[cp_model.BoolVar] = []
        # size[k] = sum_p a[p,k]
        self.size: List[cp_model.IntVar] = []
        # eq[p,q] ⇔ digit[p] == digit[q] for 4-neighbors
        self.eq: dict[Tuple[Pos, Pos], cp_model.BoolVar] = {}
        # Percolation reachability for each label k (layers 0..T)
        self.reach: List[List[dict[Pos, cp_model.BoolVar]]] = []

        self.create_vars()
        self.add_all_constraints()

    def lin_idx(self, p: Pos) -> int:
        return p.y * self.H + p.x

    def idx_pos(self, k: int) -> Pos:
        y, x = divmod(k, self.H)
        return Pos(x, y)

    def create_vars(self):
        V, H, N = self.V, self.H, self.N
        T = N - 1  # enough steps to flood any connected set

        # Digits
        for p in get_all_pos(V, H):
            self.digit[p] = self.model.NewIntVar(1, 9, f"dig[{p.x},{p.y}]")

        # Fix clues (exactly as you asked)
        for y in range(V):
            for x in range(H):
                k = self.clues[y][x]
                if k != '*':
                    self.model.Add(self.digit[Pos(x, y)] == int(k))

        # One-hot labels per cell
        for p in get_all_pos(V, H):
            for k in range(N):
                self.a[(p, k)] = self.model.NewBoolVar(f"a[{p.x},{p.y}]={k}")
            self.model.Add(sum(self.a[(p, k)] for k in range(N)) == 1)

        # z_k, size[k]
        for k in range(N):
            kpos = self.idx_pos(k)
            zk = self.a[(kpos, k)]  # used iff anchor cell takes its own label
            self.z.append(zk)
            self.size.append(self.model.NewIntVar(0, N, f"size[{k}]"))

        for k in range(N):
            self.model.Add(self.size[k] == sum(self.a[(p, k)] for p in get_all_pos(V, H)))

        # Anchor guard: a[p,k] <= z_k
        for k in range(N):
            zk = self.z[k]
            for p in get_all_pos(V, H):
                self.model.Add(self.a[(p, k)] <= zk)

        # Neighbor digit equality flags
        for p in get_all_pos(V, H):
            for q in get_neighbors4(p, V, H):
                if (q, p) in self.eq:
                    continue
                b = self.model.NewBoolVar(f"eq[{p.x},{p.y}]==[{q.x},{q.y}]")
                self.model.Add(self.digit[p] == self.digit[q]).OnlyEnforceIf(b)
                self.model.Add(self.digit[p] != self.digit[q]).OnlyEnforceIf(b.Not())
                self.eq[(p, q)] = b
                self.eq[(q, p)] = b

        # Percolation reachability arrays

        for k in tqdm(range(N), desc='create'):
            layers_k: List[dict[Pos, cp_model.BoolVar]] = []
            for t in range(T + 1):
                layer: dict[Pos, cp_model.BoolVar] = {}
                for p in get_all_pos(V, H):
                    layer[p] = self.model.NewBoolVar(f"R[{k}][{t}][{p.x},{p.y}]")
                layers_k.append(layer)
            self.reach.append(layers_k)

    def add_all_constraints(self):
        self.same_digit_neighbors_share_label()
        self.component_digit_uniformity()
        self.component_connectivity_percolation()
        self.component_size_equals_digit()
        self.canonical_min_anchor()  # remove label symmetry
        self.prune_digit_one()

    # Adjacent equal digits must be same label
    def same_digit_neighbors_share_label(self):
        N = self.N
        for p in get_all_pos(self.V, self.H):
            for q in get_neighbors4(p, self.V, self.H):
                b = self.eq[(p, q)]
                for k in range(N):
                    apk = self.a[(p, k)]
                    aqk = self.a[(q, k)]
                    # If eq=1 then apk == aqk (two inequalities gated by b)
                    self.model.Add(apk <= aqk + (1 - b))
                    self.model.Add(aqk <= apk + (1 - b))

    # All cells in label k have the anchor k's digit
    def component_digit_uniformity(self):
        for k in range(self.N):
            kpos = self.idx_pos(k)
            dk = self.digit[kpos]
            for p in get_all_pos(self.V, self.H):
                apk = self.a[(p, k)]
                self.model.Add(self.digit[p] == dk).OnlyEnforceIf(apk)

    # Connectivity for each label using percolation (seed at anchor when used)
    def component_connectivity_percolation(self):
        V, H, N = self.V, self.H, self.N
        T = N - 1
        for k in tqdm(range(N), desc='component_connectivity_percolation'):
            zk = self.z[k]
            R0 = self.reach[k][0]
            # Seed: only anchor is reached if used; others 0
            for p in get_all_pos(V, H):
                if p == self.idx_pos(k):
                    self.model.Add(R0[p] == zk)
                else:
                    self.model.Add(R0[p] == 0)

            # Grow monotonically inside the chosen set a[*,k]
            for t in range(T):
                Rt = self.reach[k][t]
                Rt1 = self.reach[k][t + 1]
                for p in get_all_pos(V, H):
                    apk = self.a[(p, k)]
                    # Monotone and capped by membership
                    self.model.Add(Rt1[p] >= Rt[p])
                    self.model.Add(Rt1[p] <= apk)
                    # Support from any reached neighbor
                    neigh_and = []
                    for q in get_neighbors4(p, V, H):
                        s = self.model.NewBoolVar(f"S[{k}][{t+1}][{p.x},{p.y}]<-({q.x},{q.y})")
                        self.model.Add(s <= apk)
                        self.model.Add(s <= Rt[q])
                        self.model.Add(s >= apk + Rt[q] - 1)
                        neigh_and.append(s)
                        self.model.Add(Rt1[p] >= s)
                    if neigh_and:
                        self.model.Add(Rt1[p] <= Rt[p] + sum(neigh_and))

            # Final layer equals the chosen set a[*,k]
            RT = self.reach[k][T]
            for p in get_all_pos(V, H):
                self.model.Add(RT[p] == self.a[(p, k)])

    # Region size equals its digit, using OnlyEnforceIf (no invalid multiplication)
    def component_size_equals_digit(self):
        for k in range(self.N):
            kpos = self.idx_pos(k)
            dk = self.digit[kpos]
            zk = self.z[k]
            size_k = self.size[k]
            # If label unused -> size == 0
            self.model.Add(size_k == 0).OnlyEnforceIf(zk.Not())
            # If label used -> size == digit at anchor
            self.model.Add(size_k == dk).OnlyEnforceIf(zk)

    # Canonical anchor: a region may use label k only if no member has index < k
    # (forces k to be the minimum linear index among its cells; removes symmetry)
    def canonical_min_anchor(self):
        for k in range(self.N):
            for j in range(k):  # all indices less than k
                jpos = self.idx_pos(j)
                # No cell with smaller index can belong to label k
                self.model.Add(self.a[(jpos, k)] == 0)

    def prune_digit_one(self):
        """Optional pruning: digit==1 implies no equal-digit neighbor."""
        for p in get_all_pos(self.V, self.H):
            is1 = self.model.NewBoolVar(f"is1[{p.x},{p.y}]")
            self.model.Add(self.digit[p] == 1).OnlyEnforceIf(is1)
            self.model.Add(self.digit[p] != 1).OnlyEnforceIf(is1.Not())
            for q in get_neighbors4(p, self.V, self.H):
                self.model.Add(self.eq[(p, q)] == 0).OnlyEnforceIf(is1)

    def solve_all(self, max_solutions: Optional[int] = None, callback: Optional[Callable[[SingleSolution], None]] = None) -> List[SingleSolution]:
        solver = cp_model.CpSolver()
        solver.parameters.enumerate_all_solutions = True
        # Do NOT set num_search_workers (per your note)
        solutions: List[SingleSolution] = []
        collector = AllSolutionsCollector(self.digit, solutions, max_solutions=max_solutions, callback=callback)
        solver.Solve(self.model, collector)
        print("Solutions found:", len(solutions))
        print("status:", solver.StatusName())
        return solutions

    def solve_and_print(self):
        H, V = self.H, self.V
        def cb(sol: SingleSolution):
            print("Solution:")
            res = np.full((V, H), '', dtype=object)
            for p in get_all_pos(V, H):
                c = f'{sol.assignment[p]} '
                set_char(res, p, c)
            for row in res:
                print(''.join(row))
        return self.solve_all(callback=cb)
