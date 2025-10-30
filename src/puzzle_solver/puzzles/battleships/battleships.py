from dataclasses import dataclass
from collections import defaultdict
from typing import Optional

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, get_neighbors8, get_row_pos, get_col_pos, get_pos, in_bounds
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


@dataclass
class Ship:
    is_active: cp_model.IntVar
    length: int
    top_left_pos: Pos
    body: set[Pos]
    water: set[Pos]
    mid_body: set[Pos]
    top_tip: Optional[Pos]
    bottom_tip: Optional[Pos]
    left_tip: Optional[Pos]
    right_tip: Optional[Pos]

class Board:
    def __init__(self, board: np.array, top: np.array, side: np.array, ship_counts: dict[int, int]):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        self.V, self.H = board.shape
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
        elif orientation == 'vertical':
            body = set(get_pos(x=pos.x, y=y) for y in range(pos.y, pos.y + length))
            left_tip = None
            right_tip = None
            top_tip = pos
            bottom_tip = get_pos(x=pos.x, y=pos.y + length - 1)
        else:
            raise ValueError(f'invalid orientation: {orientation}')
        if any(not in_bounds(p, self.V, self.H) for p in body):
            return None
        water = set(p for pos in body for p in get_neighbors8(pos, self.V, self.H)) - body
        mid_body = body - {top_tip, bottom_tip, left_tip, right_tip} if length > 1 else set()
        return Ship(
            is_active=self.model.NewBoolVar(f'{pos}:is_active'), length=length,
            top_left_pos=pos, body=body, mid_body=mid_body, water=water,
            top_tip=top_tip, bottom_tip=bottom_tip, left_tip=left_tip, right_tip=right_tip,
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
        # if a ship is active then all its body is active and all its water is inactive
        pos_to_ships: dict[Pos, list[Ship]] = defaultdict(list)
        for ship in self.shipyard:
            for pos in ship.body:
                self.model.Add(self.model_vars[pos] == 1).OnlyEnforceIf(ship.is_active)
                pos_to_ships[pos].append(ship)
            for pos in ship.water:
                self.model.Add(self.model_vars[pos] == 0).OnlyEnforceIf(ship.is_active)
        # if a pos is active then exactly one ship can be placed at that position
        for pos in get_all_pos(self.V, self.H):
            self.model.Add(lxp.Sum([ship.is_active for ship in pos_to_ships[pos]]) == 1).OnlyEnforceIf(self.model_vars[pos])
        # force ship counts
        for length, count in self.ship_counts.items():
            self.model.Add(lxp.Sum([ship.is_active for ship in self.shipyard if ship.length == length]) == count)
        # force the initial board placement
        for pos in get_all_pos(self.V, self.H):
            c = get_char(self.board, pos)
            if c == 'S':  # single-length ship
                self.model.Add(lxp.Sum([ship.is_active for ship in self.shipyard if ship.length == 1 and ship.top_left_pos == pos]) == 1)
            elif c == 'W':  # water
                self.model.Add(self.model_vars[pos] == 0)
            elif c == 'O':  # mid-body of a ship
                self.model.Add(lxp.Sum([ship.is_active for ship in self.shipyard if pos in ship.mid_body]) == 1)
            elif c == 'U':  # top tip of a ship
                self.model.Add(lxp.Sum([ship.is_active for ship in self.shipyard if ship.top_tip == pos]) == 1)
            elif c == 'D':  # bottom tip of a ship
                self.model.Add(lxp.Sum([ship.is_active for ship in self.shipyard if ship.bottom_tip == pos]) == 1)
            elif c == 'L':  # left tip of a ship
                self.model.Add(lxp.Sum([ship.is_active for ship in self.shipyard if ship.left_tip == pos]) == 1)
            elif c == 'R':  # right tip of a ship
                self.model.Add(lxp.Sum([ship.is_active for ship in self.shipyard if ship.right_tip == pos]) == 1)
            elif c == ' ':  # empty cell
                pass
            else:
                raise ValueError(f'invalid character: {c}')
        for row in range(self.V):  # force the top counts
            self.model.Add(lxp.Sum([self.model_vars[p] for p in get_row_pos(row, self.H)]) == self.side[row])
        for col in range(self.H):  # force the side counts
            self.model.Add(lxp.Sum([self.model_vars[p] for p in get_col_pos(col, self.V)]) == self.top[col])

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: solver.Value(var) for pos, var in board.model_vars.items()})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H, is_shaded=lambda r, c: single_res.assignment[get_pos(x=c, y=r)] == 1))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
