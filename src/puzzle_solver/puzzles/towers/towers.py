import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, set_char, get_pos, get_row_pos, get_col_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution


def bool_from_greater_than(model, a, b, name):
    res = model.NewBoolVar(name)
    model.add(a > b).OnlyEnforceIf(res)
    model.add(a <= b).OnlyEnforceIf(res.Not())
    return res


class Board:
    def __init__(self, board: np.array, sides: dict[str, np.array]):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert board.shape[0] == board.shape[1], 'board must be square'
        assert len(sides) == 4, '4 sides must be provided'
        assert all(s.ndim == 1 and s.shape[0] == board.shape[0] for s in sides.values()), 'all sides must be equal to board size'
        assert set(sides.keys()) == set(['right', 'left', 'top', 'bottom'])
        assert all((c == ' ') or str(c).isdecimal() for c in np.nditer(board)), 'board must contain space or digits'
        self.board = board
        self.sides = sides
        self.N = board.shape[0]
        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.N):
            self.model_vars[pos] = self.model.NewIntVar(1, self.N, f'{pos}')

    def add_all_constraints(self):
        # if board has value then force intvar to be that value
        for pos in get_all_pos(self.N):
            v = get_char(self.board, pos)
            if str(v).isdecimal():
                self.model.Add(self.model_vars[pos] == int(v))
        # all different for rows
        for row_i in range(self.N):
            row_vars = [self.model_vars[pos] for pos in get_row_pos(row_i, self.N)]
            self.model.AddAllDifferent(row_vars)
        # all different for cols
        for col_i in range(self.N):
            col_vars = [self.model_vars[pos] for pos in get_col_pos(col_i, self.N)]
            self.model.AddAllDifferent(col_vars)
        # constrain number of viewable towers
        # top
        for x in range(self.N):
            real = self.sides['top'][x]
            if real == -1:
                continue
            can_see_variables = []
            previous_towers: list[cp_model.IntVar] = []
            for y in range(self.N):
                current_tower = self.model_vars[get_pos(x=x, y=y)]
                can_see_variables.append(self.can_see_tower(previous_towers, current_tower, f'top:{x}:{y}'))
                previous_towers.append(current_tower)
            self.model.add(lxp.sum(can_see_variables) == real)
        # bottom
        for x in range(self.N):
            real = self.sides['bottom'][x]
            if real == -1:
                continue
            can_see_variables = []
            previous_towers: list[cp_model.IntVar] = []
            for y in range(self.N-1, -1, -1):
                current_tower = self.model_vars[get_pos(x=x, y=y)]
                can_see_variables.append(self.can_see_tower(previous_towers, current_tower, f'bottom:{x}:{y}'))
                previous_towers.append(current_tower)
            self.model.add(lxp.sum(can_see_variables) == real)
        # left
        for y in range(self.N):
            real = self.sides['left'][y]
            if real == -1:
                continue
            can_see_variables = []
            previous_towers: list[cp_model.IntVar] = []
            for x in range(self.N):
                current_tower = self.model_vars[get_pos(x=x, y=y)]
                can_see_variables.append(self.can_see_tower(previous_towers, current_tower, f'left:{x}:{y}'))
                previous_towers.append(current_tower)
            self.model.add(lxp.sum(can_see_variables) == real)
        # right
        for y in range(self.N):
            real = self.sides['right'][y]
            if real == -1:
                continue
            can_see_variables = []
            previous_towers: list[cp_model.IntVar] = []
            for x in range(self.N-1, -1, -1):
                current_tower = self.model_vars[get_pos(x=x, y=y)]
                can_see_variables.append(self.can_see_tower(previous_towers, current_tower, f'right:{x}:{y}'))
                previous_towers.append(current_tower)
            self.model.add(lxp.sum(can_see_variables) == real)

    def can_see_tower(self, blocks: list[cp_model.IntVar], tower: cp_model.IntVar, name: str) -> cp_model.IntVar:
        """
        Returns a boolean variable of whether a position BEFORE the blocks can see the "tower" parameter.
        i.e., is the tower taller than all the blocks?

        Args:
            blocks (list[cp_model.IntVar]): blocks that possibly block the view of the tower
            tower (cp_model.IntVar): tower to check if can be seen
            name (str): name of the constraint

        Returns:
            cp_model.IntVar: boolean variable of whether the tower can be seen
        """
        if len(blocks) == 0:
            return True
        # I can see "tower" if it's larger that all the blocks
        # lits is a list of [(tower > b0), (tower > b1), ..., (tower > bi)]
        lits = [bool_from_greater_than(self.model, tower, block, f'{name}:lits:{i}') for i, block in enumerate(blocks)]

        # create a single bool which decides if I can see it or not
        res = self.model.NewBoolVar(name)
        self.model.AddBoolAnd(lits).OnlyEnforceIf(res)
        self.model.AddBoolOr([res] + [l.Not() for l in lits])
        return res

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, int] = {}
            for pos, var in board.model_vars.items():
                assignment[pos] = solver.value(var)
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.full((self.N, self.N), ' ', dtype=object)
            for pos in get_all_pos(self.N):
                c = get_char(self.board, pos)
                c = single_res.assignment[pos]
                set_char(res, pos, c)
            print(res)
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
