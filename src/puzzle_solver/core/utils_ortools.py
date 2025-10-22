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
    Total new variables: =4V [for N by M 2D grid total is 4NM]
    """
    if is_neighbor is None:
        is_neighbor = lambda p1, p2: manhattan_distance(p1, p2) <= 1

    vs = vars_to_force
    v_count = len(vs)
    if v_count <= 2:  # graph must have at least 3 nodes to possibly be disconnected
        return {}
    # =V model variables, one for each variable
    is_root: dict[Pos, cp_model.IntVar] = {}  # =V, defines the unique root 
    prefix_zero: dict[Pos, cp_model.IntVar] = {}  # =V, used for picking the unique root
    node_height: dict[Pos, cp_model.IntVar] = {}  # =V, trickles down from the root
    max_neighbor_height: dict[Pos, cp_model.IntVar] = {}  # =V, the height of the tallest neighbor
    prefix_name = "connected_component_"
    # total = 4V [for N by M 2D grid total is 4NM]

    keys_in_order = list(vs.keys())  # must enforce some ordering

    for p in keys_in_order:
        is_root[p] = model.NewBoolVar(f"{prefix_name}is_root[{p}]")
        node_height[p] = model.NewIntVar(0, v_count, f"{prefix_name}node_height[{p}]")
        max_neighbor_height[p] = model.NewIntVar(0, v_count, f"{prefix_name}max_neighbor_height[{p}]")
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
    model.Add(sum(is_root.values()) <= 1)

    # For each node i, consider only neighbors
    for i, pi in enumerate(keys_in_order):
        # ps is list of neighbor heights
        ps = [node_height[pj] for j, pj in enumerate(keys_in_order) if i != j and is_neighbor(pi, pj)]
        model.AddMaxEquality(max_neighbor_height[pi], ps)
        # if a node is active and its not root, its height is the height of the tallest neighbor - 1
        model.Add(node_height[pi] == max_neighbor_height[pi] - 1).OnlyEnforceIf([vs[pi], is_root[pi].Not()])
        model.Add(node_height[pi] == v_count).OnlyEnforceIf(is_root[pi])
        model.Add(node_height[pi] == 0).OnlyEnforceIf(vs[pi].Not())
    
    # final check: all active nodes have height > 0
    for p in keys_in_order:
        model.Add(node_height[p] > 0).OnlyEnforceIf(vs[p])

    all_new_vars: dict[str, cp_model.IntVar] = {}
    for k, v in is_root.items():
        all_new_vars[f"{prefix_name}is_root[{k}]"] = v
    for k, v in prefix_zero.items():
        all_new_vars[f"{prefix_name}prefix_zero[{k}]"] = v
    for k, v in node_height.items():
        all_new_vars[f"{prefix_name}node_height[{k}]"] = v
    for k, v in max_neighbor_height.items():
        all_new_vars[f"{prefix_name}max_neighbor_height[{k}]"] = v

    return all_new_vars


def force_no_loops(model: cp_model.CpModel, vars_to_force: dict[Any, cp_model.IntVar], is_neighbor: Callable[[Any, Any], bool] = None):
    """
    Forces no loops in the given variables and any abstract function that defines adjacency.
    Returns a dictionary of new variables that can be used to enforce the no component constraint.
    """
    if is_neighbor is None:
        is_neighbor = lambda p1, p2: manhattan_distance(p1, p2) <= 1

    vs = vars_to_force
    v_count = len(vs)
    is_root: dict[Pos, cp_model.IntVar] = {}
    block_root: dict[Pos, cp_model.IntVar] = {}
    node_height: dict[Pos, cp_model.IntVar] = {}
    tree_edge: dict[tuple[Pos, Pos], cp_model.IntVar] = {}  # tree_edge[p, q] means p is parent of q
    prefix_name = "no_loops_"

    parent_of = {p: [] for p in vs.keys()}
    children_of = {p: [] for p in vs.keys()}
    for p in vs.keys():
        for q in vs.keys():
            if p == q:
                continue
            if is_neighbor(p, q):
                parent_of[q].append(p)
                children_of[p].append(q)

    keys_in_order = list(vs.keys())  # must enforce some ordering
    node_to_idx: dict[Pos, int] = {p: i+1 for i, p in enumerate(keys_in_order)}
    for p in keys_in_order:
        # capacity = node_to_idx[p] + 1
        # if p == Pos(0, 0):
        #     capacity = 10
        #     print(f'capacity for {p} = {capacity}')
        node_height[p] = model.NewIntVar(0, v_count, f"{prefix_name}node_height[{p}]")
        block_root[p] = model.NewIntVar(0, node_to_idx[p], f"{prefix_name}block_root[{p}]")
        is_root[p] = model.NewBoolVar(f"{prefix_name}is_root[{p}]")
        model.Add(is_root[p] == 0).OnlyEnforceIf([vs[p].Not()])
        model.Add(node_height[p] == 0).OnlyEnforceIf([vs[p].Not()])
        model.Add(node_height[p] == 1).OnlyEnforceIf([is_root[p]])
        model.Add(block_root[p] == 0).OnlyEnforceIf([vs[p].Not()])
        model.Add(block_root[p] == node_to_idx[p]).OnlyEnforceIf([is_root[p]])

    for p in keys_in_order:
        for q in children_of[p]:
            tree_edge[(p, q)] = model.NewBoolVar(f"{prefix_name}tree_edge[{p} is parent of {q}]")
            model.Add(tree_edge[(p, q)] == 0).OnlyEnforceIf([vs[p].Not()])
            model.Add(tree_edge[(p, q)] == 0).OnlyEnforceIf([vs[q].Not()])
            # a tree_edge[p, q] means p is parent of q thus h[q] = h[p] + 1
            model.Add(node_height[q] == node_height[p] + 1).OnlyEnforceIf([tree_edge[(p, q)]])
            model.Add(block_root[q] == block_root[p]).OnlyEnforceIf([tree_edge[(p, q)]])

    for (p, q) in tree_edge:
        if (q, p) in tree_edge:
            model.Add(tree_edge[(p, q)] == 0).OnlyEnforceIf([tree_edge[(q, p)]])
            model.Add(tree_edge[(p, q)] == 1).OnlyEnforceIf([tree_edge[(q, p)].Not(), vs[p], vs[q]])

    for p in keys_in_order:
        for p_child in children_of[p]:
            # i am root thus I point to all my children
            model.Add(tree_edge[(p, p_child)] == 1).OnlyEnforceIf([is_root[p], vs[p_child]])
        for p_parent in parent_of[p]:
            # i am root thus I have no parent
            model.Add(tree_edge[(p_parent, p)] == 0).OnlyEnforceIf([is_root[p]])
        # every active node has exactly 1 parent except root has none
        model.AddExactlyOne([tree_edge[(p_parent, p)] for p_parent in parent_of[p]] + [vs[p].Not(), is_root[p]])
    
    # now each subgraph has directions where each non-root points to a single parent (and its value is parent+1). 
    # to break cycles, every non-root active node must be > all neighbors that arent children

    all_new_vars: dict[str, cp_model.IntVar] = {}
    for k, v in is_root.items():
        all_new_vars[f"{prefix_name}is_root[{k}]"] = v
    for k, v in tree_edge.items():
        all_new_vars[f"{prefix_name}tree_edge[{k[0]} is parent of {k[1]}]"] = v
    for k, v in node_height.items():
        all_new_vars[f"{prefix_name}node_height[{k}]"] = v
    for k, v in block_root.items():
        all_new_vars[f"{prefix_name}block_root[{k}]"] = v

    return all_new_vars
