
import multiprocessing
from typing import Optional, Callable
from typing import List, Dict

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp
from ortools.sat.python.cp_model import CpSolverSolutionCallback

from utils import Pos, Monster, Direction, get_pos, get_next_pos, in_bounds, get_char, get_all_monster_types, can_see, SingleBeamResult, SingleSolution, get_hashable_solution

class AllSolutionsCollector(CpSolverSolutionCallback):
    def __init__(self, board: "Board", out: List[SingleSolution], max_solutions: Optional[int] = None, callback: Optional[Callable[[SingleSolution], None]] = None):
        super().__init__()
        self.board = board
        self.out = out
        self.unique_solutions = set()
        self.max_solutions = max_solutions
        self.callback = callback
        # Precompute a name->Monster map and group vars by cell for fast lookup
        self.name_to_monster: Dict[str, Monster] = {m.value[1]: m for m in Monster}
        self.vars_by_pos: Dict[Pos, List[tuple[str, cp_model.IntVar]]] = {}
        for (pos, monster_name), var in board.model_vars.items():
            self.vars_by_pos.setdefault(pos, []).append((monster_name, var))

    def on_solution_callback(self):
        try:
            assignment: Dict[Pos, Monster] = {}
            for pos, candidates in self.vars_by_pos.items():
                for monster_name, var in candidates:  # exactly one is true per star cell
                    if self.BooleanValue(var):
                        assignment[pos] = self.name_to_monster[monster_name]
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
    def __init__(self, board: np.array, sides: dict[str, np.array]):
        assert board.ndim == 2, f'board must be 2d, got {board.ndim}'
        assert board.shape[0] == board.shape[1], 'board must be square'
        assert len(sides) == 4, '4 sides must be provided'
        assert all(s.ndim == 1 and s.shape[0] == board.shape[0] for s in sides.values()), 'all sides must be equal to board size'
        assert set(sides.keys()) == set(['right', 'left', 'top', 'bottom'])
        self.board = board
        self.sides = sides
        self.N = board.shape[0]
        self.model = cp_model.CpModel()
        self.model_vars: dict[tuple[Pos, str], cp_model.IntVar] = {}
        self.star_positions: set[Pos] = {pos for pos in self.get_all_pos() if get_char(self.board, pos) == '*'}

        self.create_vars()
        self.add_all_constraints()

    def get_all_pos(self):
        for y in range(self.N):
            for x in range(self.N):
                yield get_pos(x, y)

    def create_vars(self):
        for pos in self.star_positions:
            c = get_char(self.board, pos)
            assert c == '*', f'star position {pos} has character {c}'
            monster_vars = []
            for _, monster_name in get_all_monster_types():
                v = self.model.NewBoolVar(f"{pos}_is_{monster_name}")
                self.model_vars[(pos, monster_name)] = v
                monster_vars.append(v)
            self.model.add_exactly_one(*monster_vars)

    def add_all_constraints(self):
        # top edge
        print("top edge")
        for i, ground in zip(range(self.N), self.sides['top']):
            pos = get_pos(x=i, y=-1)
            beam_result = self.beam(pos, 'down')
            self.model.add(self.get_var(beam_result) == ground)

        # left edge
        print("left edge")
        for i, ground in zip(range(self.N), self.sides['left']):
            pos = get_pos(x=-1, y=i)
            beam_result = self.beam(pos, 'right')
            self.model.add(self.get_var(beam_result) == ground)

        # right edge
        print("right edge")
        for i, ground in zip(range(self.N), self.sides['right']):
            pos = get_pos(x=self.N, y=i)
            beam_result = self.beam(pos, 'left')
            self.model.add(self.get_var(beam_result) == ground)

        # bottom edge
        print("bottom edge")
        for i, ground in zip(range(self.N), self.sides['bottom']):
            pos = get_pos(x=i, y=self.N)
            beam_result = self.beam(pos, 'up')
            self.model.add(self.get_var(beam_result) == ground)

    def get_var(self, path: list[SingleBeamResult]) -> lxp:
        path_vars = []
        for square in path:
            assert square.position in self.star_positions, f'square {square.position} is not a star position'
            for monster, monster_name in get_all_monster_types():
                if can_see(square.position, square.reflect_count, monster):
                    path_vars.append(self.model_vars[(square.position, monster_name)])
        return lxp.Sum(path_vars) if path_vars else 0

    def beam(self, start_pos: Pos, direction: Direction) -> list[SingleBeamResult]:
        cur_result: list[SingleBeamResult] = []
        reflect_count = 0
        cur_pos = start_pos
        while True:
            cur_pos = get_next_pos(cur_pos, direction)
            if not in_bounds(cur_pos, self.N):
                break
            cur_pos_char = get_char(self.board, cur_pos)
            if cur_pos_char == '//':
                direction = {
                    'right': 'up',
                    'up': 'right',
                    'down': 'left',
                    'left': 'down'
                }[direction]
                reflect_count += 1
            elif cur_pos_char == '\\':
                direction = {
                    'right': 'down',
                    'down': 'right',
                    'up': 'left',
                    'left': 'up'
                }[direction]
                reflect_count += 1
            else:
                # not a mirror
                cur_result.append(SingleBeamResult(cur_pos, reflect_count))
        return cur_result

    def solve_all(self, max_solutions: Optional[int] = None, callback: Optional[Callable[[SingleSolution], None]] = None) -> List[SingleSolution]:
        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = multiprocessing.cpu_count()
        solutions: List[SingleSolution] = []
        collector = AllSolutionsCollector(self, solutions, max_solutions=max_solutions, callback=callback)
        print("Searching for solutions...")
        solver.Solve(self.model, collector)
        print("Solutions found:", len(solutions))
        print("status:", solver.StatusName())
        return solutions
