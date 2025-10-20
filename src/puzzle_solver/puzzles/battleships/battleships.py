from enum import Enum
from dataclasses import dataclass, field
from typing import Optional
import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, get_neighbors8, set_char, get_row_pos, get_col_pos, get_pos, in_bounds
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution, or_constraint

@dataclass
class Ship:
    is_active: cp_model.IntVar
    length: int
    top_left_pos: Pos
    body: set[Pos]
    water: set[Pos]
    mid_body: set[Pos] = field(default_factory=set)
    top_tip: Optional[Pos] = field(default=None)
    bottom_tip: Optional[Pos] = field(default=None)
    left_tip: Optional[Pos] = field(default=None)
    right_tip: Optional[Pos] = field(default=None)

class Board:
    def __init__(self, board: np.array, top: np.array, side: np.array, ship_counts: dict[int, int]):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        self.V = board.shape[0]
        self.H = board.shape[1]
        assert top.ndim == 1 and top.shape[0] == self.H, 'top must be a 1d array of length board width'
        assert side.ndim == 1 and side.shape[0] == self.V, 'side must be a 1d array of length board height'
        assert all((str(c.item()) in [' ', 'W', 'O', 'S', 'U', 'D', 'L', 'R'] for c in np.nditer(board))), 'board must contain only spaces, W, O, S, U, D, L, R'
        self.board = board
        self.top = top
        self.side = side
        self.ship_counts = ship_counts

        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}
        self.shipyard: list[Ship] = []  # will contain every possible ship based on ship counts

        self.create_vars()
        self.init_shipyard()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[pos] = self.model.NewBoolVar(f'{pos}:is_ship')

    def get_ship(self, pos: Pos, length: int, orientation: str) -> Optional[Ship]:
        assert orientation in ['horizontal', 'vertical'], 'orientation must be horizontal or vertical'
        if length == 1:
            body = {pos}
            top_tip = None
            bottom_tip = None
            left_tip = None
            right_tip = None
        elif orientation == 'horizontal':
            body = set(get_pos(x=x, y=pos.y) for x in range(pos.x, pos.x + length))
            top_tip = None
            bottom_tip = None
            left_tip = pos
            right_tip = get_pos(x=pos.x + length - 1, y=pos.y)
        else:
            body = set(get_pos(x=pos.x, y=y) for y in range(pos.y, pos.y + length))
            left_tip = None
            right_tip = None
            top_tip = pos
            bottom_tip = get_pos(x=pos.x, y=pos.y + length - 1)
        if any(not in_bounds(p, self.V, self.H) for p in body):
            return None
        water = set(p for pos in body for p in get_neighbors8(pos, self.V, self.H))
        water -= body
        mid_body = body - {top_tip, bottom_tip, left_tip, right_tip} if length > 1 else set()
        return Ship(
            is_active=self.model.NewBoolVar(f'{pos}:is_active'),
            length=length,
            top_left_pos=pos,
            body=body,
            water=water,
            mid_body=mid_body,
            top_tip=top_tip,
            bottom_tip=bottom_tip,
            left_tip=left_tip,
            right_tip=right_tip,
        )

    def init_shipyard(self):
        for length in self.ship_counts.keys():
            for pos in get_all_pos(self.V, self.H):
                for orientation in ['horizontal', 'vertical']:
                    if length == 1 and orientation == 'vertical':  # prevent double counting 1-length ships
                        continue
                    ship = self.get_ship(pos, length, orientation)
                    if ship is not None:
                        self.shipyard.append(ship)

    def add_all_constraints(self):
        # ship and cells linked
        for ship in self.shipyard:
            for pos in ship.body:
                self.model.Add(self.model_vars[pos] == 1).OnlyEnforceIf(ship.is_active)
            for pos in ship.water:
                self.model.Add(self.model_vars[pos] == 0).OnlyEnforceIf(ship.is_active)
        # constrain the cell to be an OR of all the ships that can be placed at that position
        for pos in get_all_pos(self.V, self.H):
            or_constraint(self.model, self.model_vars[pos], [ship.is_active for ship in self.shipyard if pos in ship.body])
        # force ship counts
        for length, count in self.ship_counts.items():
            self.constrain_ship_counts([ship for ship in self.shipyard if ship.length == length], count)
        # force initial board placement
        for pos in get_all_pos(self.V, self.H):
            c = get_char(self.board, pos)
            if c == 'S':  # single-length ship
                self.constrain_ship_counts([ship for ship in self.shipyard if ship.length == 1 and ship.top_left_pos == pos], 1)
            elif c == 'W':  # water
                self.model.Add(self.model_vars[pos] == 0)
            elif c == 'O':  # mid-body of a ship
                self.constrain_ship_counts([ship for ship in self.shipyard if pos in ship.mid_body], 1)
            elif c == 'U':  # top tip of a ship
                self.constrain_ship_counts([ship for ship in self.shipyard if ship.top_tip == pos], 1)
            elif c == 'D':  # bottom tip of a ship
                self.constrain_ship_counts([ship for ship in self.shipyard if ship.bottom_tip == pos], 1)
            elif c == 'L':  # left tip of a ship
                self.constrain_ship_counts([ship for ship in self.shipyard if ship.left_tip == pos], 1)
            elif c == 'R':  # right tip of a ship
                self.constrain_ship_counts([ship for ship in self.shipyard if ship.right_tip == pos], 1)
            elif c == ' ':  # empty cell
                pass
            else:
                raise ValueError(f'invalid character: {c}')
        # force the top and side counts
        for row in range(self.V):
            self.model.Add(sum([self.model_vars[p] for p in get_row_pos(row, self.H)]) == self.side[row])
        for col in range(self.H):
            self.model.Add(sum([self.model_vars[p] for p in get_col_pos(col, self.V)]) == self.top[col])

    def constrain_ship_counts(self, ships: list[Ship], count: int):
        self.model.Add(sum([ship.is_active for ship in ships]) == count)

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, int] = {}
            for pos, var in board.model_vars.items():
                assignment[pos] = solver.Value(var)
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.full((self.V, self.H), ' ', dtype=str)
            for pos, val in single_res.assignment.items():
                c = 'S' if val == 1 else ' '
                set_char(res, pos, c)
            print(res)

        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
