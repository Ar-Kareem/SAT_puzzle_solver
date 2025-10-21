from collections import defaultdict, deque
from typing import Dict, List, Tuple, Set, Any, Optional
import random

from ortools.constraint_solver import pywrapcp, routing_enums_pb2


Pos = Any  # Hashable node id

def solve_optimal_walk(
    start_pos: Pos,
    edges: Set[Tuple[Pos, Pos]],
    gems_to_edges: "defaultdict[Pos, List[Tuple[Pos, Pos]]]",
    *,
    restarts: int,          # try more for harder instances (e.g., 48–128)
    time_limit_ms: int,   # per restart
    seed: int,
    verbose: bool
) -> List[Tuple[Pos, Pos]]:
    """
    Directed edges. For each gem (key in gems_to_edges), traverse >=1 of its directed edges.
    Returns the actual directed walk (edge-by-edge) from start_pos.
    Uses multi-start Noon–Bean + OR-Tools and post-optimizes the representative order.

    I significantly used AI for the implementation of this function which is why it is a bit messy with useless comments.
    """
    # ---- Multi-start Noon–Bean + metaheuristic sweeps ----
    meta_list = [
        # routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH,
        # routing_enums_pb2.LocalSearchMetaheuristic.SIMULATED_ANNEALING,
        routing_enums_pb2.LocalSearchMetaheuristic.TABU_SEARCH,
    ]
    expected_runtime = time_limit_ms * restarts * len(meta_list)
    if verbose:
        print(f'minimum runtime: {expected_runtime/1000:.1f} seconds')
    rng = random.Random(seed)

    assert start_pos is not None, 'start_pos is required'
    assert edges, 'edges must be non-empty'
    assert gems_to_edges, 'gems_to_edges must be non-empty'
    assert all(all(e in edges for e in elist) for elist in gems_to_edges.values()), \
        'all gem edges must be in edges'

    nodes = set(u for (u, v) in edges) | set(v for (u, v) in edges)
    assert start_pos in nodes, 'start_pos must be in edges'
    assert all(u in nodes and v in nodes for (u, v) in edges)

    # ---------- Directed adjacency ----------
    adj: Dict[Pos, List[Pos]] = {u: [] for u in nodes}
    for (u, v) in edges:
        adj[u].append(v)

    # ---------- States: ONLY the given directed gem edges ----------
    states: List[Tuple[Pos, Pos]] = []   # index -> (tail, head)
    state_group: List[Pos] = []          # index -> gem_id
    group_to_state_indices_original: Dict[Pos, List[int]] = defaultdict(list)

    for gem_id, elist in gems_to_edges.items():
        for (u, v) in elist:
            idx = len(states)
            states.append((u, v))
            state_group.append(gem_id)
            group_to_state_indices_original[gem_id].append(idx)

    # Depot node
    DEPOT = len(states)
    states.append((None, None))
    state_group.append("__DEPOT__")

    N_no_depot = DEPOT
    N = len(states)
    gem_groups = list(group_to_state_indices_original.keys())
    all_gems: Set[Pos] = set(gem_groups)

    # ---------- Directed shortest paths among relevant nodes ----------
    relevant: Set[Pos] = {start_pos}
    for (tail, head) in states[:N_no_depot]:
        relevant.add(tail)
        relevant.add(head)

    def bfs_dir(src: Pos) -> Tuple[Dict[Pos, int], Dict[Pos, Optional[Pos]]]:
        dist = {n: float('inf') for n in nodes}
        prev = {n: None for n in nodes}
        if src not in adj:
            return dist, prev
        q = deque([src])
        dist[src] = 0
        while q:
            u = q.popleft()
            for w in adj[u]:
                if dist[w] == float('inf'):
                    dist[w] = dist[u] + 1
                    prev[w] = u
                    q.append(w)
        return dist, prev

    sp_dist: Dict[Pos, Dict[Pos, int]] = {}
    sp_prev: Dict[Pos, Dict[Pos, Optional[Pos]]] = {}
    for s in relevant:
        d, p = bfs_dir(s)
        sp_dist[s], sp_prev[s] = d, p

    def reconstruct_path(a: Pos, b: Pos) -> List[Pos]:
        if a == b:
            return [a]
        if sp_dist[a][b] == float('inf'):
            raise ValueError(f"No directed path {a} -> {b}.")
        path = [b]
        cur = b
        prev_map = sp_prev[a]
        while cur != a:
            cur = prev_map[cur]
            if cur is None:
                raise RuntimeError("Predecessor chain broken.")
            path.append(cur)
        path.reverse()
        return path

    BIG = 10**9

    def build_base_cost_matrix() -> Tuple[List[List[int]], int]:
        # dist(i->j) = sp(head_i, tail_j) + 1
        # dist(DEPOT->j) = sp(start_pos, tail_j) + 1
        # dist(i->DEPOT) = 0  (end anywhere)
        C = [[0]*N for _ in range(N)]
        max_base = 0
        for i in range(N):
            for j in range(N):
                if i == j:
                    c = 0
                elif i == DEPOT and j == DEPOT:
                    c = 0
                elif i == DEPOT:
                    tail_j, _ = states[j]
                    d = 0 if start_pos == tail_j else sp_dist[start_pos][tail_j]
                    c = BIG if d == float('inf') else d + 1
                elif j == DEPOT:
                    c = 0
                else:
                    _, head_i = states[i]
                    tail_j, _ = states[j]
                    d = 0 if head_i == tail_j else sp_dist[head_i][tail_j]
                    c = BIG if d == float('inf') else d + 1
                C[i][j] = c
                if i != j and i != DEPOT and j != DEPOT and c < BIG:
                    if c > max_base:
                        max_base = c
        return C, max_base

    C_base, max_base = build_base_cost_matrix()

    edge_to_gems: Dict[Tuple[Pos, Pos], Set[Pos]] = defaultdict(set)
    for g, elist in gems_to_edges.items():
        for e in elist:
            edge_to_gems[e].add(g)

    # ---- Coverage-aware stitching cost for a sequence of representatives ----
    def build_walk_from_reps(rep_seq: List[int]) -> Tuple[List[Pos], Set[Pos]]:
        """Return (walk_nodes, covered_gems) for given representative state indices."""
        covered: Set[Pos] = set()
        walk_nodes: List[Pos] = [start_pos]
        cur = start_pos
        # map states idx -> (tail, head)
        for st in rep_seq:
            tail, head = states[st]
            # skip if gem already covered
            g = state_group[st]
            if g in covered:
                continue
            # connector
            if cur != tail:
                path = reconstruct_path(cur, tail)
                # mark gems on connector
                for i in range(len(path)-1):
                    e = (path[i], path[i+1])
                    if e in edge_to_gems:
                        covered.update(edge_to_gems[e])
                walk_nodes.extend(path[1:])
                cur = tail
                if g in covered:
                    continue
            # traverse rep edge
            walk_nodes.append(head)
            cur = head
            if (tail, head) in edge_to_gems:
                covered.update(edge_to_gems[(tail, head)])
        return walk_nodes, covered

    def walk_edges(nodes_seq: List[Pos]) -> List[Tuple[Pos, Pos]]:
        return [(nodes_seq[i], nodes_seq[i+1]) for i in range(len(nodes_seq)-1)]

    def simplify_ping_pongs(nodes_seq: List[Pos]) -> List[Pos]:
        """Remove u->v->u pairs if they don't lose coverage."""
        ns = list(nodes_seq)
        changed = True
        while changed:
            changed = False
            i = 0
            while i + 3 < len(ns):
                u, v, w, z = ns[i], ns[i+1], ns[i+2], ns[i+3]
                if w == u:  # u->v, v->u
                    before_edges = walk_edges(ns[:i+1])
                    removed_edges = [(u, v), (v, u)]
                    after_edges = walk_edges([u] + ns[i+3:])
                    covered_before = set()
                    for e in before_edges:
                        if e in edge_to_gems:
                            covered_before.update(edge_to_gems[e])
                    covered_removed = set()
                    for e in removed_edges:
                        if e in edge_to_gems:
                            covered_removed.update(edge_to_gems[e])
                    covered_after = set()
                    for e in after_edges:
                        if e in edge_to_gems:
                            covered_after.update(edge_to_gems[e])
                    if all_gems.issubset(covered_before | covered_after):
                        del ns[i+1:i+3]   # drop v,u
                        changed = True
                        continue
                i += 1
        return ns

    def true_walk_cost(nodes_seq: List[Pos]) -> int:
        # Number of edges (unit cost)
        return len(nodes_seq) - 1

    # ---- Noon–Bean + OR-Tools single run (with given cluster ring orders and metaheuristic) ----
    def solve_once(cluster_orders: Dict[Pos, List[int]], metaheuristic):
        # Build Noon–Bean cost matrix from C_base
        M = (max_base + 1) * (N + 5)
        D = [row[:] for row in C_base]  # copy

        # add M to inter-cluster (excluding depot)
        for i in range(N_no_depot):
            gi = state_group[i]
            for j in range(N_no_depot):
                if i == j: 
                    continue
                gj = state_group[j]
                if gi != gj:
                    D[i][j] += M

        # ring + shift
        INF = 10**12
        succ_in_cluster: Dict[int, int] = {}
        for g, order in cluster_orders.items():
            k = len(order)
            if k == 0: 
                continue
            pred = {}
            for idx, v in enumerate(order):
                pred[v] = order[(idx - 1) % k]
                succ_in_cluster[v] = order[(idx + 1) % k]
            # block intra except ring
            for a in order:
                for b in order:
                    if a != b:
                        D[a][b] = INF
            # ring arcs
            for a in order:
                D[a][succ_in_cluster[a]] = 0
            # shift outgoing to pred
            for v in order:
                pv = pred[v]
                for t in range(N):
                    if t in order or v == t or v == DEPOT:
                        continue
                    if state_group[t] == "__DEPOT__":
                        if D[v][t] < INF:
                            D[pv][t] = min(D[pv][t], D[v][t])
                        D[v][t] = INF
                    else:
                        if D[v][t] < INF:
                            D[pv][t] = min(D[pv][t], D[v][t])
                        D[v][t] = INF

        # OR-Tools
        manager = pywrapcp.RoutingIndexManager(N, 1, DEPOT)
        routing = pywrapcp.RoutingModel(manager)

        def transit_cb(from_index, to_index):
            i = manager.IndexToNode(from_index)
            j = manager.IndexToNode(to_index)
            return int(D[i][j])

        transit_cb_index = routing.RegisterTransitCallback(transit_cb)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_cb_index)

        params = pywrapcp.DefaultRoutingSearchParameters()
        params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        params.local_search_metaheuristic = metaheuristic
        params.time_limit.FromMilliseconds(max(0.01, time_limit_ms))
        params.log_search = False

        solution = routing.SolveWithParameters(params)
        if solution is None:
            return None, None, None, None

        # decode tour
        route: List[int] = []
        idx = routing.Start(0)
        while not routing.IsEnd(idx):
            route.append(manager.IndexToNode(idx))
            idx = solution.Value(routing.NextVar(idx))
        route.append(manager.IndexToNode(idx))  # DEPOT

        # representatives via leaving events (succ(p))
        rep_idxs: List[int] = []
        seen_gems: Set[Pos] = set()
        for a, b in zip(route, route[1:]):
            ga, gb = state_group[a], state_group[b]
            if ga == "__DEPOT__" or ga == gb:
                continue
            if ga in seen_gems:
                continue
            # chosen representative is succ(a)
            if a in cluster_orders.get(ga, []):
                # find succ
                order = cluster_orders[ga]
                ai = order.index(a)
                rep = order[(ai + 1) % len(order)]
                rep_idxs.append(rep)
                seen_gems.add(ga)

        return rep_idxs, succ_in_cluster, D, route

    best_nodes = None
    best_cost = float('inf')
    best_reps = None

    # initial deterministic order as a baseline
    def shuffled_cluster_orders():
        orders = {}
        for g, idxs in group_to_state_indices_original.items():
            order = idxs[:]  # copy existing indexing order
            rng.shuffle(order)  # randomize ring to mitigate Noon–Bean bias
            orders[g] = order
        return orders

    attempts = max(1, restarts)
    for attempt in range(attempts):
        cluster_orders = shuffled_cluster_orders()
        for meta in meta_list:
            # print('solve once')
            rep_idxs, _, _, _ = solve_once(cluster_orders, meta)
            # print('solve once done')
            if rep_idxs is None:
                continue

            # -------- Local 2-opt on representative order (under true walk cost) --------
            # Start from the order returned by the solver
            reps = rep_idxs[:]

            def reps_to_nodes_and_cost(rep_seq: List[int]) -> Tuple[List[Pos], int]:
                nodes_seq, covered = build_walk_from_reps(rep_seq)
                # ensure full coverage; otherwise penalize
                if not all_gems.issubset(covered):
                    return nodes_seq, len(nodes_seq) - 1 + 10**6
                nodes_seq = simplify_ping_pongs(nodes_seq)
                return nodes_seq, true_walk_cost(nodes_seq)

            improved = True
            nodes_seq, cost = reps_to_nodes_and_cost(reps)
            while improved:
                improved = False
                n = len(reps)
                # classic 2-opt swap on the order of representatives
                for i in range(n):
                    for j in range(i+1, n):
                        new_reps = reps[:i] + reps[i:j+1][::-1] + reps[j+1:]
                        new_nodes, new_cost = reps_to_nodes_and_cost(new_reps)
                        if new_cost < cost:
                            reps = new_reps
                            # print('2-opt improved cost from', cost, 'to', new_cost)
                            nodes_seq, cost = new_nodes, new_cost
                            improved = True
                            break
                    if improved:
                        break

            if cost < best_cost:
                best_cost = cost
                best_nodes = nodes_seq
                best_reps = reps

    if best_nodes is None:
        raise RuntimeError("No solution found.")
    # print('final check')
    # Final checks and edge list
    edge_walk: List[Tuple[Pos, Pos]] = [(best_nodes[i], best_nodes[i+1]) for i in range(len(best_nodes)-1)]
    assert all(e in edges for e in edge_walk), "Output contains an edge not in the input directed edges."

    # Ensure all gems covered
    covered_final: Set[Pos] = set()
    for e in edge_walk:
        if e in edge_to_gems:
            covered_final.update(edge_to_gems[e])
    missing = all_gems - covered_final
    assert not missing, f"Walk lost coverage for gems: {missing}"

    return edge_walk
