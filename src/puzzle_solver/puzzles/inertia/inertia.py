from collections import defaultdict

import numpy as np

from puzzle_solver.core.utils import Direction8, Pos, get_all_pos, get_char, in_bounds, get_next_pos
from . import tsp


def _jump(board: np.array, pos: Pos, direction: Direction8) -> tuple[Pos, list[Pos]]:
    # jump from pos in direction, return the next position and the positions of the gems that would be achieved (mostly likely None)
    initial_pos = pos
    out = []
    while True:
        next_pos = get_next_pos(pos, direction)
        if not in_bounds(next_pos, board.shape[0], board.shape[1]):
            break
        ch = get_char(board, next_pos)
        if ch == 'W':
            break
        if ch == 'O':
            pos = next_pos
            break
        if ch == 'B':  # Note: the ball always starts ontop of an 'O' cell, thus hitting a 'B' is like hitting a 'O'
            pos = next_pos
            break
        if ch == 'M':  # WE HIT A MINE
            return None, None
        if ch == 'G':
            pos = next_pos
            out.append(next_pos)
            continue
        if ch == ' ':
            pos = next_pos
            continue
    if pos == initial_pos:  # we did not move
        return None, None
    return pos, out

def parse_nodes_and_edges(board: np.array):
    "parses the board into a graph where an edge is 1 move, and each gem lists the edges that would get it"
    assert board.ndim == 2, 'board must be 2d'
    assert all(c.item() in [' ', 'W', 'O', 'B', 'M', 'G'] for c in np.nditer(board)), 'board must contain only spaces, W, O, B, M, or G'
    todo_nodes: set[Pos] = set()
    completed_nodes: set[Pos] = set()
    edges_to_direction: dict[tuple[Pos, Pos], Direction8] = {}  # edge (u: Pos, v: Pos) -> direction
    gems_to_edges: dict[Pos, list[tuple[Pos, Pos]]] = defaultdict(list)  # gem position -> list of edges that would get this gem
    V, H = board.shape
    start_pos = [p for p in get_all_pos(V, H) if get_char(board, p) == 'B']
    assert len(start_pos) == 1, 'board must have exactly one start position'
    start_pos = start_pos[0]
    todo_nodes.add(start_pos)
    while todo_nodes:
        pos = todo_nodes.pop()
        for direction in Direction8:
            next_pos, gems = _jump(board, pos, direction)
            if next_pos is None:
                continue
            e = (pos, next_pos)
            assert e not in edges_to_direction, 'edge already exists'
            edges_to_direction[e] = direction
            if len(gems) > 0:
                for gem in gems:
                    assert e not in gems_to_edges[gem], 'edge already in gems_to_edges'
                    gems_to_edges[gem].append(e)
            if next_pos not in completed_nodes:
                todo_nodes.add(next_pos)
        completed_nodes.add(pos)
    assert len(gems_to_edges) == len([p for p in get_all_pos(V, H) if get_char(board, p) == 'G']), 'some gems are not reachable'
    edges = set(edges_to_direction.keys())
    return start_pos, edges, edges_to_direction, gems_to_edges

def get_moves_from_walk(walk: list[tuple[Pos, Pos]], edges_to_direction: dict[tuple[Pos, Pos], Direction8], verbose: bool = True) -> list[str]:
    direction_to_str = {Direction8.UP: '↑', Direction8.DOWN: '↓', Direction8.LEFT: '←', Direction8.RIGHT: '→', Direction8.UP_LEFT: '↖', Direction8.UP_RIGHT: '↗', Direction8.DOWN_LEFT: '↙', Direction8.DOWN_RIGHT: '↘'}
    for edge in walk:
        assert edge in edges_to_direction, f'edge {edge} not valid yet was in walk'
    walk_directions = [edges_to_direction[edge] for edge in walk]
    walk_directions_printable = [direction_to_str[x] for x in walk_directions]
    if verbose:
        print("number of moves", len(walk_directions))
        for i, direction in enumerate(walk_directions_printable):
            print(f"{direction}", end=' ')
            if i % 10 == 9:
                print()
        print()
    return walk_directions

def simulate_moves(board: np.array, moves: list[str]) -> bool:
    V, H = board.shape
    start_pos = [p for p in get_all_pos(V, H) if get_char(board, p) == 'B']
    assert len(start_pos) == 1, 'board must have exactly one start position'
    gems_collected_so_far = set()
    start_pos = start_pos[0]
    current_pos = start_pos
    for move in moves:
        next_pos, gems = _jump(board, current_pos, move)
        if next_pos is None:
            print(f'invalid move {move} from {current_pos}. Either hit a wall (considered illegal here) or a mine (dead)')
            return set()  # Running into a mine is fatal. Even if you picked up the last gem in the same move which then hit a mine, the game will count you as dead rather than victorious.
        current_pos = next_pos
        gems_collected_so_far.update(gems)
    return gems_collected_so_far


def is_board_completed(board: np.array, moves: list[str]) -> bool:
    V, H = board.shape
    all_gems = set(p for p in get_all_pos(V, H) if get_char(board, p) == 'G')
    gems_collected = simulate_moves(board, moves)
    assert gems_collected.issubset(all_gems), f'collected gems that are not on the board??? should not happen, {gems_collected - all_gems}'
    return gems_collected == all_gems

def solve_optimal_walk(
    start_pos: Pos,
    edges: set[tuple[Pos, Pos]],
    gems_to_edges: defaultdict[Pos, list[tuple[Pos, Pos]]],
    *,
    restarts: int = 1,          # try more for harder instances (e.g., 48–128)
    time_limit_ms: int = 1000,   # per restart
    seed: int = 0,
    verbose: bool = False
) -> list[tuple[Pos, Pos]]:
    return tsp.solve_optimal_walk(start_pos, edges, gems_to_edges, restarts=restarts, time_limit_ms=time_limit_ms, seed=seed, verbose=verbose)