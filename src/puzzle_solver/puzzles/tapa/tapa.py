from typing import Union
from itertools import combinations

import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Direction8, Pos, get_all_pos, set_char, get_char, in_bounds, Direction, get_next_pos, get_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution, force_connected_component
from puzzle_solver.core.utils_visualizer import render_shaded_grid


def rotated_assignments_N_nums(Xs: tuple[int, ...], target_length: int = 8) -> set[tuple[bool, ...]]:
    """ Given Xs = [X1, X2, ..., Xm] (each Xi >= 1), build all unique length-`target_length`
        boolean lists of the form: [ True*X1, False*N1, True*X2, False*N2, ..., True*Xm, False*Nm ]
        where each Ni >= 1 and sum(Xs) + sum(Ni) = target_length,
        including all `target_length` wrap-around rotations, de-duplicated.
    """
    assert len(Xs) >= 1, "Xs must have at least one block length."
    assert all(x >= 1 for x in Xs), "All Xi must be >= 1."
    assert sum(Xs) + len(Xs) <= target_length, f"sum(Xs) + len(Xs) <= target_length required; got {sum(Xs)} + {len(Xs)} > {target_length}"
    num_zero_blocks = len(Xs)
    total_zeros = target_length - sum(Xs)
    seen: set[tuple[bool, ...]] = set()
    for cut_positions in combinations(range(1, total_zeros), num_zero_blocks - 1):
        cut_positions = (*cut_positions, total_zeros)
        Ns = [cut_positions[0]]  # length of zero blocks
        for i in range(1, len(cut_positions)):
            Ns.append(cut_positions[i] - cut_positions[i - 1])
        base: list[bool] = []
        for x, n in zip(Xs, Ns):
            base.extend([True] * x)
            base.extend([False] * n)
        for dx in range(target_length):  # all rotations (wrap-around)
            rot = tuple(base[dx:] + base[:dx])
            seen.add(rot)
    return seen


class Board:
    def __init__(self, board: np.array, separator: str = '/'):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all(all(str(c).strip().isdecimal() or str(c).strip() == '' for c in cell.item().split(separator)) for cell in np.nditer(board)), 'board must contain only digits and separator'
        self.V, self.H = board.shape
        self.board = board
        self.separator = separator
        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[pos] = self.model.NewBoolVar(f'{pos}')

    def add_all_constraints(self):
        # 2x2 blacks are not allowed
        for pos in get_all_pos(self.V, self.H):
            tl = pos
            tr = get_next_pos(pos, Direction.RIGHT)
            bl = get_next_pos(pos, Direction.DOWN)
            br = get_next_pos(bl, Direction.RIGHT)
            if any(not in_bounds(p, self.V, self.H) for p in [tl, tr, bl, br]):
                continue
            self.model.AddBoolOr([self.model_vars[tl].Not(), self.model_vars[tr].Not(), self.model_vars[bl].Not(), self.model_vars[br].Not()])
        for pos in get_all_pos(self.V, self.H):
            c = get_char(self.board, pos)
            if c.strip() == '':
                continue
            clue = tuple(int(x.strip()) for x in c.split(self.separator))
            self.model.Add(self.model_vars[pos] == 0)  # clue cannot be black
            self.enforce_clue(pos, clue)  # each clue must be satisfied
        # all blacks are connected
        force_connected_component(self.model, self.model_vars)

    def enforce_clue(self, pos: Pos, clue: Union[int, tuple[int, int]]):
        neighbors = []
        for direction in [Direction8.UP, Direction8.UP_RIGHT, Direction8.RIGHT, Direction8.DOWN_RIGHT, Direction8.DOWN, Direction8.DOWN_LEFT, Direction8.LEFT, Direction8.UP_LEFT]:
            n = get_next_pos(pos, direction)
            neighbors.append(self.model_vars[n] if in_bounds(n, self.V, self.H) else self.model.NewConstant(False))
        valid_assignments = rotated_assignments_N_nums(Xs=clue)
        self.model.AddAllowedAssignments(neighbors, valid_assignments)

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, int] = {}
            for pos, var in board.model_vars.items():
                assignment[pos] = solver.Value(var)
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            board_justified = np.full((self.V, self.H), ' ', dtype=object)
            for pos in get_all_pos(self.V, self.H):
                c = get_char(self.board, pos).strip()
                if len(c) > 3:
                    c = '...'
                set_char(board_justified, pos, ' ' * (2 - len(c)) + c)
            print(render_shaded_grid(self.V, self.H, lambda r, c: single_res.assignment[get_pos(x=c, y=r)] == 1, empty_text=lambda r, c: str(board_justified[r, c])))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose, max_solutions=5)
