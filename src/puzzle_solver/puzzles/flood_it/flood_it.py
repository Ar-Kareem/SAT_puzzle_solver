import sys
import time
from collections import defaultdict
from typing import Optional

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Pos, get_all_pos, get_neighbors4, get_char
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution


class Board:
    def __init__(self, nodes: dict[int, int], edges: dict[int, set[int]], horizon: int, start_node_id: int):
        self.T = horizon
        self.nodes = nodes
        self.edges = edges
        self.start_node_id = start_node_id
        self.K = len(set(nodes.values()))

        self.model = cp_model.CpModel()
        self.decision: dict[tuple[int, int], cp_model.IntVar] = {}  # (t, k)
        self.connected: dict[tuple[int, int], cp_model.IntVar] = {}  # (t, cluster_id)

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for t in range(self.T - 1):  # (N-1) actions (we dont need to decide at time N)
            for k in range(self.K):
                self.decision[t, k] = self.model.NewBoolVar(f'decision:{t}:{k}')
        for t in range(self.T):
            for cluster_id in self.nodes:
                self.connected[t, cluster_id] = self.model.NewBoolVar(f'connected:{t}:{cluster_id}')

    def add_all_constraints(self):
        # init time t=0, all clusters are not connected except start_node
        for cluster_id in self.nodes:
            if cluster_id == self.start_node_id:
                self.model.Add(self.connected[0, cluster_id] == 1)
            else:
                self.model.Add(self.connected[0, cluster_id] == 0)
        # each timestep I will pick either one or zero colors
        for t in range(self.T - 1):
            # print('fixing decision at time t=', t, 'to single action with colors', self.K)
            self.model.Add(lxp.sum([self.decision[t, k] for k in range(self.K)]) <= 1)
        # at the end of the game, all clusters must be connected
        for cluster_id in self.nodes:
            self.model.Add(self.connected[self.T-1, cluster_id] == 1)

        for t in range(1, self.T):
            for cluster_id in self.nodes:
                # connected[t, i] must be 0 if all connencted clusters at t-1 are 0 (thus connected[t, i] <= sum(connected[t-1, j] for j in touching)
                sum_neighbors = lxp.sum([self.connected[t-1, j] for j in self.edges[cluster_id]]) + self.connected[t-1, cluster_id]
                self.model.Add(self.connected[t, cluster_id] <= sum_neighbors)
                # connected[t, i] must be 0 if color chosen at time t does not match color of cluster i and not connected at t-1
                cluster_color = self.nodes[cluster_id]
                self.model.Add(self.connected[t, cluster_id] == 0).OnlyEnforceIf([self.decision[t-1, cluster_color].Not(), self.connected[t-1, cluster_id].Not()])
                self.model.Add(self.connected[t, cluster_id] == 1).OnlyEnforceIf([self.connected[t-1, cluster_id]])

        pairs = [(self.decision[t, k], t+1) for t in range(self.T - 1) for k in range(self.K)]
        self.model.Minimize(lxp.weighted_sum([p[0] for p in pairs], [p[1] for p in pairs]))

    def solve(self) -> list[SingleSolution]:
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: list[str] = [None for _ in range(self.T - 1)]
            for t in range(self.T - 1):
                for k in range(self.K):
                    if solver.Value(self.decision[t, k]) == 1:
                        assignment[t] = k
                        break
            return SingleSolution(assignment=assignment)
        return generic_solve_all(self, board_to_solution, verbose=False, max_solutions=1)


def solve_minimum_steps(board: np.array, start_pos: Optional[Pos] = None, verbose: bool = True) -> int:
    tic = time.time()
    all_colors: set[str] = {c.item().strip() for c in np.nditer(board) if c.item().strip()}
    color_to_int: dict[str, int] = {c: i for i, c in enumerate(sorted(all_colors))}  # colors string to color id
    int_to_color: dict[int, str] = {i: c for c, i in color_to_int.items()}

    graph: dict[Pos, int] = _board_to_graph(board)  # position to cluster id
    nodes: dict[int, int] = {cluster_id: color_to_int[get_char(board, pos)] for pos, cluster_id in graph.items()}
    edges = _graph_to_edges(board, graph)  # cluster id to touching cluster ids
    if start_pos is None:
        start_pos = Pos(0,0)

    def solution_int_to_str(solution: SingleSolution):
        return [int_to_color.get(color_id, '?') for color_id in solution.assignment]

    def print_solution(solution: SingleSolution):
        solution = solution_int_to_str(solution)
        print("Solution:", solution)

    solution = _binary_search_solution(nodes, edges, graph[start_pos], callback=print_solution)
    if verbose:
        if solution is None:
            print("No solution found")
        else:
            solution = solution_int_to_str(solution)
            print(f"Best Horizon: T={len(solution)}")
            print("Best solution found:", solution)
        toc = time.time()
        print(f"Time taken: {toc - tic:.2f} seconds")
    return solution


def _board_to_graph(board: np.array) -> dict[int, set[int]]:
    def dfs_flood(board: np.array, pos: Pos, cluster_id: int, graph: dict[Pos, int]):
        if pos in graph:
            return
        graph[pos] = cluster_id
        for neighbor in get_neighbors4(pos, board.shape[0], board.shape[1]):
            if get_char(board, neighbor) == get_char(board, pos):
                dfs_flood(board, neighbor, cluster_id, graph)
    graph: dict[Pos, int] = {}
    cluster_id = 0
    V, H = board.shape
    for pos in get_all_pos(V, H):
        if pos in graph:
            continue
        dfs_flood(board, pos, cluster_id, graph)
        cluster_id += 1
    return graph


def _graph_to_edges(board: np.array, graph: dict[Pos, int]) -> dict[int, set[int]]:
    cluster_edges: dict[int, set[int]] = defaultdict(set)
    V, H = board.shape
    for pos in get_all_pos(V, H):
        for neighbor in get_neighbors4(pos, V, H):
            n1, n2 = graph[pos], graph[neighbor]
            if n1 != n2:
                cluster_edges[n1].add(n2)
                cluster_edges[n2].add(n1)
    return cluster_edges


def _binary_search_solution(nodes, edges, start_node_id, callback):
    min_T = 1
    max_T = len(nodes)
    hist = {}  # record historical T and best solution
    while min_T <= max_T:
        if max_T - min_T <= 20:  # small gap, just take the middle
            T = min_T + (max_T - min_T) // 2
        else:  # large gap, just +5 the min to not go too far
            T = min_T + 15
        # main check for binary search
        if T in hist:  # already done and found solution
            solutions = hist[T]
        else:
            print(f"Trying with exactly {T} moves...", end='')
            sys.stdout.flush()
            binst = Board(nodes=nodes, edges=edges, horizon=T, start_node_id=start_node_id)
            solutions = binst.solve()
            print(' Possible!' if len(solutions) > 0 else ' Not possible!')
            if len(solutions) > 0:
                callback(solutions[0])
        if min_T == max_T:
            hist[T] = solutions
            break
        if len(solutions) > 0:
            hist[T] = solutions
            max_T = T
        else:
            min_T = T + 1
    best_solution = min(hist.items(), key=lambda x: x[0])[1][0]
    return best_solution


