import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, set_char, get_neighbors4, get_all_pos_to_idx_dict
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution, and_constraint


class Board:
    """
    Per cell p:
      val[p]    ∈ {1..9} (respect givens)
      region[p] ∈ {0..N-1}   # region id is the linear index of the region's root
      is_root[p] <=> (region[p] == idx[p])
      # NOTE: root is the minimum index among its members via region[p] ≤ idx[p]

    Per (p, k) where k is a root index (0..N-1):
      in_region[p,k]  <=> (region[p] == k)
      dist[p,k] ∈ {0..INF}
        - If in_region[p,k] = 0  ⇒  dist[p,k] = INF
        - If p == pos_of(k) and is_root[pos_of(k)] = 1  ⇒  dist[p,k] = 0
        - If in_region[p,k] = 1 and p != pos_of(k)  ⇒
              dist[p,k] = 1 + min_n masked_dist[n,k]
          where masked_dist[n,k] = dist[n,k] + 1 if in_region[n,k] else INF

    Edge (u,v):
      same-digit neighbors must be in same region.

    Region sizes:
      For each k: size[k] == #{p : region[p] == k}
      If is_root[pos_of(k)] → size[k] == val[pos_of(k)]
      Else size[k] == 0
    """

    def __init__(self, board: np.ndarray):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        self.board = board
        self.V, self.H = board.shape
        assert all((c == ' ') or (str(c).isdecimal() and 0 <= int(c) <= 9)
                   for c in np.nditer(board)), "board must contain space or digits 0..9"

        self.N = self.V * self.H
        self.INF = self.N + 1  # a safe "infinity" upper bound for distances

        # Linear index maps (keyed by Pos; do NOT construct tuples)
        self.idx_of: dict[Pos, int] = get_all_pos_to_idx_dict(self.V, self.H)
        self.pos_of: list[Pos] = [None] * self.N
        for pos, idx in self.idx_of.items():
            self.pos_of[idx] = pos

        m = self.model = cp_model.CpModel()

        # Variables
        self.val = {}          # val[p]
        self.region = {}       # region[p]
        self.same_region = {}  # same_region[(p,q)]
        self.is_root = {}      # is_root[p]
        self.is_val = {}       # is_val[(p,k)]  (k=1..9)
        self.in_region = {}    # in_region[(p,k)]  (k = 0..N-1)
        self.dist = {}         # dist[(p,k)] ∈ [0..INF]

        # Per-cell vars and givens
        for p in get_all_pos(self.V, self.H):
            idx = self.idx_of[p]

            v = m.NewIntVar(1, 9, f'val[{idx}]')
            ch = get_char(self.board, p)
            if str(ch).isdecimal():
                m.Add(v == int(ch))
            self.val[p] = v

            r = m.NewIntVar(0, self.N - 1, f'region[{idx}]')
            self.region[p] = r

            b = m.NewBoolVar(f'is_root[{idx}]')
            self.is_root[p] = b
            m.Add(r == idx).OnlyEnforceIf(b)
            m.Add(r != idx).OnlyEnforceIf(b.Not())

            # is_val indicators (for same-digit merge)
            for k in range(1, 10):
                bv = m.NewBoolVar(f'is_val[{idx}=={k}]')
                self.is_val[(p, k)] = bv
                m.Add(self.val[p] == k).OnlyEnforceIf(bv)
                m.Add(self.val[p] != k).OnlyEnforceIf(bv.Not())

        # Root = minimum index among members
        for p in get_all_pos(self.V, self.H):
            m.Add(self.region[p] <= self.idx_of[p])

        # Membership indicators in_region[p,k] <=> region[p] == k
        for k in range(self.N):
            for p in get_all_pos(self.V, self.H):
                bmem = m.NewBoolVar(f'in_region[{self.idx_of[p]}=={k}]')
                self.in_region[(p, k)] = bmem
                m.Add(self.region[p] == k).OnlyEnforceIf(bmem)
                m.Add(self.region[p] != k).OnlyEnforceIf(bmem.Not())

        # same-digit neighbors must be in the same region
        for u in get_all_pos(self.V, self.H):
            for v in get_neighbors4(u, self.V, self.H):
                if self.idx_of[v] < self.idx_of[u]:
                    continue  # undirected pair once
                # If val[u]==k and val[v]==k for any k in 1..9, then region[u]==region[v]
                # Implement as: for each k, (is_val[u,k] & is_val[v,k]) ⇒ (region[u]==region[v])
                for k in range(1, 10):
                    m.Add(self.region[u] == self.region[v])\
                        .OnlyEnforceIf([self.is_val[(u, k)], self.is_val[(v, k)]])

        for u in get_all_pos(self.V, self.H):
            for v in get_neighbors4(u, self.V, self.H):
                b = self.model.NewBoolVar(f'same_region[{self.idx_of[u]},{self.idx_of[v]}]')
                self.same_region[(u, v)] = b
                self.model.Add(self.region[u] == self.region[v]).OnlyEnforceIf(b)
                self.model.Add(self.region[u] != self.region[v]).OnlyEnforceIf(b.Not())
                self.model.Add(self.val[u] == self.val[v]).OnlyEnforceIf(b)

        # Distance variables dist[p,k] and masked AddMinEquality
        for k in range(self.N):
            root_pos = self.pos_of[k]

            for p in get_all_pos(self.V, self.H):
                dp = m.NewIntVar(0, self.INF, f'dist[{self.idx_of[p]},{k}]')
                self.dist[(p, k)] = dp

                # If p not in region k -> dist = INF
                m.Add(dp == self.INF).OnlyEnforceIf(self.in_region[(p, k)].Not())

                # Root distance: if k is active at its own position -> dist[root,k] = 0
                if p == root_pos:
                    m.Add(dp == 0).OnlyEnforceIf(self.is_root[root_pos])
                    # If root_pos isn't the root for k, membership is 0 and above rule sets INF.

            # For non-root members p of region k: dist[p,k] = 1 + min masked neighbor distances
            for p in get_all_pos(self.V, self.H):
                if p == root_pos:
                    continue  # handled above

                # Build masked neighbor candidates: INF if neighbor not in region k; else dist[n,k] + 1
                cand_vars = []
                for n in get_neighbors4(p, self.V, self.H):
                    cn = m.NewIntVar(0, self.INF, f'canddist[{self.idx_of[p]},{k}->{self.idx_of[n]}]')
                    cand_vars.append(cn)

                    both_in_region_k = m.NewBoolVar(f'both_in_region_k[{self.idx_of[p]} in {k} and {self.idx_of[n]} in {k}]')
                    and_constraint(m, both_in_region_k, [self.in_region[(p, k)], self.in_region[(n, k)]])

                    # Reified equality:
                    # in_region[n,k] => cn == dist[n,k] + 1
                    m.Add(cn == self.dist[(n, k)] + 1).OnlyEnforceIf(both_in_region_k)
                    # not in_region[n,k] => cn == INF
                    m.Add(cn == self.INF).OnlyEnforceIf(both_in_region_k.Not())

                # Only enforce the min equation when p is actually in region k (and not the root position).
                # If p ∉ region k, dp is already INF via the earlier rule.
                if cand_vars:
                    m.AddMinEquality(self.dist[(p, k)], cand_vars)
        for p in get_all_pos(self.V, self.H):
            # every cell must have 1 dist != INF (lets just do at least 1 dist != INF)
            not_infs = []
            for k in range(self.N):
                not_inf = m.NewBoolVar(f'not_inf[{self.idx_of[p]},{k}]')
                m.Add(self.dist[(p, k)] != self.INF).OnlyEnforceIf(not_inf)
                m.Add(self.dist[(p, k)] == self.INF).OnlyEnforceIf(not_inf.Not())
                not_infs.append(not_inf)
            m.AddBoolOr(not_infs)

        # Region sizes
        for k in range(self.N):
            root_pos = self.pos_of[k]
            members = [self.in_region[(p, k)] for p in get_all_pos(self.V, self.H)]
            size_k = m.NewIntVar(0, self.N, f'size[{k}]')
            m.Add(size_k == sum(members))
            # Active root -> size equals its value
            m.Add(size_k == self.val[root_pos]).OnlyEnforceIf(self.is_root[root_pos])
            # Inactive root id -> size 0
            m.Add(size_k == 0).OnlyEnforceIf(self.is_root[root_pos].Not())

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: "Board", solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, int] = {}
            for p in get_all_pos(board.V, board.H):
                assignment[p] = solver.Value(board.val[p])
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.full((self.V, self.H), ' ', dtype=object)
            for pos in get_all_pos(self.V, self.H):
                c = get_char(self.board, pos)
                c = single_res.assignment[pos]
                set_char(res, pos, c)
            print(res)
        return generic_solve_all(self, board_to_solution, callback=callback)
