import json
from dataclasses import dataclass
import time

import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Direction, Pos, get_all_pos, get_neighbors4, get_next_pos, get_char, in_bounds
from puzzle_solver.core.utils_ortools import generic_solve_all, force_connected_component, and_constraint
from puzzle_solver.core.utils_visualizer import combined_function


@dataclass(frozen=True)
class SingleSolution:
    assignment: dict[tuple[Pos, Pos], int]

    def get_hashable_solution(self) -> str:
        result = []
        for (pos, neighbor), v in self.assignment.items():
            result.append((pos.x, pos.y, neighbor.x, neighbor.y, v))
        return json.dumps(result, sort_keys=True)


def get_ray(pos: Pos, V: int, H: int, direction: Direction) -> list[tuple[Pos, Pos]]:
    out = []
    prev_pos = pos
    while True:
        pos = get_next_pos(pos, direction)
        if not in_bounds(pos, V, H):
            break
        out.append((prev_pos, pos))
        prev_pos = pos
    return out


class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all((c.item().strip() == '') or (str(c.item())[:-1].isdecimal() and c.item()[-1].upper() in ['B', 'W']) for c in np.nditer(board)), 'board must contain only space or digits and B/W'

        self.V, self.H = board.shape
        self.board_numbers: dict[Pos, int] = {}
        self.board_colors: dict[Pos, str] = {}
        for pos in get_all_pos(self.V, self.H):
            c = get_char(board, pos)
            if c.strip() == '':
                continue
            self.board_numbers[pos] = int(c[:-1])
            self.board_colors[pos] = c[-1].upper()
        self.model = cp_model.CpModel()
        self.edge_vars: dict[tuple[Pos, Pos], cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            for neighbor in get_neighbors4(pos, self.V, self.H):
                if (neighbor, pos) in self.edge_vars:  # already added in opposite direction
                    self.edge_vars[(pos, neighbor)] = self.edge_vars[(neighbor, pos)]
                else:  # new edge
                    self.edge_vars[(pos, neighbor)] = self.model.NewBoolVar(f'{pos}-{neighbor}')

    def add_all_constraints(self):
        # each corners must have either 0 or 2 neighbors
        for pos in get_all_pos(self.V, self.H):
            corner_connections = [self.edge_vars[(pos, n)] for n in get_neighbors4(pos, self.V, self.H)]
            if pos not in self.board_numbers:  # no color, either 0 or 2 edges
                self.model.AddLinearExpressionInDomain(sum(corner_connections), cp_model.Domain.FromValues([0, 2]))
            else:  # color, must have exactly 2 edges
                self.model.Add(sum(corner_connections) == 2)

        # enforce colors
        for pos in get_all_pos(self.V, self.H):
            if pos not in self.board_numbers:
                continue
            self.enforce_corner_color(pos, self.board_colors[pos])
            self.enforce_corner_number(pos, self.board_numbers[pos])

        # enforce single connected component
        def is_neighbor(edge1: tuple[Pos, Pos], edge2: tuple[Pos, Pos]) -> bool:
            return any(c1 == c2 for c1 in edge1 for c2 in edge2)
        force_connected_component(self.model, self.edge_vars, is_neighbor=is_neighbor)

    def enforce_corner_color(self, pos: Pos, pos_color: str):
        assert pos_color in ['W', 'B'], f'Invalid color: {pos_color}'
        pos_r = get_next_pos(pos, Direction.RIGHT)
        var_r = self.edge_vars[(pos, pos_r)] if (pos, pos_r) in self.edge_vars else False
        pos_d = get_next_pos(pos, Direction.DOWN)
        var_d = self.edge_vars[(pos, pos_d)] if (pos, pos_d) in self.edge_vars else False
        pos_l = get_next_pos(pos, Direction.LEFT)
        var_l = self.edge_vars[(pos, pos_l)] if (pos, pos_l) in self.edge_vars else False
        pos_u = get_next_pos(pos, Direction.UP)
        var_u = self.edge_vars[(pos, pos_u)] if (pos, pos_u) in self.edge_vars else False
        if pos_color == 'W':  # White circles must be passed through in a straight line
            self.model.Add(var_r == var_l)
            self.model.Add(var_u == var_d)
        elif pos_color == 'B':  # Black circles must be turned upon
            self.model.Add(var_r == 0).OnlyEnforceIf([var_l])
            self.model.Add(var_l == 0).OnlyEnforceIf([var_r])
            self.model.Add(var_u == 0).OnlyEnforceIf([var_d])
            self.model.Add(var_d == 0).OnlyEnforceIf([var_u])
        else:
            raise ValueError(f'Invalid color: {pos_color}')

    def enforce_corner_number(self, pos: Pos, pos_number: int):
        # The numbers in the circles show the sum of the lengths of the 2 straight lines going out of that circle.
        # Build visibility chains per direction (exclude self)
        vis_vars: list[cp_model.IntVar] = []
        for direction in Direction:
            rays = get_ray(pos, self.V, self.H, direction)  # cells outward
            if not rays:
                continue
            # Chain: v0 = w[ray[0]]; vt = w[ray[t]] & vt-1
            prev = None
            for idx, (pos1, pos2) in enumerate(rays):
                v = self.model.NewBoolVar(f"vis[{pos1}-{pos2}]->({direction.name})[{idx}]")
                vis_vars.append(v)
                if idx == 0:
                    # v0 == w[cell]
                    self.model.Add(v == self.edge_vars[(pos1, pos2)])
                else:
                    and_constraint(self.model, target=v, cs=[self.edge_vars[(pos1, pos2)], prev])
                prev = v
        self.model.Add(sum(vis_vars) == pos_number)


    def solve_and_print(self, verbose: bool = True):
        tic = time.time()
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[tuple[Pos, Pos], int] = {}
            for (pos, neighbor), var in board.edge_vars.items():
                assignment[(pos, neighbor)] = solver.Value(var)
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            nonlocal tic
            print(f"Solution found in {time.time() - tic:.2f} seconds")
            tic = time.time()
            res = np.full((self.V - 1, self.H - 1), ' ', dtype=object)
            for (pos, neighbor), v in single_res.assignment.items():
                if v == 0:
                    continue
                min_x = min(pos.x, neighbor.x)
                min_y = min(pos.y, neighbor.y)
                dx = abs(pos.x - neighbor.x)
                dy = abs(pos.y - neighbor.y)
                if min_x == self.H - 1:  # only way to get right
                    res[min_y][min_x - 1] += 'R'
                elif min_y == self.V - 1:  # only way to get down
                    res[min_y - 1][min_x] += 'D'
                elif dx == 1:
                    res[min_y][min_x] += 'U'
                elif dy == 1:
                    res[min_y][min_x] += 'L'
                else:
                    raise ValueError(f'Invalid position: {pos} and {neighbor}')
            print(combined_function(self.V - 1, self.H - 1, cell_flags=lambda r, c: res[r, c], center_char=lambda r, c: '.'))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
