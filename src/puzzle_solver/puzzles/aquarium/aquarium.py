import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, get_neighbors4, get_row_pos, get_col_pos, get_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function, id_board_to_wall_fn


def _sanity_check(board: np.array):  # percolation check
    V, H = board.shape
    visited: set[Pos] = set()
    finished_islands: set[int] = set()
    def dfs(pos: Pos, target_i: int):
        if pos in visited:
            return
        visited.add(pos)
        for neighbor in get_neighbors4(pos, V, H):
            if neighbor in visited:
                continue
            neighbor_i = int(get_char(board, neighbor))
            if neighbor_i == target_i:
                dfs(neighbor, target_i)
    for pos in get_all_pos(V, H):
        if pos in visited:
            continue
        current_i = int(get_char(board, pos))
        assert current_i not in finished_islands, f'island {current_i} already finished'
        dfs(pos, current_i)
        finished_islands.add(current_i)
    assert len(finished_islands) == len(set(board.flatten())), 'board is not connected'

class Board:
    def __init__(self, board: np.array, top: np.array, side: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        _sanity_check(board)
        self.V, self.H = board.shape
        assert top.ndim == 1 and top.shape[0] == self.H, 'top must be a 1d array of length board width'
        assert side.ndim == 1 and side.shape[0] == self.V, 'side must be a 1d array of length board height'
        assert all((str(c.item()).isdecimal() for c in np.nditer(board))), 'board must contain only digits'
        self.board = board
        self.top = top
        self.side = side
        self.aquarium_numbers = set([int(c.item()) for c in np.nditer(board)])
        self.aquariums = {i: [pos for pos in get_all_pos(self.V, self.H) if int(get_char(self.board, pos)) == i] for i in self.aquarium_numbers}
        self.aquariums_exist_in_row: dict[int, set[int]] = {aq_i: set() for aq_i in self.aquarium_numbers}
        for aq_i in self.aquarium_numbers:
            for row in range(self.V):
                if any(pos.y == row for pos in self.aquariums[aq_i]):
                    self.aquariums_exist_in_row[aq_i].add(row)

        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}
        self.is_aquarium_here: dict[tuple[int, int], cp_model.IntVar] = {}  # is the aquarium here?

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[pos] = self.model.NewBoolVar(f'{pos}')
        for aq_i in self.aquarium_numbers:
            for row in self.aquariums_exist_in_row[aq_i]:
                self.is_aquarium_here[row, aq_i] = self.model.NewBoolVar(f'{row}:{aq_i}')

    def add_all_constraints(self):
        for aq_i in self.aquarium_numbers:
            for pos in self.aquariums[aq_i]:
                self.model.Add(self.is_aquarium_here[pos.y, aq_i] == 1).OnlyEnforceIf(self.model_vars[pos])
        # aquarium always start from the bottom
        for aq_i in self.aquarium_numbers:
            for row in self.aquariums_exist_in_row[aq_i]:
                if row + 1 not in self.aquariums_exist_in_row[aq_i]:  # (row + 1) is below (row) thus currently (row) is the bottom of the aquarium
                    continue
                self.model.Add(self.is_aquarium_here[row + 1, aq_i] == 1).OnlyEnforceIf(self.is_aquarium_here[row, aq_i])
        for row in range(self.V):
            for aq_i in self.aquarium_numbers:
                aq_i_row_pos = [pos for pos in self.aquariums[aq_i] if pos.y == row]
                for pos in aq_i_row_pos:
                    # if the aquarium is here, all the squares in the row of this aquarium must be filled
                    self.model.Add(self.model_vars[pos] == 1).OnlyEnforceIf(self.is_aquarium_here[row, aq_i])
                # if the aquarium is here, at least one square in the row of this aquarium must be filled
                if len(aq_i_row_pos) > 0:
                    self.model.Add(sum([self.model_vars[pos] for pos in aq_i_row_pos]) == len(aq_i_row_pos)).OnlyEnforceIf(self.is_aquarium_here[row, aq_i])
                    self.model.Add(sum([self.model_vars[pos] for pos in aq_i_row_pos]) == 0).OnlyEnforceIf(self.is_aquarium_here[row, aq_i].Not())
        # force the top and side constraints
        for col in range(self.H):
            self.model.Add(sum([self.model_vars[pos] for pos in get_col_pos(col, self.V)]) == self.top[col])
        for row in range(self.V):
            self.model.Add(sum([self.model_vars[pos] for pos in get_row_pos(row, self.H)]) == self.side[row])

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: solver.value(board.model_vars[pos]) for pos in board.model_vars.keys()})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H, cell_flags=id_board_to_wall_fn(self.board), center_char=lambda r, c: 'O' if single_res.assignment[get_pos(x=c, y=r)] == 1 else ''))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose, max_solutions=99)
