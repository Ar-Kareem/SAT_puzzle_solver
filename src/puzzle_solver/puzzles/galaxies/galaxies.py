from collections import defaultdict
from typing import Iterable, Union

import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, set_char, Direction, get_next_pos, in_bounds, get_opposite_direction, get_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution, force_connected_component
from puzzle_solver.core.utils_visualizer import combined_function, id_board_to_wall_fn


def parse_numpy(galaxies: np.ndarray) -> list[tuple[Pos, ...]]:
    result = defaultdict(list)
    for pos, arr_id in np.ndenumerate(galaxies):
        if not arr_id.strip():
            continue
        result[arr_id].append(get_pos(x=pos[1], y=pos[0]))
    return [positions for _, positions in sorted(result.items(), key=lambda x: x[0])]


class Board:
    def __init__(self, galaxies: Union[list[tuple[Pos, ...]], np.ndarray], V: int = None, H: int = None):
        if isinstance(galaxies, np.ndarray):
            V, H = galaxies.shape
            galaxies = parse_numpy(galaxies)
        else:
            assert V is not None and H is not None, 'V and H must be provided if galaxies is not a numpy array'
        assert V >= 1 and H >= 1, 'V and H must be at least 1'
        assert all(isinstance(galaxy, Iterable) for galaxy in galaxies), 'galaxies must be a list of Iterables'
        assert all(len(galaxy) in [1, 2, 4] for galaxy in galaxies), 'each galaxy must be exactly 1, 2, or 4 positions'
        self.V = V
        self.H = H
        self.n_galaxies = len(galaxies)
        self.galaxies = galaxies
        self.prelocated_positions: set[Pos] = {pos: i for i, galaxy in enumerate(galaxies) for pos in galaxy}

        self.model = cp_model.CpModel()
        self.pos_to_galaxy: dict[Pos, dict[int, cp_model.IntVar]] = {p: {} for p in get_all_pos(V, H)}  # each position can be part of exactly one out of many possible galaxies
        self.allocated_pairs: set[tuple[Pos, Pos]] = set()  # each pair is allocated to exactly one galaxy

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for i in range(self.n_galaxies):
            galaxy = self.galaxies[i]
            if len(galaxy) == 1:
                p1, p2 = galaxy[0], galaxy[0]
            elif len(galaxy) == 2:
                p1, p2 = galaxy[0], galaxy[1]
            elif len(galaxy) == 4:
                p1, p2 = galaxy[0], galaxy[3]  # [1] and [2] will be linked with symmetry
            self.expand_galaxy(p1, p2, i)

    def expand_galaxy(self, p1: Pos, p2: Pos, galaxy_idx: int):
        if (p1, p2) in self.allocated_pairs or (p2, p1) in self.allocated_pairs:
            return
        if p1 in self.prelocated_positions and self.prelocated_positions[p1] != galaxy_idx:
            return
        if p2 in self.prelocated_positions and self.prelocated_positions[p2] != galaxy_idx:
            return
        if not in_bounds(p1, self.V, self.H) or not in_bounds(p2, self.V, self.H):
            return
        self.bind_pair(p1, p2, galaxy_idx)
        # symmetrically expand the galaxy until illegal position is hit
        for direction in [Direction.RIGHT, Direction.UP, Direction.DOWN, Direction.LEFT]:
            symmetrical_direction = get_opposite_direction(direction)
            new_p1 = get_next_pos(p1, direction)
            new_p2 = get_next_pos(p2, symmetrical_direction)
            self.expand_galaxy(new_p1, new_p2, galaxy_idx)

    def bind_pair(self, p1: Pos, p2: Pos, galaxy_idx: int):
        assert galaxy_idx not in self.pos_to_galaxy[p1], f'p1={p1} already has galaxy idx={galaxy_idx}'
        assert galaxy_idx not in self.pos_to_galaxy[p2], f'p2={p2} already has galaxy idx={galaxy_idx}'
        self.allocated_pairs.add((p1, p2))
        v1 = self.model.NewBoolVar(f'{p1}:{galaxy_idx}')
        v2 = self.model.NewBoolVar(f'{p2}:{galaxy_idx}')
        self.model.Add(v1 == v2)
        self.pos_to_galaxy[p1][galaxy_idx] = v1
        self.pos_to_galaxy[p2][galaxy_idx] = v2

    def add_all_constraints(self):
        galaxy_vars = {}
        for pos in get_all_pos(self.V, self.H):
            pos_vars = list(self.pos_to_galaxy[pos].values())
            self.model.AddExactlyOne(pos_vars)
            for galaxy_idx, v in self.pos_to_galaxy[pos].items():
                galaxy_vars.setdefault(galaxy_idx, {})[pos] = v
        for pos_vars in galaxy_vars.values():
            force_connected_component(self.model, pos_vars)


    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, int] = {}
            for pos, galaxy_vars in board.pos_to_galaxy.items():
                for galaxy_idx, var in galaxy_vars.items():  # every pos is part of exactly one galaxy
                    if solver.Value(var) == 1:
                        assignment[pos] = galaxy_idx
                        break
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.full((self.V, self.H), ' ', dtype=object)
            for pos in get_all_pos(self.V, self.H):
                set_char(res, pos, single_res.assignment[pos])
            print(combined_function(self.V, self.H,
                cell_flags=id_board_to_wall_fn(res),
                center_char=lambda r, c: '.' if (Pos(x=c, y=r) in self.prelocated_positions) else ' '))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
