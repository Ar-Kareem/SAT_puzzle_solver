import time
from typing import Union, Optional

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

from puzzle_solver.core.utils import Pos, get_all_pos, get_char, set_char, get_neighbors8
from puzzle_solver.core.utils_ortools import generic_solve_all, SingleSolution


class Board:
    def __init__(self, board: np.array, mine_count: Optional[int] = None):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert all(isinstance(i.item(), str) and (str(i.item()) in [' ', 'F', 'S', 'M', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']) for i in np.nditer(board)), 'board must be either F, S, M, 0-9 or space'
        self.board = board
        self.V = board.shape[0]
        self.H = board.shape[1]
        self.mine_count = mine_count
        self.model = cp_model.CpModel()
        self.model_vars: dict[Pos, cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[pos] = self.model.NewBoolVar(f'{pos}')

    def add_all_constraints(self):
        if self.mine_count is not None:
            self.model.Add(lxp.Sum(list(self.model_vars.values())) == self.mine_count)
        for pos in get_all_pos(self.V, self.H):
            c = get_char(self.board, pos)
            if c in ['F', ' ']:
                continue
            if c == 'S':  # safe position but neighbours are unknown
                self.model.Add(self.model_vars[pos] == 0)
                continue
            if c == 'M':  # mine position but neighbours are unknown
                self.model.Add(self.model_vars[pos] == 1)
                continue
            # clue indicates safe position AND neighbours are known
            c = int(c)
            self.model.Add(lxp.Sum([self.model_vars[n] for n in get_neighbors8(pos, self.V, self.H, include_self=False)]) == c)
            self.model.Add(self.model_vars[pos] == 0)


def _is_feasible(board: np.array, pos: Pos = None, value: str = None, mine_count: int = None) -> bool:
    """Returns True if the board is feasible after setting the value at the position"""
    board = board.copy()
    if pos is not None and value is not None:
        set_char(board, pos, str(value))
    board = Board(board, mine_count=mine_count)
    def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
        return SingleSolution(assignment={pos: solver.value(var) for pos, var in board.model_vars.items()})
    return len(generic_solve_all(board, board_to_solution, max_solutions=1, verbose=False)) >= 1

def _is_safe(board: np.array, pos: Pos, mine_count: Optional[int] = None) -> Union[bool, None]:
    """Returns a True if the position is safe, False if it is a mine, otherwise None"""
    safe_feasible = _is_feasible(board, pos, 'S', mine_count=mine_count)
    mine_feasible = _is_feasible(board, pos, 'M', mine_count=mine_count)
    if safe_feasible and mine_feasible:
        return None
    if safe_feasible:
        return True
    if mine_feasible:
        return False
    raise ValueError(f"Position {pos} has both safe and mine infeasible")

def give_next_guess(board: np.array, mine_count: Optional[int] = None, verbose: bool = True):
    tic = time.time()
    is_feasible = _is_feasible(board, mine_count=mine_count)
    if not is_feasible:
        raise ValueError("Board is not feasible")
    V = board.shape[0]
    H = board.shape[1]
    check_positions = set()  # any position that is unknown and has a neighbour with a clue or flag
    flag_positions = set()
    for pos in get_all_pos(V, H):
        neighbours8 = get_neighbors8(pos, V, H, include_self=False)
        if get_char(board, pos) not in [' ', 'F']:
            continue
        if get_char(board, pos) == 'F' or any(get_char(board, n) != ' ' for n in neighbours8):
            check_positions.add(pos)
        if get_char(board, pos) == 'F':
            flag_positions.add(pos)
    pos_dict = {pos: _is_safe(board, pos, mine_count) for pos in check_positions}
    safe_positions = {pos for pos, is_safe in pos_dict.items() if is_safe is True}
    mine_positions = {pos for pos, is_safe in pos_dict.items() if is_safe is False}
    new_garuneed_mine_positions = mine_positions - flag_positions
    wrong_flag_positions = flag_positions - mine_positions
    if verbose:
        if len(safe_positions) > 0:
            print(f"Found {len(safe_positions)} new guaranteed safe positions")
            print(safe_positions)
            print('-'*10)
        if len(mine_positions) == 0:
            print("No guaranteed mine positions")
            print('-'*10)
        if len(new_garuneed_mine_positions) > 0:
            print(f"Found {len(new_garuneed_mine_positions)} new guaranteed mine positions")
            print(new_garuneed_mine_positions)
            print('-'*10)
        if len(wrong_flag_positions) > 0:
            print(f"WARNING | "*4 + "WARNING")
            print(f"Found {len(wrong_flag_positions)} wrong flag positions")
            print(wrong_flag_positions)
            print('-'*10)
        toc = time.time()
        print(f"Time taken: {toc - tic:.2f} seconds")
    return safe_positions, new_garuneed_mine_positions, wrong_flag_positions

def print_board(board: np.array, safe_positions: set[Pos], new_garuneed_mine_positions: set[Pos], wrong_flag_positions: set[Pos]):
    res = np.full((board.shape[0], board.shape[1]), ' ', dtype=object)
    for pos in get_all_pos(board.shape[0], board.shape[1]):
        if pos in safe_positions:
            set_char(res, pos, 'S')
        elif pos in new_garuneed_mine_positions:
            set_char(res, pos, 'M')
        elif get_char(board, pos) == 'F' and pos not in wrong_flag_positions:
            set_char(res, pos, 'F')
    
    print(res)