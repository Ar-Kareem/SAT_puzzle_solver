import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Optional, Callable
from enum import Enum

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp
from ortools.sat.python.cp_model import CpSolverSolutionCallback

sys.path.append(str(Path(__file__).parent.parent))
from core.utils import Pos, get_all_pos, get_char, set_char, in_bounds, get_next_pos, get_neighbors4, Direction, SingleSolution, get_hashable_solution


class State(Enum):
    BLACK = ('BLACK', 'B')
    SHINE = ('SHINE', 'S')
    LIGHT = ('LIGHT', 'L')


def laser_out(board: np.array, init_pos: Pos) -> list[Pos]:
    'laser out in all 4 directions until we hit a wall or out of bounds'
    N = board.shape[0]
    result = []
    for direction in Direction:
        cur_pos = init_pos
        while True:
            cur_pos = get_next_pos(cur_pos, direction)
            if not in_bounds(cur_pos, N) or get_char(board, cur_pos) != '*':
                break
            result.append(cur_pos)
    return result


class AllSolutionsCollector(CpSolverSolutionCallback):
    def __init__(self, board: 'Board', out: List[SingleSolution], max_solutions: Optional[int] = None, callback: Optional[Callable[[SingleSolution], None]] = None):
        super().__init__()
        self.out = out
        self.unique_solutions = set()
        self.max_solutions = max_solutions
        self.callback = callback
        self.vars_by_pos: Dict[Pos, List[tuple[State, cp_model.IntVar]]] = {}
        for (pos, state), var in board.model_vars.items():
            self.vars_by_pos.setdefault(pos, []).append((state, var))

    def on_solution_callback(self):
        try:
            assignment: Dict[Pos, str] = {}
            for pos, candidates in self.vars_by_pos.items():
                for state, var in candidates:  # exactly one is true per star cell
                    if self.BooleanValue(var):
                        assignment[pos] = state.value[1]
                        break
            result = SingleSolution(assignment=assignment)
            result_json = get_hashable_solution(result)
            if result_json in self.unique_solutions:
                return
            self.unique_solutions.add(result_json)
            self.out.append(result)
            if self.callback is not None:
                self.callback(result)
            if self.max_solutions is not None and len(self.out) >= self.max_solutions:
                self.StopSearch()
        except Exception as e:
            print(e)
            raise e

class Board:
    def __init__(self, board: np.array):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert board.shape[0] == board.shape[1], 'board must be square'
        assert all((c in ['*', 'W']) or str(c).isdecimal() for c in np.nditer(board)), 'board must contain only * or W or numbers'
        self.board = board
        self.N = board.shape[0]
        self.star_positions: set[Pos] = {pos for pos in get_all_pos(self.N) if get_char(self.board, pos) == '*'}
        self.number_position: set[Pos] = {pos for pos in get_all_pos(self.N) if str(get_char(self.board, pos)).isdecimal()}
        self.model = cp_model.CpModel()
        self.model_vars: dict[tuple[Pos, State], cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def create_vars(self):
        for pos in self.star_positions:
            var_list = []
            for state in State:
                v = self.model.NewBoolVar(f'{pos}:{state.value[0]}')
                self.model_vars[(pos, state)] = v
                var_list.append(v)
            self.model.AddExactlyOne(var_list)

    def add_all_constraints(self):
        # goal: no black squares
        for pos in self.star_positions:
            self.model.Add(self.model_vars[(pos, State.BLACK)] == 0)
        # number of lights touching a decimal is = decimal
        for pos in self.number_position:
            ground = int(get_char(self.board, pos))
            neighbour_list = get_neighbors4(pos, self.N, self.N)
            neighbour_list = [p for p in neighbour_list if p in self.star_positions]
            neighbour_light_count = lxp.Sum([self.model_vars[(p, State.LIGHT)] for p in neighbour_list])
            self.model.Add(neighbour_light_count == ground)
        # if a square is a light then everything it touches shines
        for pos in self.star_positions:
            orthoginals = laser_out(self.board, pos)
            for ortho in orthoginals:
                self.model.Add(self.model_vars[(ortho, State.SHINE)] == 1).OnlyEnforceIf([self.model_vars[(pos, State.LIGHT)]])
        # a square is black if all of it's laser_out is not light AND itself isnot a light
        for pos in self.star_positions:
            orthoginals = laser_out(self.board, pos)
            i_am_not_light = [self.model_vars[(pos, State.LIGHT)].Not()]
            no_light_in_laser = [self.model_vars[(p, State.LIGHT)].Not() for p in orthoginals]
            self.model.Add(self.model_vars[(pos, State.BLACK)] == 1).OnlyEnforceIf(i_am_not_light + no_light_in_laser)

    def solve_all(self, max_solutions: Optional[int] = None, callback: Optional[Callable[[SingleSolution], None]] = None) -> List[SingleSolution]:
        solver = cp_model.CpSolver()
        solver.parameters.enumerate_all_solutions = True
        solutions: List[SingleSolution] = []
        collector = AllSolutionsCollector(self, solutions, max_solutions=max_solutions, callback=callback)
        tic = time.time()
        solver.solve(self.model, collector)
        print("Solutions found:", len(solutions))
        print("status:", solver.StatusName())
        toc = time.time()
        print(f"Time taken: {toc - tic:.2f} seconds")
        return solutions

    def solve_and_print(self):
        def callback(single_res: SingleSolution):
            print("Solution found")
            res = np.zeros_like(self.board)
            for pos in get_all_pos(self.N):
                c = get_char(self.board, pos)
                if c == '*':
                    c = single_res.assignment[pos]
                    c = 'L' if c == 'L' else ' '
                set_char(res, pos, c)
            print(res)
        return self.solve_all(callback=callback)
