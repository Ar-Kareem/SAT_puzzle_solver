from typing import Any

import numpy as np

from puzzle_solver import slant_solver as solver
from puzzle_solver.core.utils import get_pos


def test_dummy():
    # 3x3 toy example
    # https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/slant.html#3x3:a2a0b2b3a1c0
    numbers = [
        (get_pos(x=1, y=0), 2),
        (get_pos(x=3, y=0), 0),
        (get_pos(x=2, y=1), 2),
        (get_pos(x=1, y=2), 3),
        (get_pos(x=3, y=2), 1),
        (get_pos(x=3, y=3), 0),
    ]
    binst = solver.Board(numbers=numbers, V=3, H=3)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    ground = np.array([
        [ '//', '\\', '\\' ],
        [ '//', '//', '//' ],
        [ '//', '\\', '//' ],
    ])
    ground_assignment = {get_pos(x=x, y=y): '//' if ground[y][x] == '//' else '\\' for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_dummy_2():
    # 2z2 toy example
    numbers_arr = np.array([
        ['0', ' ', '0'],
        [' ', ' ', ' '],
        ['0', ' ', '1'],
    ])
    binst = solver.Board(numbers=numbers_arr)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    ground = np.array([
        ['//', '\\'],
        ['\\', '\\'],
    ])
    ground_assignment = {get_pos(x=x, y=y): '//' if ground[y][x] == '//' else '\\' for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_ground():
    # 12x10 hard
    # https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/slant.html#12x10:b1a1a1a1e12b2a2a2a11a22a232a3b1a11a312a1b3d11c113a3a12a22a2b12c222b232e12b2a2c1d322a31c1a2112a1a1a11k1b
    numbers_arr = np.array([
        [' ', ' ', '1', ' ', '1', ' ', '1', ' ', '1', ' ', ' ', ' ', ' '],
        [' ', '1', '2', ' ', ' ', '2', ' ', '2', ' ', '2', ' ', '1', '1'],
        [' ', '2', '2', ' ', '2', '3', '2', ' ', '3', ' ', ' ', '1', ' '],
        ['1', '1', ' ', '3', '1', '2', ' ', '1', ' ', ' ', '3', ' ', ' '],
        [' ', ' ', '1', '1', ' ', ' ', ' ', '1', '1', '3', ' ', '3', ' '],
        ['1', '2', ' ', '2', '2', ' ', '2', ' ', ' ', '1', '2', ' ', ' '],
        [' ', '2', '2', '2', ' ', ' ', '2', '3', '2', ' ', ' ', ' ', ' '],
        [' ', '1', '2', ' ', ' ', '2', ' ', '2', ' ', ' ', ' ', '1', ' '],
        [' ', ' ', ' ', '3', '2', '2', ' ', '3', '1', ' ', ' ', ' ', '1'],
        [' ', '2', '1', '1', '2', ' ', '1', ' ', '1', ' ', '1', '1', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', ' ', ' '],
    ])
    binst = solver.Board(numbers=numbers_arr)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    solution = solutions[0].assignment
    ground = np.array([
        [ '//', '\\', '\\', '//', '//', '//', '//', '\\', '\\', '\\', '//', '\\' ],
        [ '\\', '\\', '\\', '\\', '\\', '\\', '//', '\\', '//', '//', '\\', '\\' ],
        [ '\\', '\\', '\\', '//', '//', '\\', '//', '\\', '\\', '\\', '\\', '//' ],
        [ '\\', '//', '\\', '\\', '//', '\\', '//', '//', '\\', '//', '\\', '//' ],
        [ '//', '\\', '\\', '//', '\\', '\\', '\\', '//', '//', '//', '\\', '\\' ],
        [ '//', '\\', '\\', '//', '\\', '\\', '\\', '//', '\\', '//', '\\', '\\' ],
        [ '//', '\\', '\\', '//', '\\', '//', '//', '//', '\\', '//', '//', '\\' ],
        [ '\\', '\\', '\\', '\\', '\\', '//', '//', '//', '\\', '//', '\\', '\\' ],
        [ '//', '//', '//', '\\', '\\', '//', '//', '\\', '\\', '//', '\\', '\\' ],
        [ '\\', '\\', '//', '//', '//', '\\', '//', '\\', '//', '\\', '\\', '//' ],
    ])
    ground_assignment = {get_pos(x=x, y=y): '//' if ground[y][x] == '//' else '\\' for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def _DEBUG_detect_cycles(nodes: dict[Any, int], neighbor_dict) -> bool:
    visited: set[Any] = set()
    edges_visited: set[tuple[Any, Any]] = set()
    path: set[Any] = set()
    to_print: list[Any] = []

    def dfs(p: Any) -> bool:
        if p in path:
            return True # Found cycle
        if p in visited:
            return False # Already explored this path, no cycle found
        visited.add(p)
        path.add(p)
        for neighbor_node, neighbor_value in neighbor_dict[p].items():
            # print(f'checking {p} to neighbor {neighbor_node} -> {"is off" if neighbor_value == 0 else "is on"}')
            if (neighbor_node, p) in edges_visited:  # already took this edge in the other direction
                continue
            if neighbor_value == 1:
                edges_visited.add((p, neighbor_node))
                to_print.append(neighbor_node)
                if dfs(neighbor_node):
                    return True
        path.remove(p)
        return False

    for start, v in nodes.items():
        if v == 0:
            continue
        # print('expanding from', start)
        assert start in nodes, f'start {start} not in nodes'
        if start not in visited:
            to_print = [start]
            if dfs(start):
                print('cycle found!!!', to_print)
                return True
            # if len(to_print) > 1:
                # print("Found acyclic subgraph with edges:")
                # print(f"graph: ", end='')
                # for edge in to_print:
                #     print(f" -> {edge}", end='')
                # print()
    return False


if __name__ == '__main__':
    test_dummy()
    test_dummy_2()
    test_ground()
