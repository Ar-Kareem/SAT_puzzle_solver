from collections import defaultdict

import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Direction, Pos, get_all_pos, get_next_pos, get_char, in_bounds, set_char, get_pos, get_opposite_direction
from puzzle_solver.core.utils_ortools import generic_solve_all, force_connected_component, and_constraint, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


def get_ray(pos: Pos, V: int, H: int, direction: Direction) -> list[Pos]:
    out = []
    while True:
        out.append(pos)
        pos = get_next_pos(pos, direction)
        if not in_bounds(pos, V, H):
            break
    return out


class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all((c.item().strip() == '') or (str(c.item())[:-1].isdecimal() and c.item()[-1].upper() in ['B', 'W']) for c in np.nditer(board)), 'board must contain only space or digits and B/W'
        self.V, self.H = board.shape
        self.board = board
        self.board_numbers: dict[Pos, int] = {}
        self.board_colors: dict[Pos, str] = {}
        for pos in get_all_pos(self.V, self.H):
            c = get_char(board, pos)
            if c.strip() == '':
                continue
            self.board_numbers[pos] = int(c[:-1])
            self.board_colors[pos] = c[-1].upper()

        self.model = cp_model.CpModel()
        self.cell_active: dict[Pos, cp_model.IntVar] = {}
        self.cell_direction: dict[tuple[Pos, Direction], cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.cell_active[pos] = self.model.NewBoolVar(f'{pos}')
            for direction in Direction:
                neighbor = get_next_pos(pos, direction)
                opposite_direction = get_opposite_direction(direction)
                if not in_bounds(neighbor, self.V, self.H):
                    self.cell_direction[(pos, direction)] = self.model.NewConstant(0)
                    continue
                if (neighbor, opposite_direction) in self.cell_direction:
                    self.cell_direction[(pos, direction)] = self.cell_direction[(neighbor, opposite_direction)]
                else:
                    self.cell_direction[(pos, direction)] = self.model.NewBoolVar(f'{pos}-{neighbor}')

    def add_all_constraints(self):
        for pos in get_all_pos(self.V, self.H):
            s = sum([self.cell_direction[(pos, direction)] for direction in Direction])
            self.model.Add(s == 2).OnlyEnforceIf(self.cell_active[pos])
            self.model.Add(s == 0).OnlyEnforceIf(self.cell_active[pos].Not())
            if pos not in self.board_numbers:
                continue
            self.enforce_corner_color_and_number(pos, self.board_colors[pos], self.board_numbers[pos])  # enforce colors and number
        self.force_connected_component()  # enforce single connected component

    def enforce_corner_color_and_number(self, pos: Pos, pos_color: str, pos_number: int):
        assert pos_color in ['W', 'B'] and pos_number > 0, f'Invalid color or number: {pos_color}, {pos_number}'
        self.model.Add(self.cell_active[pos] == 1)
        if pos_color == 'W':  # White circles must be passed through in a straight line
            self.model.Add(self.cell_direction[(pos, Direction.RIGHT)] == self.cell_direction[(pos, Direction.LEFT)])
            self.model.Add(self.cell_direction[(pos, Direction.DOWN)] == self.cell_direction[(pos, Direction.UP)])
        elif pos_color == 'B':  # Black circles must be turned upon
            self.model.Add(self.cell_direction[(pos, Direction.RIGHT)] == 0).OnlyEnforceIf([self.cell_direction[(pos, Direction.LEFT)]])
            self.model.Add(self.cell_direction[(pos, Direction.LEFT)] == 0).OnlyEnforceIf([self.cell_direction[(pos, Direction.RIGHT)]])
            self.model.Add(self.cell_direction[(pos, Direction.DOWN)] == 0).OnlyEnforceIf([self.cell_direction[(pos, Direction.UP)]])
            self.model.Add(self.cell_direction[(pos, Direction.UP)] == 0).OnlyEnforceIf([self.cell_direction[(pos, Direction.DOWN)]])
        else:
            raise ValueError(f'Invalid color: {pos_color}')
        vis_vars: list[cp_model.IntVar] = []  # The numbers in the circles show the sum of the lengths of the 2 straight lines going out of that circle.
        for direction in Direction:  # Build visibility chains in four direction
            ray = get_ray(pos, self.V, self.H, direction)  # cells outward
            for idx in range(len(ray)):
                v = self.model.NewBoolVar(f"vis[{pos}]->({direction.name})[{idx}]")
                and_constraint(self.model, target=v, cs=[self.cell_direction[(p, direction)] for p in ray[:idx+1]])
                vis_vars.append(v)
        self.model.Add(sum(vis_vars) == pos_number)

    def force_connected_component(self):
        def is_neighbor(pd1: tuple[Pos, Direction], pd2: tuple[Pos, Direction]) -> bool:
            p1, d1 = pd1
            p2, d2 = pd2
            if p1 == p2 and d1 != d2:  # same position, different direction, is neighbor
                return True
            if get_next_pos(p1, d1) == p2 and d2 == get_opposite_direction(d1):
                return True
            return False
        force_connected_component(self.model, self.cell_direction, is_neighbor=is_neighbor)

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, str] = defaultdict(str)
            for (pos, direction), var in board.cell_direction.items():
                assignment[pos] += direction.name[0] if solver.BooleanValue(var) else ''
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            output_board = np.full((self.V, self.H), '', dtype=object)
            for pos in get_all_pos(self.V, self.H):
                if get_char(self.board, pos)[-1] in ['B', 'W']:  # if the main board has a white or black pearl, put it in the output
                    set_char(output_board, pos, get_char(self.board, pos))
                if not single_res.assignment[pos].strip():  # if the cell does not the line through it, put a dot
                    set_char(output_board, pos, '.')
            print(combined_function(self.V, self.H, show_grid=False, special_content=lambda r, c: single_res.assignment[get_pos(x=c, y=r)], center_char=lambda r, c: output_board[r, c]))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
