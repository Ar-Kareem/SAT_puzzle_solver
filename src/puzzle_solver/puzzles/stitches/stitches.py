from typing import Union

import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, get_next_pos, Direction, get_row_pos, get_col_pos, in_bounds, get_opposite_direction, get_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution, and_constraint
from puzzle_solver.core.utils_visualizer import combined_function, id_board_to_wall_fn


class Board:
    def __init__(self, board: np.array, top: np.array, side: np.array, connection_count=1):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        self.V = board.shape[0]
        self.H = board.shape[1]
        assert top.ndim == 1 and top.shape[0] == self.H, 'top must be a 1d array of length board width'
        assert side.ndim == 1 and side.shape[0] == self.V, 'side must be a 1d array of length board height'
        assert all((str(c.item()).isdecimal() for c in np.nditer(board))), 'board must contain only digits'
        assert isinstance(connection_count, int) and connection_count >= 1, f'connection count must be int and >= 1, got {connection_count}'
        self.board = board
        self.top = top
        self.side = side
        self.connection_count = connection_count
        self.top_empties = [self.H - i for i in self.top]
        self.side_empties = [self.V - i for i in self.side]
        self.block_numbers = set([int(c.item()) for c in np.nditer(board)])
        self.blocks = {i: [pos for pos in get_all_pos(self.V, self.H) if int(get_char(self.board, pos)) == i] for i in self.block_numbers}
        # keys are (block_i, block_j) where block_i < block_j to avoid double counting
        # values are sets of (pos_a, direction_a, pos_b, direction_b) where the two blocks meet
        self.block_neighbors: dict[tuple[int, int], set[tuple[Pos, Direction, Pos, Direction]]] = {}
        self.valid_stitches: set[tuple[Pos, Pos]] = set()  # records all pairs of positions that can have a stitch
        for pos in get_all_pos(self.V, self.H):
            block_i = int(get_char(self.board, pos))
            for direction in Direction:
                neighbor = get_next_pos(pos, direction)
                if not in_bounds(neighbor, self.V, self.H):
                    continue
                block_j = int(get_char(self.board, neighbor))
                if block_i < block_j:  # avoid double counting
                    opposite_direction = get_opposite_direction(direction)
                    self.block_neighbors.setdefault((block_i, block_j), set()).add((pos, direction, neighbor, opposite_direction))
                    self.valid_stitches.add((pos, neighbor))
                    self.valid_stitches.add((neighbor, pos))

        self.model = cp_model.CpModel()
        self.model_vars: dict[tuple[Pos, Union[Direction, None]], cp_model.IntVar] = {}
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            for direction in Direction:
                self.model_vars[(pos, direction)] = self.model.NewBoolVar(f'{pos}:{direction}')
            self.model_vars[(pos, None)] = self.model.NewBoolVar(f'{pos}:empty')

    def add_all_constraints(self):
        # every position has exactly 1 state
        for pos in get_all_pos(self.V, self.H):
            state = [self.model_vars[(pos, direction)] for direction in Direction]
            state.append(self.model_vars[(pos, None)])
            self.model.AddExactlyOne(state)
        # If a position points at X (and this is a valid pair) then X has to point at me
        for pos in get_all_pos(self.V, self.H):
            for direction in Direction:
                neighbor = get_next_pos(pos, direction)
                if not in_bounds(neighbor, self.V, self.H) or (pos, neighbor) not in self.valid_stitches:  # this is not a valid stitch
                    self.model.Add(self.model_vars[(pos, direction)] == 0)
                    continue
                opposite_direction = get_opposite_direction(direction)
                self.model.Add(self.model_vars[(pos, direction)] == self.model_vars[(neighbor, opposite_direction)])

        # all blocks connected exactly N times (N usually 1 but can be 2 or 3)
        for connections in self.block_neighbors.values():
            is_connected_list = []
            for pos_a, direction_a, pos_b, direction_b in connections:
                v = self.model.NewBoolVar(f'{pos_a}:{direction_a}->{pos_b}:{direction_b}')
                and_constraint(self.model, v, [self.model_vars[pos_a, direction_a], self.model_vars[pos_b, direction_b]])
                is_connected_list.append(v)
            self.model.Add(sum(is_connected_list) == self.connection_count)

        # sums of top and side must match
        for col in range(self.H):
            self.model.Add(sum([self.model_vars[pos, None] for pos in get_col_pos(col, self.V)]) == self.top_empties[col])
        for row in range(self.V):
            self.model.Add(sum([self.model_vars[pos, None] for pos in get_row_pos(row, self.H)]) == self.side_empties[row])

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: direction.name[0] if direction is not None else ' ' for (pos, direction), var in board.model_vars.items() if solver.Value(var) == 1 and direction is not None})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H,
                cell_flags=id_board_to_wall_fn(self.board),
                special_content=lambda r, c: single_res.assignment.get(get_pos(x=c, y=r), ''),
                center_char=lambda r, c: 'O' if get_pos(x=c, y=r) in single_res.assignment else '.'))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose, max_solutions=9)
