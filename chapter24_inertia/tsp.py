from collections import deque, defaultdict
from typing import Dict, List, Tuple, Set, Any, Optional
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

Pos = Any  # Hashable node id

def solve_optimal_walk(start_pos: Pos, edges: Set[Tuple[Pos, Pos]], gems_to_edges: defaultdict[Pos, List[Tuple[Pos, Pos]]]) -> List[Tuple[Pos, Pos]]:
    """
    Solve: start at `start_pos` and walk a minimum-length route that traverses
    at least one edge from each gem group in `gems_to_edges`.
    Edges are undirected with unit weight (hop=1). Returns the chosen oriented
    edges (one per group, in visiting order) and the full node-by-node walk.

    Returns:
        List[Tuple[Pos, Pos]]                            # edge to edge path from start to collect all gems in minimum number of moves
    """
    assert start_pos is not None, 'start_pos is required'
    assert edges is not None, 'edges are required'
    assert gems_to_edges is not None, 'gems_to_edges are required'
    assert len(edges) > 0, 'edges must be non-empty'
    assert len(gems_to_edges) > 0, 'gems_to_edges must be non-empty'
    assert all(all(edge in edges for edge in elist) for elist in gems_to_edges.values()), 'all edges in gems_to_edges must be in edges'
    nodes = set([u for (u, v) in edges]) | set([v for (u, v) in edges])
    assert start_pos in nodes, 'start_pos must be in edges'
    assert all(edge[0] in nodes and edge[1] in nodes for edge in edges), 'all edges must be in nodes'
    # ----------------------------
    # 0) Build the base graph (undirected, unit weights)
    # ----------------------------
    adj: Dict[Pos, List[Pos]] = {u: [] for u in nodes}
    for (u, v) in edges:
        if u not in adj: adj[u] = []
        adj[u].append(v)

    # ----------------------------
    # 1) Build oriented "states" from edges (u->v) and (v->u),
    #    and cluster them by gem_id (group).
    #    We *only* create states for edges that appear in gems_to_edges.
    # ----------------------------
    states: List[Tuple[Pos, Pos]] = []         # index -> (tail, head)
    state_group: List[Pos] = []                # index -> gem_id
    group_to_state_indices: Dict[Pos, List[int]] = defaultdict(list)

    for gem_id, elist in gems_to_edges.items():
        for (u, v) in elist:
            # Ensure edge exists in graph (robustness)
            if u not in adj or v not in adj or (v not in adj[u]):
                raise ValueError(f"Edge {(u, v)} for gem {gem_id} does not exist in base graph.")
            idx_uv = len(states); states.append((u, v)); state_group.append(gem_id); group_to_state_indices[gem_id].append(idx_uv)

    # Add a depot representing the start (not part of any gem cluster)
    DEPOT = len(states)
    states.append((None, None))
    state_group.append("__DEPOT__")

    # Quick helpers
    N_no_depot = DEPOT
    N = len(states)
    groups = [g for g in group_to_state_indices.keys()]

    # ----------------------------
    # 2) Precompute BFS shortest paths between all *relevant* nodes
    #    (all distinct endpoints of states plus start_pos).
    #    We also store predecessors to reconstruct paths later.
    # ----------------------------
    relevant_nodes: Set[Pos] = {start_pos}
    for (tail, head) in states[:N_no_depot]:
        relevant_nodes.add(tail)
        relevant_nodes.add(head)

    # BFS from a single source on unweighted graph
    def bfs(source: Pos) -> Tuple[Dict[Pos, int], Dict[Pos, Optional[Pos]]]:
        dist = {n: float('inf') for n in nodes}
        prev: Dict[Pos, Optional[Pos]] = {n: None for n in nodes}
        if source not in adj:
            return dist, prev
        dq = deque([source])
        dist[source] = 0
        while dq:
            u = dq.popleft()
            for w in adj[u]:
                if dist[w] == float('inf'):
                    dist[w] = dist[u] + 1
                    prev[w] = u
                    dq.append(w)
        return dist, prev

    # Run BFS from each relevant node
    sp_dist: Dict[Pos, Dict[Pos, int]] = {}
    sp_prev: Dict[Pos, Dict[Pos, Optional[Pos]]] = {}
    for s in relevant_nodes:
        d, p = bfs(s)
        sp_dist[s] = d
        sp_prev[s] = p

    def reconstruct_path(a: Pos, b: Pos) -> List[Pos]:
        """Return node sequence from a to b (inclusive) along a shortest path."""
        if a == b:
            return [a]
        if sp_dist[a][b] == float('inf'):
            raise ValueError(f"No path between {a} and {b}.")
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

    # ----------------------------
    # 3) Base cost matrix on original states (pre-transform):
    #    dist(i -> j) = shortest_path(head_i, tail_j) + 1;
    #    dist(DEPOT -> j) = shortest_path(start_pos, tail_j) + 1;
    #    dist(i -> DEPOT) = 0  (end anywhere; return to depot is free)
    # ----------------------------
    def base_cost(i: int, j: int) -> int:
        if i == j:
            return 0
        if i == DEPOT and j == DEPOT:
            return 0
        if i == DEPOT:
            tail_j, head_j = states[j]
            return (0 if start_pos == tail_j else sp_dist[start_pos][tail_j]) + 1
        if j == DEPOT:
            # Ending anywhere: free return to depot
            return 0
        tail_i, head_i = states[i]
        tail_j, head_j = states[j]
        move = 0 if head_i == tail_j else sp_dist[head_i][tail_j]
        return move + 1

    C = [[0]*N for _ in range(N)]
    max_base = 0
    for i in range(N):
        for j in range(N):
            c = base_cost(i, j)
            C[i][j] = c
            if i != j and i != DEPOT and j != DEPOT:
                if c != float('inf'):
                    max_base = max(max_base, c)

    # ----------------------------
    # 4) Noon–Bean transform (GTSP -> ATSP) on nodes 0..N-1, excluding DEPOT from the transform.
    #    - Add big M to every inter-cluster (non-depot) arc
    #    - Create a zero-cost "ring" in each cluster
    #    - Shift outgoing arcs of each node to its predecessor in the ring
    #    DEPOT arcs are left as-is (no M, no shifting).
    # ----------------------------
    # Choose M safely large: (max_base + 1) * (N + 5)
    M = (max_base + 1) * (N + 5)

    # Build per-cluster cyclic order (arbitrary but fixed)
    cluster_orders: Dict[Pos, List[int]] = {}
    for g in groups:
        cluster_orders[g] = list(group_to_state_indices[g])

    # Start from the base matrix
    D = [row[:] for row in C]

    # Add M to all inter-cluster arcs (i->j) where neither endpoint is DEPOT
    for i in range(N_no_depot):
        gi = state_group[i]
        for j in range(N_no_depot):
            if i == j:
                continue
            gj = state_group[j]
            if gi != gj:
                D[i][j] += M

    # For each cluster, create a zero-cost ring and shift outgoing arcs
    INF = 10**12  # effectively "forbidden" inside a cluster except ring
    for g, order in cluster_orders.items():
        k = len(order)
        if k == 0:
            continue
        # Map node -> predecessor in the chosen ring order
        pred = {}
        succ = {}
        for idx, v in enumerate(order):
            pred[v] = order[(idx - 1) % k]
            succ[v] = order[(idx + 1) % k]

        # (a) Disable all intra-cluster arcs except ring arcs (set to INF)
        for a in order:
            for b in order:
                if a == b:
                    continue
                D[a][b] = INF
        # (b) Set ring arcs a -> succ[a] to 0
        for a in order:
            D[a][succ[a]] = 0

        # (c) Shift ALL outgoing arcs to nodes in other clusters:
        #     For each node v in cluster, for each t outside cluster (and non-depot treated separately):
        #     move cost from v->t to pred[v]->t, and "block" v->t (set to INF).
        for v in order:
            pv = pred[v]
            for t in range(N):
                if t in order:  # skip intra-cluster; we already set ring
                    continue
                if v == t:
                    continue
                if v == DEPOT:
                    continue  # (not in order anyway)
                if state_group[t] == "__DEPOT__":
                    # Do not add M to arcs into DEPOT and do not shift them,
                    # but we still want all outgoing arcs from the cluster
                    # to be available only from predecessor pv (to enforce the choice).
                    # So: move v->DEPOT to pv->DEPOT, and block v->DEPOT.
                    if D[v][t] < INF:
                        # Keep the smallest if multiple map into pv->DEPOT
                        D[pv][t] = min(D[pv][t], D[v][t])
                    D[v][t] = INF
                else:
                    # t is in a different cluster: the arc cost already has +M
                    # Move it to predecessor
                    if D[v][t] < INF:
                        D[pv][t] = min(D[pv][t], D[v][t])
                    D[v][t] = INF

    # IMPORTANT: Leave all arcs touching DEPOT unchanged (they were never M-shifted).
    # D[DEPOT][*] and D[*][DEPOT] are already in C and copied over at the start.

    # ----------------------------
    # 5) Solve ATSP with OR-Tools (single vehicle, start=end=DEPOT)
    # ----------------------------
    manager = pywrapcp.RoutingIndexManager(N, 1, DEPOT)
    routing = pywrapcp.RoutingModel(manager)

    # Transit callback from D
    def transit_cb(from_index, to_index):
        i = manager.IndexToNode(from_index)
        j = manager.IndexToNode(to_index)
        return int(D[i][j])

    transit_cb_index = routing.RegisterTransitCallback(transit_cb)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_cb_index)

    # First solution + local search
    search_params = pywrapcp.DefaultRoutingSearchParameters()
    search_params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    search_params.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    search_params.time_limit.FromSeconds(10)

    solution = routing.SolveWithParameters(search_params)
    if solution is None:
        raise RuntimeError("No solution found by OR-Tools.")

    # Extract the tour (sequence of node indices)
    route: List[int] = []
    idx = routing.Start(0)
    while not routing.IsEnd(idx):
        node = manager.IndexToNode(idx)
        route.append(node)
        idx = solution.Value(routing.NextVar(idx))
    route.append(manager.IndexToNode(idx))  # end (DEPOT)

    # ----------------------------
    # 6) Decode chosen representative per cluster (in visitation order)
    #    Noon–Bean decoding: when the tour leaves a cluster Ci from node p in Ci to a node in Ck (k!=i),
    #    the selected representative for Ci is succ(p) in the ring.
    # ----------------------------
    # Build quick succ map again
    succ_in_cluster: Dict[int, int] = {}
    for g, order in cluster_orders.items():
        k = len(order)
        for idx, v in enumerate(order):
            succ_in_cluster[v] = order[(idx + 1) % k]

    visited_gems: List[Tuple[Pos, int]] = []  # [(gem_id, chosen_state_idx)]
    seen_gems: Set[Pos] = set()

    for a, b in zip(route, route[1:]):
        ga = state_group[a]
        gb = state_group[b]
        if ga == "__DEPOT__" or ga == gb:
            continue
        # Leaving cluster ga -> gb
        if ga in seen_gems:
            # We only keep the first time we leave ga (we enter each cluster once ideally)
            continue
        if a not in succ_in_cluster:
            continue  # leaving depot, ignore
        rep = succ_in_cluster[a]  # chosen representative (tail->head)
        visited_gems.append((ga, rep))
        seen_gems.add(ga)

    # Sanity: ensure every gem cluster chosen exactly once
    all_gems = set(groups)
    if all_gems != set(g for (g, _) in visited_gems):
        # In rare degeneracies, we might need to sweep the whole route to capture all leaves.
        # Fallback: collect last-in-cluster nodes and map via succ.
        missing = all_gems - set(g for (g, _) in visited_gems)
        if missing:
            # One more pass: track last node seen for each cluster, then use the point where cluster changes
            last_in_cluster: Dict[Pos, int] = {}
            for a, b in zip(route, route[1:]):
                ga = state_group[a]
                gb = state_group[b]
                if ga != "__DEPOT__":
                    last_in_cluster[ga] = a
                if ga != gb and ga in missing:
                    rep = succ_in_cluster.get(last_in_cluster[ga], None)
                    if rep is not None:
                        visited_gems.append((ga, rep))
            # Final filter (in order, unique)
            picked = {}
            ordered = []
            for g, rep in visited_gems:
                if g not in picked:
                    picked[g] = rep
                    ordered.append((g, rep))
            visited_gems = ordered

    # Order visited_gems in the actual traversal order they appear in the route
    # (they already are, based on the leave events).
    chosen_states_in_order: List[Tuple[Pos, Tuple[Pos, Pos]]] = []
    for gem_id, st_idx in visited_gems:
        tail, head = states[st_idx]
        chosen_states_in_order.append((gem_id, (tail, head)))

    # ----------------------------
    # 7) Build the actual node-by-node walk
    #    start_pos -> tail_0  +  edge(tail_0, head_0)
    #    then head_i -> tail_{i+1} + edge(...)
    # ----------------------------
    # ---------- Build a coverage-aware compressed walk ----------
    edge_to_gems: Dict[Tuple[Pos, Pos], Set[Pos]] = defaultdict(set)
    for g, elist in gems_to_edges.items():
        for e in elist:
            edge_to_gems[e].add(g)

    def mark_covered_on_path(nodes_path: List[Pos], covered: Set[Pos]) -> None:
        for i in range(len(nodes_path) - 1):
            e = (nodes_path[i], nodes_path[i+1])
            if e in edge_to_gems:
                covered.update(edge_to_gems[e])

    compressed_reps: List[Tuple[Pos, Tuple[Pos, Pos]]] = []
    covered: Set[Pos] = set()
    cur = start_pos
    walk_nodes: List[Pos] = [start_pos]

    for gem_id, (tail, head) in chosen_states_in_order:
        if gem_id in covered:
            continue

        if cur != tail:
            path_ct = reconstruct_path(cur, tail)  # directed
            mark_covered_on_path(path_ct, covered)
            walk_nodes.extend(path_ct[1:])
            cur = tail

        if gem_id in covered:
            continue

        # traverse representative edge
        if walk_nodes[-1] != tail:
            raise RuntimeError(f"Continuity broken before traversing {tail}->{head}")
        walk_nodes.append(head)
        cur = head
        if (tail, head) in edge_to_gems:
            covered.update(edge_to_gems[(tail, head)])
        compressed_reps.append((gem_id, (tail, head)))

    # ---------- Local simplification: remove 2-edge ping-pongs that add no coverage ----------
    def walk_edges(nodes_seq: List[Pos]) -> List[Tuple[Pos, Pos]]:
        return [(nodes_seq[i], nodes_seq[i+1]) for i in range(len(nodes_seq)-1)]

    # Precompute per-edge gem sets for quick coverage diffs
    def covered_gems_of_edges(edges_seq: List[Tuple[Pos, Pos]]) -> Set[Pos]:
        s: Set[Pos] = set()
        for e in edges_seq:
            if e in edge_to_gems:
                s.update(edge_to_gems[e])
        return s

    all_gems: Set[Pos] = set(gems_to_edges.keys())

    def simplify_ping_pongs(nodes_seq: List[Pos]) -> List[Pos]:
        changed = True
        ns = list(nodes_seq)
        while changed:
            changed = False
            i = 0
            while i + 3 < len(ns):
                u, v, w, z = ns[i], ns[i+1], ns[i+2], ns[i+3]
                # Look for pattern u->v, v->u (i.e., ns[i+2] == u)
                if w == u:
                    e1 = (u, v)
                    e2 = (v, u)
                    # If we drop e1 and e2, coverage lost equals gems covered ONLY by these two edges
                    edges_before = walk_edges(ns[:i+1])          # up to u
                    edges_removed = [e1, e2]
                    edges_after  = walk_edges([u] + ns[i+3:])    # resume at u -> ...

                    gems_before = covered_gems_of_edges(edges_before)
                    gems_removed = covered_gems_of_edges(edges_removed)
                    gems_after = covered_gems_of_edges(edges_after)

                    # Total gems after removal:
                    gems_total_after = gems_before | gems_after
                    # If all required gems remain covered, it's safe to remove the ping-pong
                    if all_gems.issubset(gems_total_after):
                        # remove v and w (=u) from the nodes list between positions i and i+3
                        # ns: [..., u, v, u, z, ...] => [..., u, z, ...]
                        del ns[i+1:i+3]
                        changed = True
                        # Do not increment i: re-check at the same index after removal
                        continue
                i += 1
        return ns

    walk_nodes = simplify_ping_pongs(walk_nodes)

    # ---------- Build final edge list & validate ----------
    edge_walk: List[Tuple[Pos, Pos]] = [(walk_nodes[i], walk_nodes[i+1]) for i in range(len(walk_nodes)-1)]
    assert all(e in edges for e in edge_walk), "Output contains an edge not in the input directed edges."
    # Ensure all gems are covered
    final_covered = covered_gems_of_edges(edge_walk)
    missing = all_gems - final_covered
    assert not missing, f"Walk lost coverage for gems: {missing}"

    return edge_walk
