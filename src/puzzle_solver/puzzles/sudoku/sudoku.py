from typing import Union, Optional
from collections import defaultdict

import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_pos, get_all_pos, get_char, set_char, get_row_pos, get_col_pos
from puzzle_solver.core.utils_ortools import and_constraint, generic_solve_all, or_constraint, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


def get_value(board: np.array, pos: Pos) -> Union[int, str]:
    c = get_char(board, pos).lower()
    if c == ' ':
        return c
    if str(c).isdecimal():
        return int(c)
    # a,b,... maps to 10,11,...
    return ord(c) - ord('a') + 10


def set_value(board: np.array, pos: Pos, value: Union[int, str]):
    if value == ' ':
        value = ' '
    elif value < 10:
        value = str(value)
    else:
        value = chr(value - 10 + ord('a'))
    set_char(board, pos, value)


def get_block_pos(i: int, Bv: int, Bh: int) -> list[Pos]:
    # Think: Bv=3 and Bh=4 while the board has 4 vertical blocks and 3 horizontal blocks
    top_left_x = (i%Bv)*Bh
    top_left_y = (i//Bv)*Bv
    return [get_pos(x=top_left_x + x, y=top_left_y + y) for x in range(Bh) for y in range(Bv)]


class Board:
    def __init__(self,
            board: np.array,
            constrain_blocks: bool = True,
            block_size: Optional[tuple[int, int]] = None,
            sandwich: Optional[dict[str, list[int]]] = None,
            unique_diagonal: bool = False,
            jigsaw: Optional[np.array] = None,
            killer: Optional[tuple[np.array, dict[str, int]]] = None,
            ):
        """
        board: 2d array of characters
        constrain_blocks: whether to constrain the blocks. If True, each block must contain all numbers from 1 to 9 exactly once.
        block_size: tuple of block size (vertical, horizontal). If not provided, the block size is the square root of the board size.
        sandwich: dictionary of sandwich clues (side, bottom). If provided, the sum of the values between 1 and 9 for each row and column is equal to the clue.
        unique_diagonal: whether to constrain the 2 diagonals to be unique. If True, each diagonal must contain all numbers from 1 to 9 exactly once.
        killer: tuple of (killer board, killer clues). If provided, the killer board must be a 2d array of ids of the killer blocks. The killer clues must be a dictionary of killer block ids to clues.
            Each numbers in a killer block must be unique and sum to the clue.
        """
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert board.shape[0] == board.shape[1], 'board must be square'
        assert all(isinstance(i.item(), str) and len(i.item()) == 1 and (i.item().isalnum() or i.item() == ' ') for i in np.nditer(board)), 'board must contain only alphanumeric characters or space'
        self.board = board
        self.V, self.H = board.shape
        self.L = max(self.V, self.H)
        self.constrain_blocks = constrain_blocks
        self.unique_diagonal = unique_diagonal
        self.sandwich = None
        self.jigsaw_id_to_pos = None
        self.killer = None

        if self.constrain_blocks:
            if block_size is None:
                B = np.sqrt(self.V)  # block size
                assert B.is_integer(), 'board size must be a perfect square or provide block_size'
                Bv, Bh = int(B), int(B)
            else:
                Bv, Bh = block_size
                assert Bv * Bh == self.V, 'block size must be a factor of board size'
            # can be different in 4x3 for example
            self.Bv = Bv
            self.Bh = Bh
            self.B = Bv * Bh  # block count
        else:
            assert block_size is None, 'cannot set block size if blocks are not constrained'

        if jigsaw is not None:
            if self.constrain_blocks:
                print('Warning: jigsaw and blocks are both constrained, are you sure you want to do this?')
            assert jigsaw.ndim == 2, f'jigsaw must be 2d, got {jigsaw.ndim}'
            assert jigsaw.shape[0] == self.V and jigsaw.shape[1] == self.H, 'jigsaw must be the same size as the board'
            assert all(isinstance(i.item(), str) and i.item().isdecimal() for i in np.nditer(jigsaw)), 'jigsaw must contain only digits or space'
            self.jigsaw_id_to_pos: dict[int, list[Pos]] = defaultdict(list)
            for pos in get_all_pos(self.V, self.H):
                v = get_char(jigsaw, pos)
                if v.isdecimal():
                    self.jigsaw_id_to_pos[int(v)].append(pos)
            assert all(len(pos_list) <= self.L for pos_list in self.jigsaw_id_to_pos.values()), 'jigsaw areas cannot be larger than the number of digits'

        if sandwich is not None:
            assert set(sandwich.keys()) == set(['side', 'bottom']), 'sandwich must contain only side and bottom'
            assert len(sandwich['side']) == self.H, 'side must be equal to board width'
            assert len(sandwich['bottom']) == self.V, 'bottom must be equal to board height'
            self.sandwich = sandwich

        if killer is not None:
            assert killer[0].ndim == 2, f'killer board must be 2d, got {killer[0].ndim}'
            assert killer[0].shape[0] == self.V and killer[0].shape[1] == self.H, 'killer board must be the same size as the board'
            assert all(isinstance(i.item(), str) and i.item().isdecimal() for i in np.nditer(killer[0])), 'killer board must contain only digits or space'
            assert set(killer[1].keys()).issubset(set(killer[0].flatten())), f'killer clues must contain all killer block ids, {set(killer[0].flatten()) - set(killer[1].keys())}'
            self.killer = killer

        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[pos] = self.model.NewIntVar(1, self.L, f'{pos}')

    def add_all_constraints(self):
        # some squares are already filled
        for pos in get_all_pos(self.V, self.H):
            c = get_value(self.board, pos)
            if c != ' ':
                self.model.Add(self.model_vars[pos] == c)
        # every number appears exactly once in each row, each column and each block
        # each row
        for row in range(self.V):
            row_vars = [self.model_vars[pos] for pos in get_row_pos(row, H=self.H)]
            self.model.AddAllDifferent(row_vars)
        # each column
        for col in range(self.H):
            col_vars = [self.model_vars[pos] for pos in get_col_pos(col, V=self.V)]
            self.model.AddAllDifferent(col_vars)
        if self.constrain_blocks:  # each block must contain all numbers from 1 to 9 exactly once
            for block_i in range(self.B):
                block_vars = [self.model_vars[p] for p in get_block_pos(block_i, Bv=self.Bv, Bh=self.Bh)]
                self.model.AddAllDifferent(block_vars)
        if self.sandwich is not None:
            self.add_sandwich_constraints()
        if self.unique_diagonal:
            self.add_unique_diagonal_constraints()
        if self.jigsaw_id_to_pos is not None:
            self.add_jigsaw_constraints()
        if self.killer is not None:
            self.add_killer_constraints()

    def add_sandwich_constraints(self):
        """Sandwich constraints, enforce that the sum of the values between 1 and 9 for each row and column is equal to the clue."""
        for c, clue in enumerate(self.sandwich['bottom']):
            if clue is None or int(clue) < 0:
                continue
            col_vars = [self.model_vars[p] for p in get_col_pos(c, V=self.V)]
            add_single_sandwich(col_vars, int(clue), self.model, name=f"sand_side_{c}")
        for r, clue in enumerate(self.sandwich['side']):
            if clue is None or int(clue) < 0:
                continue
            row_vars = [self.model_vars[p] for p in get_row_pos(r, H=self.H)]
            add_single_sandwich(row_vars, int(clue), self.model, name=f"sand_bottom_{r}")

    def add_unique_diagonal_constraints(self):
        main_diagonal_vars = [self.model_vars[get_pos(x=i, y=i)] for i in range(min(self.V, self.H))]
        self.model.AddAllDifferent(main_diagonal_vars)
        anti_diagonal_vars = [self.model_vars[get_pos(x=i, y=self.V-i-1)] for i in range(min(self.V, self.H))]
        self.model.AddAllDifferent(anti_diagonal_vars)

    def add_jigsaw_constraints(self):
        """All digits in one jigsaw area must be unique."""
        for pos_list in self.jigsaw_id_to_pos.values():
            self.model.AddAllDifferent([self.model_vars[p] for p in pos_list])

    def add_killer_constraints(self):
        """Killer constraints, enforce that the sum of the values in each killer block is equal to the clue and all numbers in a block are unique."""
        killer_board, killer_clues = self.killer
        # change clue keys to ints
        killer_clues = {int(k): v for k, v in killer_clues.items()}
        killer_id_to_pos = defaultdict(list)
        for pos in get_all_pos(self.V, self.H):
            v = get_char(killer_board, pos)
            if v.isdecimal():
                killer_id_to_pos[int(v)].append(pos)
        for killer_id, pos_list in killer_id_to_pos.items():
            self.model.AddAllDifferent([self.model_vars[p] for p in pos_list])
            clue = killer_clues[killer_id]
            self.model.Add(sum([self.model_vars[p] for p in pos_list]) == clue)

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: solver.value(var) for pos, var in board.model_vars.items()})
        def callback(single_res: SingleSolution):
            print("Solution found")
            val_arr = np.array([[single_res.assignment[get_pos(x=c, y=r)] for c in range(self.H)] for r in range(self.V)])
            print(combined_function(self.V, self.H, center_char=lambda r, c: val_arr[r, c] if val_arr[r, c] < 10 else chr(val_arr[r, c] - 10 + ord('a'))))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)



def add_single_sandwich(vars_line: list[cp_model.IntVar], clue: int, model: cp_model.CpModel, name: str):
    # VAR count:
    # is_min: L
    # is_max: L
    # pos_min/max/lt: 1+1+1
    # between: L
    # a1/a2/case_a: L+L+L
    # b1/b2/case_b: L+L+L
    # take: L
    # 10L+3 per 1 call of the function (i.e. per 1 line)
    # entire board will have 2L lines (rows and columns)
    # in total: 20L^2+6L

    L = len(vars_line)
    is_min = [model.NewBoolVar(f"{name}_ismin_{i}") for i in range(L)]
    is_max = [model.NewBoolVar(f"{name}_ismax_{i}") for i in range(L)]
    for i, v in enumerate(vars_line):
        model.Add(v == 1).OnlyEnforceIf(is_min[i])
        model.Add(v != 1).OnlyEnforceIf(is_min[i].Not())
        model.Add(v == L).OnlyEnforceIf(is_max[i])
        model.Add(v != L).OnlyEnforceIf(is_max[i].Not())

    # index of the minimum and maximum values (sum of the values inbetween must = clue)
    pos_min = model.NewIntVar(0, L - 1, f"{name}_pos_min")
    pos_max = model.NewIntVar(0, L - 1, f"{name}_pos_max")
    model.Add(pos_min == sum(i * is_min[i] for i in range(L)))
    model.Add(pos_max == sum(i * is_max[i] for i in range(L)))

    # used later to handle both cases (A. pos_min < pos_max and B. pos_max < pos_min)
    lt = model.NewBoolVar(f"{name}_lt")  # pos_min < pos_max ?
    model.Add(pos_min < pos_max).OnlyEnforceIf(lt)
    model.Add(pos_min >= pos_max).OnlyEnforceIf(lt.Not())

    between = [model.NewBoolVar(f"{name}_between_{i}") for i in range(L)]
    for i in range(L):
        # Case A: pos_min < i < pos_max (AND lt is true)
        a1 = model.NewBoolVar(f"{name}_a1_{i}")  # pos_min < i
        a2 = model.NewBoolVar(f"{name}_a2_{i}")  # i < pos_max

        model.Add(pos_min < i).OnlyEnforceIf(a1)
        model.Add(pos_min >= i).OnlyEnforceIf(a1.Not())
        model.Add(i < pos_max).OnlyEnforceIf(a2)
        model.Add(i >= pos_max).OnlyEnforceIf(a2.Not())

        case_a = model.NewBoolVar(f"{name}_caseA_{i}")
        and_constraint(model, case_a, [lt, a1, a2])

        # Case B: pos_max < i < pos_min (AND lt is false)
        b1 = model.NewBoolVar(f"{name}_b1_{i}")  # pos_max < i
        b2 = model.NewBoolVar(f"{name}_b2_{i}")  # i < pos_min

        model.Add(pos_max < i).OnlyEnforceIf(b1)
        model.Add(pos_max >= i).OnlyEnforceIf(b1.Not())
        model.Add(i < pos_min).OnlyEnforceIf(b2)
        model.Add(i >= pos_min).OnlyEnforceIf(b2.Not())

        case_b = model.NewBoolVar(f"{name}_caseB_{i}")
        and_constraint(model, case_b, [lt.Not(), b1, b2])

        # between[i] is true if we're in case A or case B
        or_constraint(model, between[i], [case_a, case_b])

    # sum values at indices that are "between"
    take = [model.NewIntVar(0, L, f"{name}_take_{i}") for i in range(L)]
    for i, v in enumerate(vars_line):
        # take[i] = v if between[i] else 0
        model.Add(take[i] == v).OnlyEnforceIf(between[i])
        model.Add(take[i] == 0).OnlyEnforceIf(between[i].Not())

    model.Add(sum(take) == clue)
