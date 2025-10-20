import time
import json
from dataclasses import dataclass
from typing import Optional, Callable, Any, Union

from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import CpSolverSolutionCallback

from puzzle_solver.core.utils import Pos


@dataclass(frozen=True)
class SingleSolution:
    assignment: dict[Pos, Union[str, int]]

    def get_hashable_solution(self) -> str:
        result = []
        for pos, v in self.assignment.items():
            result.append((pos.x, pos.y, v))
        return json.dumps(result, sort_keys=True)


def and_constraint(model: cp_model.CpModel, target: cp_model.IntVar, cs: list[cp_model.IntVar]):
    for c in cs:
        model.Add(target <= c)
    model.Add(target >= sum(cs) - len(cs) + 1)


def or_constraint(model: cp_model.CpModel, target: cp_model.IntVar, cs: list[cp_model.IntVar]):
    for c in cs:
        model.Add(target >= c)
    model.Add(target <= sum(cs))



class AllSolutionsCollector(CpSolverSolutionCallback):
    def __init__(self,
            board: Any,
            board_to_solution: Callable[Any, SingleSolution],
            max_solutions: Optional[int] = None,
            callback: Optional[Callable[SingleSolution, None]] = None
        ):
        super().__init__()
        self.board = board
        self.board_to_solution = board_to_solution
        self.max_solutions = max_solutions
        self.callback = callback
        self.solutions = []
        self.unique_solutions = set()

    def on_solution_callback(self):
        try:
            result = self.board_to_solution(self.board, self)
            result_json = result.get_hashable_solution()
            if result_json in self.unique_solutions:
                return
            self.unique_solutions.add(result_json)
            self.solutions.append(result)
            if self.callback is not None:
                self.callback(result)
            if self.max_solutions is not None and len(self.solutions) >= self.max_solutions:
                self.StopSearch()
        except Exception as e:
            print(e)
            raise e

def generic_solve_all(board: Any, board_to_solution: Callable[Any, SingleSolution], max_solutions: Optional[int] = None, callback: Optional[Callable[[SingleSolution], None]] = None, verbose: bool = True) -> list[SingleSolution]:
    try:
        solver = cp_model.CpSolver()
        solver.parameters.enumerate_all_solutions = True
        collector = AllSolutionsCollector(board, board_to_solution, max_solutions=max_solutions, callback=callback)
        tic = time.time()
        solver.solve(board.model, collector)
        if verbose:
            print("Solutions found:", len(collector.solutions))
            print("status:", solver.StatusName())
            toc = time.time()
            print(f"Time taken: {toc - tic:.2f} seconds")
        return collector.solutions
    except Exception as e:
        print(e)
        raise e


def manhattan_distance(p1: Pos, p2: Pos) -> int:
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def force_connected_component(model: cp_model.CpModel, vars_to_force: dict[Any, cp_model.IntVar], is_neighbor: Callable[[Any, Any], bool] = None):
    """
    Forces a single connected component of the given variables and any abstract function that defines adjacency.
    Returns a dictionary of new variables that can be used to enforce the connected component constraint.
    Total new variables: =(3+N)V where N is average number of neighbors, ~7*N*M for N by M 2D grid
    WARNING: Will make solutions not unique (because the choice of parent is not unique)
    """
    if is_neighbor is None:
        is_neighbor = lambda p1, p2: manhattan_distance(p1, p2) <= 1

    vs = vars_to_force
    v_count = len(vs)
    # =V model variables, one for each variable
    is_root: dict[Pos, cp_model.IntVar] = {}  # =V
    prefix_zero: dict[Pos, cp_model.IntVar] = {}  # =V
    node_mtz: dict[Pos, cp_model.IntVar] = {}  # =V
    # =NV model variables where N is average number of neighbors (with double counting)
    # for a N by M 2D grid exactly = 4MN-2M-2N [the correction term (-2M-2N) is because the borders have less neighbors]
    parent: dict[tuple[int, int], cp_model.IntVar] = {}  # =NV
    prefix_name = "connected_component_"
    # total = (3+N)V [for N by M 2D grid total is (7MN-2M-2N) or simply ~7*N*M]

    # must enforce some ordering
    key_to_idx: dict[Pos, int] = {p: i for i, p in enumerate(vs.keys())}
    idx_to_key: dict[int, Pos] = {i: p for p, i in key_to_idx.items()}
    keys_in_order = [idx_to_key[i] for i in range(len(key_to_idx))]

    for p in keys_in_order:
        is_root[p] = model.NewBoolVar(f"{prefix_name}is_root[{p}]")
        node_mtz[p] = model.NewIntVar(0, v_count - 1, f"{prefix_name}node_mtz[{p}]")
    # Unique root: the smallest index i with x[i] = 1
    # prefix_zero[i] = AND_{k < i} (not x[k])
    prev_p = None
    for p in keys_in_order:
        b = model.NewBoolVar(f"{prefix_name}prefix_zero[{p}]")
        prefix_zero[p] = b
        if prev_p is None:  # No earlier cells -> True
            model.Add(b == 1)
        else:
            # b <-> (prefix_zero[i-1] & ~x[i-1])
            and_constraint(model, b, [prefix_zero[prev_p], vs[prev_p].Not()])
        prev_p = p

    # x[i] & prefix_zero[i] -> root[i]
    for p in keys_in_order:
        and_constraint(model, is_root[p], [vs[p], prefix_zero[p]])
    # Exactly one root:
    model.Add(sum(is_root.values()) == 1)

    # For each node i, consider only neighbors
    for i, pi in enumerate(keys_in_order):
        cand = sorted([pj for j, pj in enumerate(keys_in_order) if i != j and is_neighbor(pi, pj)])
        # if a node is active and its not root, it must have 1 parent [the first true candidate], otherwise no parent
        ps = []
        for j, pj in enumerate(cand):
            parent_ij = model.NewBoolVar(f"{prefix_name}parent[{pi},{pj}]")
            parent[(pi,pj)] = parent_ij
            am_i_root = is_root[pi]
            am_i_active = vs[pi]
            is_neighbor_active = vs[pj]
            model.AddImplication(parent_ij, am_i_root.Not())
            model.AddImplication(parent_ij, am_i_active)
            model.AddImplication(parent_ij, is_neighbor_active)
            ps.append(parent_ij)
        # if 1 then sum(parents) = 1, if 0 then sum(parents) = 0; thus sum(parents) = var_minus_root
        var_minus_root = vs[pi] - is_root[pi]
        model.Add(sum(ps) == var_minus_root)
        # MTZ constraint to force single connected component
        model.Add(node_mtz[pi] == 0).OnlyEnforceIf(is_root[pi])
        model.Add(node_mtz[pi] == 0).OnlyEnforceIf(vs[pi].Not())
        for pj in cand:
            model.Add(node_mtz[pi] == node_mtz[pj] + 1).OnlyEnforceIf(parent[(pi,pj)])

    all_new_vars: dict[str, cp_model.IntVar] = {}
    for k, v in is_root.items():
        all_new_vars[f"{prefix_name}is_root[{k}]"] = v
    for k, v in prefix_zero.items():
        all_new_vars[f"{prefix_name}prefix_zero[{k}]"] = v
    for (p1, p2), v in parent.items():
        all_new_vars[f"{prefix_name}parent[{p1},{p2}]"] = v
    for k, v in node_mtz.items():
        all_new_vars[f"{prefix_name}node_mtz[{k}]"] = v

    return all_new_vars