import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, get_col_pos, get_neighbors4, get_pos, get_char, get_row_pos
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution, force_connected_component
from puzzle_solver.core.utils_visualizer import combined_function, id_board_to_wall_fn


def return_3_consecutives(int_list: list[int]) -> list[tuple[int, int]]:
    """Given a list of integers (mostly with duplicates), return every consecutive sequence of 3 integer changes.
    i.e. return a list of (begin_idx, end_idx) tuples where for each r=int_list[begin_idx:end_idx] we have r[0]!=r[1] and r[-2]!=r[-1] and len(r)>=3"""
    out = []
    change_indices = [i for i in range(len(int_list) - 1) if int_list[i] != int_list[i+1]]
    # notice how for every subsequence r, the subsequence begining index is in change_indices and the ending index - 1 is in change_indices
    for i in range(len(change_indices) - 1):
        begin_idx = change_indices[i]
        end_idx = change_indices[i+1] + 1  # we want to include the first number in the third sequence
        if end_idx > len(int_list):
            continue
        out.append((begin_idx, end_idx))
    return out


def get_diagonal(pos1: Pos, pos2: Pos) -> list[Pos]:
    assert pos1 != pos2, 'positions must be different'
    dx = pos1.x - pos2.x
    dy = pos1.y - pos2.y
    assert abs(dx) == abs(dy), 'positions must be on a diagonal'
    sdx = 1 if dx > 0 else -1
    sdy = 1 if dy > 0 else -1
    return [get_pos(x=pos2.x + i*sdx, y=pos2.y + i*sdy) for i in range(abs(dx) + 1)]


class Board:
    def __init__(self, board: np.array, region_to_clue: dict[str, int]):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all(str(c.item()).isdecimal() for c in np.nditer(board)), 'board must contain only space or digits'
        self.board = board
        self.V, self.H = board.shape
        self.all_regions: set[int] = {int(c.item()) for c in np.nditer(board)}
        self.region_to_clue = {int(k): v for k, v in region_to_clue.items()}
        assert set(self.region_to_clue.keys()).issubset(self.all_regions), f'extra regions in region_to_clue: {set(self.region_to_clue.keys()) - self.all_regions}'
        self.region_to_pos: dict[int, set[Pos]] = {r: set() for r in self.all_regions}
        for pos in get_all_pos(self.V, self.H):
            rid = int(get_char(self.board, pos))
            self.region_to_pos[rid].add(pos)

        self.model = cp_model.CpModel()
        self.B: dict[Pos, cp_model.IntVar] = {}
        self.W: dict[Pos, cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.B[pos] = self.model.NewBoolVar(f'B:{pos}')
            self.W[pos] = self.model.NewBoolVar(f'W:{pos}')
            self.model.AddExactlyOne([self.B[pos], self.W[pos]])

    def add_all_constraints(self):
        # Regions with a number should contain black cells matching the number.
        for rid, clue in self.region_to_clue.items():
            self.model.Add(sum([self.B[p] for p in self.region_to_pos[rid]]) == clue)
        # 2 black cells cannot be adjacent horizontally or vertically.
        for pos in get_all_pos(self.V, self.H):
            for neighbor in get_neighbors4(pos, self.V, self.H):
                self.model.AddBoolOr([self.W[pos], self.W[neighbor]])
        # All white cells should be connected in a single group.
        force_connected_component(self.model, self.W)
        # A straight (orthogonal) line of connected white cells cannot span across more than 2 regions.
        self.disallow_white_lines_spanning_3_regions()
        # straight diagonal black lines from side wall to horizontal wall are not allowed; because they would disconnect the white cells
        self.disallow_full_black_diagonal()
        # disallow a diagonal black line coming out of a wall of length N then coming back in on the same wall; because it would disconnect the white cells
        self.disallow_zigzag_on_wall()

    def disallow_white_lines_spanning_3_regions(self):
        # A straight (orthogonal) line of connected white cells cannot span across more than 2 regions.
        row_to_region: dict[int, list[int]] = {row: [] for row in range(self.V)}
        col_to_region: dict[int, list[int]] = {col: [] for col in range(self.H)}
        for pos in get_all_pos(self.V, self.H):  # must traverse from least to most (both row and col)
            rid = int(get_char(self.board, pos))
            row_to_region[pos.y].append(rid)
            col_to_region[pos.x].append(rid)
        for row_num, row in row_to_region.items():
            for begin_idx, end_idx in return_3_consecutives(row):
                pos_list = [get_pos(x=x, y=row_num) for x in range(begin_idx, end_idx+1)]
                self.model.AddBoolOr([self.B[p] for p in pos_list])
        for col_num, col in col_to_region.items():
            for begin_idx, end_idx in return_3_consecutives(col):
                pos_list = [get_pos(x=col_num, y=y) for y in range(begin_idx, end_idx+1)]
                self.model.AddBoolOr([self.B[p] for p in pos_list])

    def disallow_full_black_diagonal(self):
        corners_dx_dy = [
            ((0, 0), 1, 1),
            ((self.H-1, 0), -1, 1),
            ((0, self.V-1), 1, -1),
            ((self.H-1, self.V-1), -1, -1),
        ]
        for (corner_x, corner_y), dx, dy in corners_dx_dy:
            for delta in range(1, min(self.V, self.H)):
                pos1 = get_pos(x=corner_x, y=corner_y + delta*dy)
                pos2 = get_pos(x=corner_x + delta*dx, y=corner_y)
                diagonal_line = get_diagonal(pos1, pos2)
                self.model.AddBoolOr([self.W[p] for p in diagonal_line])

    def disallow_zigzag_on_wall(self):
        for pos in get_row_pos(0, self.H):  # top line
            for end_x in range(pos.x + 2, self.H, 2):  # end pos is even distance away from start pos
                end_pos = get_pos(x=end_x, y=pos.y)
                dx = end_x - pos.x
                mid_pos = get_pos(x=pos.x + dx//2, y=pos.y + dx//2)
                diag_1 = get_diagonal(pos, mid_pos)  # from top wall to bottom triangle tip "\"
                diag_2 = get_diagonal(end_pos, mid_pos)  # from bottom triangle tip to top wall "/"
                self.model.AddBoolOr([self.W[p] for p in diag_1 + diag_2])
        for pos in get_row_pos(self.V-1, self.H):  # bottom line
            for end_x in range(pos.x + 2, self.H, 2):  # end pos is even distance away from start pos
                end_pos = get_pos(x=end_x, y=pos.y)
                dx = end_x - pos.x
                mid_pos = get_pos(x=pos.x + dx//2, y=pos.y - dx//2)
                diag_1 = get_diagonal(pos, mid_pos)  # from bottom wall to top triangle tip "/"
                diag_2 = get_diagonal(end_pos, mid_pos)  # from top triangle tip to bottom wall "\"
                self.model.AddBoolOr([self.W[p] for p in diag_1 + diag_2])
        for pos in get_col_pos(0, self.V):  # left line
            for end_y in range(pos.y + 2, self.V, 2):  # end pos is even distance away from start pos
                end_pos = get_pos(x=pos.x, y=end_y)
                dy = end_y - pos.y
                mid_pos = get_pos(x=pos.x + dy//2, y=pos.y + dy//2)
                diag_1 = get_diagonal(pos, mid_pos)  # from left wall to right triangle tip "\"
                diag_2 = get_diagonal(end_pos, mid_pos)  # from right triangle tip to left wall "/"
                self.model.AddBoolOr([self.W[p] for p in diag_1 + diag_2])
        for pos in get_col_pos(self.H-1, self.V):  # right line
            for end_y in range(pos.y + 2, self.V, 2):  # end pos is even distance away from start pos
                end_pos = get_pos(x=pos.x, y=end_y)
                dy = end_y - pos.y
                mid_pos = get_pos(x=pos.x - dy//2, y=pos.y + dy//2)
                diag_1 = get_diagonal(pos, mid_pos)  # from right wall to left triangle tip "/"

    def solve_and_print(self, verbose: bool = True, max_solutions: int = 20):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            return SingleSolution(assignment={pos: solver.Value(var) for pos, var in board.B.items()})
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H,
                cell_flags=id_board_to_wall_fn(self.board),
                is_shaded=lambda r, c: single_res.assignment[get_pos(x=c, y=r)] == 1,
                center_char=lambda r, c: self.region_to_clue.get(int(self.board[r, c]), ''),
                text_on_shaded_cells=False
            ))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose, max_solutions=max_solutions)
