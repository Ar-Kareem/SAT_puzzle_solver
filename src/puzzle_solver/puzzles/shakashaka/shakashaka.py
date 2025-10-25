from collections import defaultdict
from dataclasses import dataclass
from enum import Enum

import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, set_char, get_char, get_neighbors4, in_bounds
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import render_bw_tiles_split


TPos = tuple[int, int]

class State(Enum):
    WHITE = 'W'
    BLACK = 'B'
    TOP_LEFT = 'TL'
    TOP_RIGHT = 'TR'
    BOTTOM_LEFT = 'BL'
    BOTTOM_RIGHT = 'BR'

@dataclass
class Rectangle:
    is_rotated: bool
    width: int
    height: int
    body: frozenset[tuple[TPos, State]]
    disallow_white: frozenset[tuple[TPos]]
    max_x: int
    max_y: int

@dataclass
class RectangleOnBoard:
    is_active: cp_model.IntVar
    rectangle: Rectangle
    body: frozenset[tuple[Pos, State]]
    body_positions: frozenset[Pos]
    disallow_white: frozenset[Pos]
    translate: Pos
    width: int
    height: int


def init_rectangles(V: int, H: int) -> list[Rectangle]:
    """Returns all possible upright and 45 degree rotated rectangles on a VxH board that are NOT translated (i.e. both min_x and min_y are always 0)"""
    rectangles = []
    # up right rectangles
    for height in range(1, V+1):
        for width in range(1, H+1):
            body = {(x, y) for x in range(width) for y in range(height)}
            # disallow any orthogonal adjacent white positions
            disallow_white = set((p[0] + dxdy[0], p[1] + dxdy[1]) for p in body for dxdy in ((1,0),(-1,0),(0,1),(0,-1)))
            disallow_white -= body
            rectangles.append(Rectangle(
                is_rotated=False,
                width=width,
                height=height,
                body={(p, State.WHITE) for p in body},
                disallow_white=disallow_white,
                max_x=width-1,
                max_y=height-1,
            ))
    # now imagine rectangles rotated clockwise by 45 degrees
    for height in range(1, V+1):
        for width in range(1, H+1):
            if width + height > V or width + height > H:  # this rotated rectangle wont fit
                continue
            body = {}
            tl_body = {(i, height-1-i) for i in range(height)}  # top left edge
            tr_body = {(height+i, i) for i in range(width)}  # top right edge
            br_body = {(width+height-i-1, width+i) for i in range(height)}  # bottom right edge
            bl_body = {(width-i-1, width+height-i-1) for i in range(width)}  # bottom left edge
            inner_body = set()  # inner body is anything to the right of L and to the left of R
            for y in range(width+height):
                row_is_active = False
                for x in range(width+height):
                    if (x, y) in tl_body or (x, y) in bl_body:
                        row_is_active = True
                        continue
                    if (x, y) in tr_body or (x, y) in br_body:
                        break
                    if row_is_active:
                        inner_body.add((x, y))
            tl_body = {(p, State.TOP_LEFT) for p in tl_body}
            tr_body = {(p, State.TOP_RIGHT) for p in tr_body}
            br_body = {(p, State.BOTTOM_RIGHT) for p in br_body}
            bl_body = {(p, State.BOTTOM_LEFT) for p in bl_body}
            inner_body = {(p, State.WHITE) for p in inner_body}
            rectangles.append(Rectangle(
                is_rotated=True, width=width, height=height, body=tl_body | tr_body | br_body | bl_body | inner_body, disallow_white=set(),
                # clear from vizualization, both width and height contribute to both dimensions since it is rotated
                max_x=width + height - 1,
                max_y=width + height - 1,
                ))
    return rectangles


class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all((c.item() in [' ', 'B', '0', '1', '2', '3', '4']) for c in np.nditer(board)), 'board must contain only space, B, 0, 1, 2, 3, 4'
        self.board = board
        self.V, self.H = board.shape
        self.black_positions: set[Pos] = {pos for pos in get_all_pos(self.V, self.H) if get_char(self.board, pos).strip() != ''}
        self.black_positions_tuple: set[TPos] = {(p.x, p.y) for p in self.black_positions}
        self.pos_to_rectangle_on_board: dict[Pos, list[RectangleOnBoard]] = defaultdict(list)
        self.model = cp_model.CpModel()
        self.B: dict[Pos, cp_model.IntVar] = {}
        self.W: dict[Pos, cp_model.IntVar] = {}
        self.rectangles_on_board: list[RectangleOnBoard] = []
        self.init_rectangles_on_board()
        self.create_vars()
        self.add_all_constraints()

    def init_rectangles_on_board(self):
        rectangles = init_rectangles(self.V, self.H)
        for rectangle in rectangles:
            # translate
            for dx in range(self.H - rectangle.max_x):
                for dy in range(self.V - rectangle.max_y):
                    body: list[tuple[Pos, State]] = [None] * len(rectangle.body)
                    for i, (p, s) in enumerate(rectangle.body):
                        pp = (p[0] + dx, p[1] + dy)
                        body[i] = (pp, s)
                        if pp in self.black_positions_tuple:
                            body = None
                            break
                    if body is None:
                        continue
                    disallow_white = {Pos(x=p[0] + dx, y=p[1] + dy) for p in rectangle.disallow_white}
                    body_positions = set((Pos(x=p[0], y=p[1])) for p, _ in body)
                    rectangle_on_board = RectangleOnBoard(
                        is_active=self.model.NewBoolVar(f'{rectangle.is_rotated}:{rectangle.width}x{rectangle.height}:{dx}:{dy}:is_active'),
                        rectangle=rectangle,
                        body=set((Pos(x=p[0], y=p[1]), s) for p, s in body),
                        body_positions=body_positions,
                        disallow_white=disallow_white,
                        translate=Pos(x=dx, y=dy),
                        width=rectangle.width,
                        height=rectangle.height,
                    )
                    self.rectangles_on_board.append(rectangle_on_board)
                    for p in body_positions:
                        self.pos_to_rectangle_on_board[p].append(rectangle_on_board)

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.B[pos] = self.model.NewBoolVar(f'B:{pos}')
            self.W[pos] = self.B[pos].Not()
            if pos in self.black_positions:
                self.model.Add(self.B[pos] == 1)

    def add_all_constraints(self):
        # every position not fixed must be part of exactly one rectangle
        for pos in get_all_pos(self.V, self.H):
            if pos in self.black_positions:
                continue
            self.model.AddExactlyOne([r.is_active for r in self.pos_to_rectangle_on_board[pos]])
        # if a rectangle is active then all its body is black and all its disallow_white is white
        for rectangle_on_board in self.rectangles_on_board:
            for pos, state in rectangle_on_board.body:
                if state == State.WHITE:
                    self.model.Add(self.W[pos] == 1).OnlyEnforceIf(rectangle_on_board.is_active)
                else:
                    self.model.Add(self.B[pos] == 1).OnlyEnforceIf(rectangle_on_board.is_active)
            for pos in rectangle_on_board.disallow_white:
                if not in_bounds(pos, self.V, self.H):
                    continue
                self.model.Add(self.B[pos] == 1).OnlyEnforceIf(rectangle_on_board.is_active)
        # if a position has a clue, enforce it
        for pos in get_all_pos(self.V, self.H):
            c = get_char(self.board, pos)
            if c.strip() != '' and c.strip().isdecimal():
                clue = int(c.strip())
                neighbors = [self.B[p] for p in get_neighbors4(pos, self.V, self.H) if p not in self.black_positions]
                self.model.Add(sum(neighbors) == clue)

    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, int] = {}
            for rectangle_on_board in board.rectangles_on_board:
                if solver.Value(rectangle_on_board.is_active) == 1:
                    for p, s in rectangle_on_board.body:
                        assignment[p] = s.value
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.full((self.V, self.H), 'W', dtype=object)
            text = np.full((self.V, self.H), '', dtype=object)
            for pos in get_all_pos(self.V, self.H):
                if pos in single_res.assignment:
                    val = single_res.assignment[pos]
                else:
                    c = get_char(self.board, pos)
                    if c.strip() != '':
                        val = 'B'
                        text[pos.y][pos.x] = c if c.strip() != 'B' else '.'
                set_char(res, pos, val)
            print(render_bw_tiles_split(res, cell_w=6, cell_h=3, borders=True, mode="text", cell_text=lambda r, c: text[r][c]))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
