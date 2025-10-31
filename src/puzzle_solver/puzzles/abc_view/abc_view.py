import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, get_pos, get_row_pos, get_col_pos
from puzzle_solver.core.utils_ortools import and_constraint, generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


class Board:
    def __init__(self, board: np.array, top: np.array, left: np.array, bottom: np.array, right: np.array, characters: list[str]):
        self.BLANK = 'BLANK'
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        self.characters_no_blank = characters
        self.characters = characters + [self.BLANK]
        assert all(c.strip() in self.characters or c.strip() == '' for c in board.flatten()), f'board must contain characters in {self.characters}'
        assert all(c.strip() in self.characters or c.strip() == '' for c in np.concatenate([top, left, bottom, right])), f'top, bottom, left, and right must contain only characters in {self.characters}'
        self.board = board
        self.V, self.H = board.shape
        assert top.shape == (self.H,) and bottom.shape == (self.H,) and left.shape == (self.V,) and right.shape == (self.V,), 'top, bottom, left, and right must be 1d arrays of length board width and height'
        self.top = top
        self.left = left
        self.bottom = bottom
        self.right = right

        self.model = cp_model.CpModel()
        self.model_vars: dict[tuple[Pos, str], cp_model.IntVar] = {}
        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            for character in self.characters:
                self.model_vars[pos, character] = self.model.NewBoolVar(f'{pos}:{character}')

    def add_all_constraints(self):
        for pos in get_all_pos(self.V, self.H):
            self.model.AddExactlyOne([self.model_vars[pos, character] for character in self.characters])
            c = get_char(self.board, pos).strip()  # force the clue if on the board
            if not c:
                continue
            self.model.Add(self.model_vars[pos, c] == 1)

        # each row and column must have exactly one of each character, except for BLANK
        for row in range(self.V):
            for character in self.characters_no_blank:
                self.model.AddExactlyOne([self.model_vars[pos, character] for pos in get_row_pos(row, self.H)])
        for col in range(self.H):
            for character in self.characters_no_blank:
                self.model.AddExactlyOne([self.model_vars[pos, character] for pos in get_col_pos(col, self.V)])

        # a character clue on that side means the first character that appears on the side is the clue
        for i, top_char in enumerate(self.top):
            self.force_first_character(list(get_col_pos(i, self.V)), top_char)
        for i, bottom_char in enumerate(self.bottom):
            self.force_first_character(list(get_col_pos(i, self.V))[::-1], bottom_char)
        for i, left_char in enumerate(self.left):
            self.force_first_character(list(get_row_pos(i, self.H)), left_char)
        for i, right_char in enumerate(self.right):
            self.force_first_character(list(get_row_pos(i, self.H))[::-1], right_char)

    def force_first_character(self, pos_list: list[Pos], target_character: str):
        if not target_character:
            return
        for i, pos in enumerate(pos_list):
            is_first_char = self.model.NewBoolVar(f'{i}:{target_character}:is_first_char')
            and_constraint(self.model, is_first_char, [self.model_vars[pos, self.BLANK] for pos in pos_list[:i]] + [self.model_vars[pos_list[i], self.BLANK].Not()])
            self.model.Add(self.model_vars[pos, target_character] == 1).OnlyEnforceIf(is_first_char)

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: char for (pos, char), var in board.model_vars.items() if solver.Value(var) == 1 and char != board.BLANK})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H, center_char=lambda r, c: single_res.assignment.get(get_pos(x=c, y=r), ''), text_on_shaded_cells=False))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
