from typing import Union, Optional

import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_pos, get_all_pos, get_char, set_char, get_row_pos, get_col_pos
from puzzle_solver.core.utils_ortools import and_constraint, generic_solve_all, or_constraint, SingleSolution


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
    def __init__(self, board: np.array, block_size: Optional[tuple[int, int]] = None, sandwich: Optional[dict[str, list[int]]] = None, unique_diagonal: bool = False):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert board.shape[0] == board.shape[1], 'board must be square'
        assert all(isinstance(i.item(), str) and len(i.item()) == 1 and (i.item().isalnum() or i.item() == ' ') for i in np.nditer(board)), 'board must contain only alphanumeric characters or space'
        self.board = board
        self.V, self.H = board.shape
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
        if sandwich is not None:
            assert set(sandwich.keys()) == set(['side', 'bottom']), 'sandwich must contain only side and bottom'
            assert len(sandwich['side']) == self.H, 'side must be equal to board width'
            assert len(sandwich['bottom']) == self.V, 'bottom must be equal to board height'
            self.sandwich = sandwich
        else:
            self.sandwich = None
        self.unique_diagonal = unique_diagonal
    
        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[pos] = self.model.NewIntVar(1, self.B, f'{pos}')

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
        # each block
        for block_i in range(self.B):
            block_vars = [self.model_vars[p] for p in get_block_pos(block_i, Bv=self.Bv, Bh=self.Bh)]
            self.model.AddAllDifferent(block_vars)
        if self.sandwich is not None:
            self.add_sandwich_constraints()
        if self.unique_diagonal:
            self.add_unique_diagonal_constraints()

    def add_sandwich_constraints(self):
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

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, int] = {}
            for pos, var in board.model_vars.items():
                assignment[pos] = solver.value(var)
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.full((self.V, self.H), ' ', dtype=object)
            for pos in get_all_pos(self.V, self.H):
                c = get_value(self.board, pos)
                c = single_res.assignment[pos]
                set_value(res, pos, c)
            print(res)
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
