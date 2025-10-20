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
Total new variables: =(2+2N)V where N is average number of neighbors, ~6V for 2d grid
    """
    if is_neighbor is None:
        is_neighbor = lambda p1, p2: manhattan_distance(p1, p2) <= 1

    vs = vars_to_force
    # =V model variables, one for each variable
    is_root: dict[Pos, cp_model.IntVar] = {}
    # one for each root
    prefix_zero: dict[Pos, cp_model.IntVar] = {}
    # =NV model variables where N is average number of neighbors without double counting (if (i, j) is counted then (j, i) is not)
    # 0.2916666667
    # for a N by M 2D grid exactly = (1-1/N-1/M)*2*(N*M) [the correction term (1-1/N-1/M) is because top and left borders have 1 less neighbors]
    parent: dict[tuple[int, int], cp_model.IntVar] = {}
    # one for each parent candidate
    # total = (2+2N)V [for N by M 2D grid total is (2+4(1-1/N-1/M))*(N*M) or simply ~6*N*M]
    parent_none_before: dict[tuple[int, int], cp_model.IntVar] = {}
    prefix_name = "connected_component_"

    # must enforce some ordering
    key_to_idx: dict[Pos, int] = {p: i for i, p in enumerate(vs.keys())}
    idx_to_key: dict[int, Pos] = {i: p for p, i in key_to_idx.items()}
    keys_in_order = [idx_to_key[i] for i in range(len(key_to_idx))]

    for p in keys_in_order:
        is_root[p] = model.NewBoolVar(f"{prefix_name}is_root[{p}]")
    # Unique root: the smallest index i with x[i] = 1
    # prefix_zero[i] = AND_{k < i} (not x[k])
    prev_p = None
    for p in keys_in_order:
        b = model.NewBoolVar(f"{prefix_name}prefix_zero[{p}]")
        if prev_p is None:  # No earlier cells -> True
            model.Add(b == 1)
        else:
            # b <-> (prefix_zero[i-1] & ~x[i-1])
            and_constraint(model, b, [prefix_zero[prev_p], vs[prev_p].Not()])
        prefix_zero[p] = b
        prev_p = p

    # x[i] & prefix_zero[i] -> root[i]
    for p in keys_in_order:
        and_constraint(model, is_root[p], [vs[p], prefix_zero[p]])
    # Exactly one root:
    model.Add(sum(is_root.values()) == 1)

    # Parent edges to enforce a single connected component
    # For each node i, consider only neighbors with smaller index as parent candidates.
    # Parent edges to enforce a unique single connected component
    for i, pi in enumerate(keys_in_order):
        cand = sorted([pj for j, pj in enumerate(keys_in_order) if j < i and is_neighbor(pi, pj)])
        # none_before[i] = AND_{k < i} (not x[cand[k]])
        none_before = []
        for j, pj in enumerate(cand):
            nb = model.NewBoolVar(f"{prefix_name}none_before[{pi},{pj}]")
            parent_none_before[(pi,pj)] = nb
            if j == 0:
                model.Add(nb == 1)
            else:
                # nb <-> (none_before[j-1] & ~x[cand[j-1]])
                and_constraint(model, nb, [none_before[j-1], vs[cand[j-1]].Not()])
            none_before.append(nb)

        # if a node is active and its not root, it must have 1 parent [the first true candidate], otherwise no parent
        ps = []
        for j, pj in enumerate(cand):
            parent_ij = model.NewBoolVar(f"{prefix_name}parent[{pi},{pj}]")
            parent[(pi,pj)] = parent_ij
            am_i_root = is_root[pi]
            am_i_active = vs[pi]
            is_neighbor_active = vs[pj]
            all_before_neighbor_are_false = none_before[j]
            and_constraint(model, parent_ij, [am_i_root.Not(), am_i_active, all_before_neighbor_are_false, is_neighbor_active])
            ps.append(parent_ij)
        # if 1 then sum(parents) = 1, if 0 then sum(parents) = 0; thus sum(parents) = var_minus_root
        var_minus_root = vs[pi] - is_root[pi]
        model.Add(sum(ps) == var_minus_root)

    all_new_vars: dict[str, cp_model.IntVar] = {}
    for k, v in is_root.items():
        all_new_vars[f"{prefix_name}is_root[{k}]"] = v
    for k, v in prefix_zero.items():
        all_new_vars[f"{prefix_name}prefix_zero[{k}]"] = v
    for (p1, p2), v in parent.items():
        all_new_vars[f"{prefix_name}parent[{p1},{p2}]"] = v
    for (p1, p2), v in parent_none_before.items():
        all_new_vars[f"{prefix_name}none_before[{p1},{p2}]"] = v

    return all_new_vars