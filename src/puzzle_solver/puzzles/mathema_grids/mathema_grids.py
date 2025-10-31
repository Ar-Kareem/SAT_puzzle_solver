from dataclasses import dataclass
import numpy as np
from ortools.sat.python import cp_model
from ortools.util.python import sorted_interval_list

from puzzle_solver.core.utils import Direction, Pos, get_char, get_next_pos, get_row_pos, get_col_pos, in_bounds, set_char
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


@dataclass
class var_with_bounds:
    var: cp_model.IntVar
    min_value: int
    max_value: int


def _div_bounds(a_min: int, a_max: int, b_min: int, b_max: int) -> tuple[int, int]:
    assert not (b_min == 0 and b_max == 0), "Denominator interval cannot be [0, 0]."
    denoms = [b_min, b_max]
    if 0 in denoms:
        denoms.remove(0)
    if b_min <= -1:
        denoms += [-1]
    if b_max >= 1:
        denoms += [1]
    candidates = [a_min // d for d in denoms] + [a_max // d for d in denoms]
    return min(candidates), max(candidates)


class Board:
    def __init__(self, board: np.array, digits: list[int]):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        self.board = board
        self.V, self.H = board.shape
        assert self.V >= 3 and self.V % 2 == 1, f'board must have at least 3 rows and an odd number of rows. Got {self.V} rows.'
        assert self.H >= 3 and self.H % 2 == 1, f'board must have at least 3 columns and an odd number of columns. Got {self.H} columns.'
        self.digits = digits
        self.domain_values = sorted_interval_list.Domain.FromValues(self.digits)
        self.domain_values_no_zero = sorted_interval_list.Domain.FromValues([d for d in self.digits if d != 0])

        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}
        self.create_vars()
        assert len(self.model_vars) == len(self.digits), f'len(model_vars) != len(digits), {len(self.model_vars)} != {len(self.digits)}'
        self.model.AddAllDifferent(list(self.model_vars.values()))

    def create_vars(self):
        for row in range(0, self.V-2, 2):
            line_pos = [pos for pos in get_row_pos(row, self.H)]
            self.parse_line(line_pos)
        for col in range(0, self.H-2, 2):
            line_pos = [pos for pos in get_col_pos(col, self.V)]
            self.parse_line(line_pos)

    def parse_line(self, line_pos: list[Pos]) -> list[int]:
        last_num = get_char(self.board, line_pos[-1])
        equal_sign = get_char(self.board, line_pos[-2])
        assert equal_sign == '=', f'last element of line must be =, got {equal_sign}'
        line_pos = line_pos[:-2]
        operators = [get_char(self.board, pos) for pos in line_pos[1::2]]
        assert all(c.strip() in ['+', '-', '*', '/'] for c in operators), f'even indices of line must be operators, got {operators}'
        digits_pos = line_pos[::2]
        running_var = self.get_var(digits_pos[0], fixed=get_char(self.board, digits_pos[0]))
        for pos, operator in zip(digits_pos[1:], operators):
            running_var = self.apply_operator(operator, running_var, self.get_var(pos, fixed=get_char(self.board, pos)))
        self.model.Add(running_var.var == int(last_num))
        return running_var

    def get_var(self, pos: Pos, fixed: str) -> var_with_bounds:
        if pos not in self.model_vars:
            domain = self.domain_values_no_zero if self.might_be_denominator(pos) else self.domain_values
            self.model_vars[pos] = self.model.NewIntVarFromDomain(domain, f'{pos}')
        if fixed.strip():
            self.model.Add(self.model_vars[pos] == int(fixed))
        return var_with_bounds(var=self.model_vars[pos], min_value=min(self.digits), max_value=max(self.digits))

    def might_be_denominator(self, pos: Pos) -> bool:
        "Important since if the variable might be a denominator and the domain includes 0 then ortools immediately sets the model as INVALID"
        above_pos = get_next_pos(pos, Direction.UP)
        left_pos = get_next_pos(pos, Direction.LEFT)
        above_operator = get_char(self.board, above_pos) if in_bounds(above_pos, self.V, self.H) else None
        left_operator = get_char(self.board, left_pos) if in_bounds(left_pos, self.V, self.H) else None
        return above_operator == '/' or left_operator == '/'

    def apply_operator(self, operator: str, a: var_with_bounds, b: var_with_bounds) -> var_with_bounds:
        assert operator in ['+', '-', '*', '/'], f'invalid operator: {operator}'
        if operator == "+":
            lo = a.min_value + b.min_value
            hi = a.max_value + b.max_value
            res = self.model.NewIntVar(lo, hi, "sum")
            self.model.Add(res == a.var + b.var)
        elif operator == "-":
            lo = a.min_value - b.max_value
            hi = a.max_value - b.min_value
            res = self.model.NewIntVar(lo, hi, "diff")
            self.model.Add(res == a.var - b.var)
        elif operator == "*":
            cands = [a.min_value*b.min_value, a.min_value*b.max_value, a.max_value*b.min_value, a.max_value*b.max_value]
            lo, hi = min(cands), max(cands)
            res = self.model.NewIntVar(lo, hi, "prod")
            self.model.AddMultiplicationEquality(res, [a.var, b.var])
        elif operator == "/":
            self.model.Add(b.var != 0)
            lo, hi = _div_bounds(a.min_value, a.max_value, b.min_value, b.max_value)
            res = self.model.NewIntVar(lo, hi, "quot")
            self.model.AddDivisionEquality(res, a.var, b.var)
        return var_with_bounds(res, lo, hi)

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: solver.Value(var) for pos, var in board.model_vars.items()})
        def callback(single_res: SingleSolution):
            print("Solution found")
            output_board = self.board.copy()
            for pos, var in single_res.assignment.items():
                set_char(output_board, pos, str(var))
            print(combined_function(self.V, self.H, center_char=lambda r, c: str(output_board[r, c])))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
