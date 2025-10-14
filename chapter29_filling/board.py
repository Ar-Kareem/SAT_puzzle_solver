# <chapter29_filling/board.py>
import sys
from pathlib import Path

import numpy as np
from ortools.sat.python import cp_model

sys.path.append(str(Path(__file__).parent.parent))
from core.utils import Pos, get_all_pos, get_char, set_char, get_neighbors4
from core.utils_ortools import generic_solve_all, SingleSolution


class Board:
    """
    Chapter 29: Filling (Fillomino-style)

    Variables per cell p:
      val[p]    ∈ {1..9}                        # digit
      region[p] ∈ {0..N-1}                      # id = linear index of the region's root
      is_root[p] <=> (region[p] == idx[p])      # root channel
      depth[p]  ∈ {0..N}                        # shortest 4-step distance to its region root
      parent[p->q] ∈ {0,1} for each 4-neighbor q # unique parent for non-roots

    Extra booleans:
      is_val[p,k] <=> (val[p] == k) for k=1..9
      same_edge[u,v] <=> (region[u] == region[v])  for each undirected neighbor edge

    Key constraints:
      - Respect givens for val.
      - Region root is the min index among its members: region[p] <= idx[p] for all p,
        plus root/size logic below fixes the root at the minimum index.
      - same-digit neighbors must be in the same region.
      - Inside a region, |depth[u]-depth[v]| ≤ 1 along edges (1-Lipschitz).
      - Roots: depth=0 and have no parent. Non-roots: choose exactly one neighbor
        as parent that is in the same region with depth[v] = depth[u]-1.
      - Lexicographic tie-break on candidates gives a unique parent:
        pick the earliest neighbor in fixed order (Up, Left, Right, Down).
      - Region size equals the root's digit; unused region ids have size 0.
    """

    def __init__(self, board: np.ndarray):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        self.board = board
        self.V, self.H = board.shape
        assert all((c == '*') or (str(c).isdecimal() and 0 <= int(c) <= 9)
                   for c in np.nditer(board)), "board must contain '*' or digits 0..9"

        self.N = self.V * self.H

        # Linear index maps, keyed by Pos (never construct tuples)
        self.idx_of: dict[Pos, int] = {pos: (pos.y * self.H + pos.x) for pos in get_all_pos(self.V, self.H)}
        self.pos_of: list[Pos] = [None] * self.N
        for pos, idx in self.idx_of.items():
            self.pos_of[idx] = pos

        self.model = cp_model.CpModel()

        # Per-cell variables
        self.val = {}
        self.region = {}  # fixed given val
        self.is_root = {}  # fixed given val
        self.depth = {}  # fixed given parent
        # parent[(u, v)] -> Bool for directed neighbor u->v
        self.parent = {}
        # is_val[(p, k)] -> Bool
        self.is_val = {}  # fixed given val
        self.same_edge = {}  # fixed given region
        # cand[(u, v)] -> Bool
        self.cand = {}  # complex; parent => cand => same_edge ; also cand[p,q] => val[p] == val[q] ; also cand[p,q] => depth[p] == depth[q] + 1
        self.members = {}  # fixed given region
        self.size_r = {}  # fixed given val + root

        # Create core vars and respect givens
        for p in get_all_pos(self.V, self.H):
            idx = self.idx_of[p]

            # val in 1..9; givens fixed
            v = self.model.NewIntVar(1, 9, f'val[{idx}]')
            ch = get_char(self.board, p)
            if str(ch).isdecimal():
                self.model.Add(v == int(ch))
            self.val[p] = v

            # region id and root channel
            r = self.model.NewIntVar(0, self.N - 1, f'region[{idx}]')
            self.region[p] = r
            b = self.model.NewBoolVar(f'is_root[{idx}]')
            self.is_root[p] = b
            self.model.Add(r == idx).OnlyEnforceIf(b)
            self.model.Add(r != idx).OnlyEnforceIf(b.Not())

            # depth
            d = self.model.NewIntVar(0, self.N, f'depth[{idx}]')
            self.depth[p] = d
            self.model.Add(d == 0).OnlyEnforceIf(b)
            self.model.Add(d >= 1).OnlyEnforceIf(b.Not())

            # parent vars to all 4-neighbors
            for q in get_neighbors4(p, self.V, self.H):
                self.parent[(p, q)] = self.model.NewBoolVar(f'parent[{idx}->{self.idx_of[q]}]')

        # is_val indicators (used for "same-digit neighbors must merge")
        for p in get_all_pos(self.V, self.H):
            for k in range(1, 10):
                b = self.model.NewBoolVar(f'is_val[{self.idx_of[p]}=={k}]')
                self.is_val[(p, k)] = b
                self.model.Add(self.val[p] == k).OnlyEnforceIf(b)
                self.model.Add(self.val[p] != k).OnlyEnforceIf(b.Not())

        # Helper: unique key for an undirected edge (u,v)
        def edge_key(u: Pos, v: Pos):
            iu, iv = self.idx_of[u], self.idx_of[v]
            return (iu, iv) if iu < iv else (iv, iu)

        # same_edge[u,v] <=> region[u] == region[v], plus 1-Lipschitz on depths within a region
        for u in get_all_pos(self.V, self.H):
            for v in get_neighbors4(u, self.V, self.H):
                key = edge_key(u, v)
                if key in self.same_edge:
                    continue
                b = self.model.NewBoolVar(f'same[{key[0]},{key[1]}]')
                self.same_edge[key] = b
                # channel region equality
                self.model.Add(self.region[u] == self.region[v]).OnlyEnforceIf(b)
                self.model.Add(self.region[u] != self.region[v]).OnlyEnforceIf(b.Not())
                # 1-Lipschitz inside region: |depth[u]-depth[v]| ≤ 1
                self.model.Add(self.depth[u] <= self.depth[v] + 1).OnlyEnforceIf(b)
                self.model.Add(self.depth[v] <= self.depth[u] + 1).OnlyEnforceIf(b)

        # same-digit neighbors must be in the same region
        for u in get_all_pos(self.V, self.H):
            for v in get_neighbors4(u, self.V, self.H):
                if self.idx_of[v] < self.idx_of[u]:
                    continue  # avoid duplicating the undirected pair
                b_same_region = self.same_edge[edge_key(u, v)]
                for k in range(1, 10):
                    self.model.Add(b_same_region == 1).OnlyEnforceIf([self.is_val[(u, k)], self.is_val[(v, k)]])

        # Candidate parents: same region AND one step closer
        def dir_index(u: Pos, v: Pos) -> int:
            dy, dx = v.y - u.y, v.x - u.x
            # Fixed order: Up(0), Left(1), Right(2), Down(3)
            if dy == -1 and dx == 0: return 0
            if dy == 0 and dx == -1: return 1
            if dy == 0 and dx == 1:  return 2
            return 3  # dy == 1 and dx == 0

        for u in get_all_pos(self.V, self.H):
            for v in get_neighbors4(u, self.V, self.H):
                key = edge_key(u, v)
                b_same_region = self.same_edge[key]
                c = self.model.NewBoolVar(f'cand[{self.idx_of[u]}->{self.idx_of[v]}]')
                self.cand[(u, v)] = c
                # candidate only if same region and depth[v] = depth[u] - 1
                self.model.AddImplication(c, b_same_region)
                self.model.Add(self.depth[u] == self.depth[v] + 1).OnlyEnforceIf(c)
                # parent implies candidate
                self.model.AddImplication(self.parent[(u, v)], c)
                # candidates/parents imply equal value (propagates uniform value through the tree)
                self.model.Add(self.val[u] == self.val[v]).OnlyEnforceIf(c)

        # Root vs non-root parent counting + lexicographic tiebreak by direction
        for u in get_all_pos(self.V, self.H):
            nbrs = sorted(get_neighbors4(u, self.V, self.H), key=lambda v: dir_index(u, v))
            par_vars = [self.parent[(u, v)] for v in nbrs]
            cand_vars = [self.cand[(u, v)] for v in nbrs]

            if par_vars:
                self.model.Add(sum(par_vars) == 0).OnlyEnforceIf(self.is_root[u])
                self.model.Add(sum(par_vars) == 1).OnlyEnforceIf(self.is_root[u].Not())
            else:
                # Isolated cell (shouldn't happen on a grid) -> must be a root
                self.model.Add(self.is_root[u] == 1)

            # Tiebreak: earliest candidate wins
            seen = []
            for pvar, cvar in zip(par_vars, cand_vars):
                # parent ≤ cand
                self.model.Add(pvar <= cvar)
                # parent ≥ cand - sum(seen)
                if seen:
                    self.model.Add(pvar >= cvar - sum(seen))
                else:
                    self.model.Add(pvar >= cvar)
                seen.append(cvar)

        # Ensure region id is the minimum index among its members (fixes root choice)
        for p in get_all_pos(self.V, self.H):
            self.model.Add(self.region[p] <= self.idx_of[p])

        # Membership indicators and region sizes
        # size[r] == number of cells whose region == r
        # If is_root[pos_of(r)] -> size[r] == val[pos_of(r)]
        # If not root -> size[r] == 0
        for r_idx in range(self.N):
            root_pos = self.pos_of[r_idx]
            members = []
            for p in get_all_pos(self.V, self.H):
                b = self.model.NewBoolVar(f'in_region[{self.idx_of[p]}=={r_idx}]')
                self.members[(p, r_idx)] = b
                # b <=> (region[p] == r_idx)
                self.model.Add(self.region[p] == r_idx).OnlyEnforceIf(b)
                self.model.Add(self.region[p] != r_idx).OnlyEnforceIf(b.Not())
                members.append(b)
            size_r = self.model.NewIntVar(0, self.N, f'size[{r_idx}]')
            self.size_r[r_idx] = size_r
            self.model.Add(size_r == sum(members))
            # root -> size == val[root]
            self.model.Add(size_r == self.val[root_pos]).OnlyEnforceIf(self.is_root[root_pos])
            # not root -> size == 0
            self.model.Add(size_r == 0).OnlyEnforceIf(self.is_root[root_pos].Not())

    # --- Solve/print ----------------------------------------------------------
    def solve_and_print(self):
        def board_to_assignment(board: "Board", solver: cp_model.CpSolverSolutionCallback):
            print('raw solve')
            # Return a mapping Pos -> digit for printing
            digits = {}
            for p in get_all_pos(board.V, board.H):
                digits[p] = solver.Value(board.val[p])
            return digits

        def callback(single_res: SingleSolution):
            print("Solution found")
            digits = single_res.assignment
            out = np.full((self.V, self.H), ' ', dtype=object)
            for p in get_all_pos(self.V, self.H):
                out[p.y][p.x] = str(digits[p])
            print(out)

        return generic_solve_all(self, board_to_assignment, callback=callback)
