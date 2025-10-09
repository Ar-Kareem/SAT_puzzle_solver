from dataclasses import dataclass
import multiprocessing

import numpy as np
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr as lxp

@dataclass
class SingleBeamResult:
  position: tuple[int, int]
  reflected: bool

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
        self.model_vars = {}
        self.create_vars()
        print('num vars', len(self.model_vars))
        self.add_all_constraints()
        self.solver = None

    def get_all_pos(self):
        for y in range(self.N):
            for x in range(self.N):
                yield (y, x)

    def create_vars(self):
        for pos in self.get_all_pos():
            c = self.get_char(pos)
            if c != '*':
                continue
            self.model_vars[(pos, 'vampire')] = self.model.NewBoolVar(f"{pos}_is_vampire")
            self.model_vars[(pos, 'zombie')] = self.model.NewBoolVar(f"{pos}_is_zombie")
            self.model_vars[(pos, 'ghost')] = self.model.NewBoolVar(f"{pos}_is_ghost")
            self.model.add_exactly_one(
                self.model_vars[(pos, 'vampire')],
                self.model_vars[(pos, 'zombie')],
                self.model_vars[(pos, 'ghost')]
            )

    def add_all_constraints(self):
        # top edge
        print("top edge")
        for i, ground in zip(range(self.N), self.sides['top']):
            pos = (-1, i)
            r = self.beam(pos, 'down')
            v = self.get_var(r)
            self.model.add(v == ground)
            
        # left edge
        print("left edge")
        for i, ground in zip(range(self.N), self.sides['left']):
            pos = (i, -1)
            r = self.beam(pos, 'right')
            v = self.get_var(r)
            self.model.add(v == ground)

        # right edge
        print("right edge")
        for i, ground in zip(range(self.N), self.sides['right']):
            pos = (i, self.N)
            r = self.beam(pos, 'left')
            v = self.get_var(r)
            self.model.add(v == ground)

        # bottom edge
        print("bottom edge")
        for i, ground in zip(range(self.N), self.sides['bottom']):
            pos = (self.N, i)
            r = self.beam(pos, 'up')
            self.model.add(v == ground)

    def get_var(self, path: list[SingleBeamResult]):
        path_vars = []
        for square in path:
            pos = square.position
            path_vars.append(self.model_vars[(pos, 'zombie')])
            if square.reflected:
                path_vars.append(self.model_vars[(pos, 'ghost')])
            else:
                path_vars.append(self.model_vars[(pos, 'vampire')])
                
        return lxp.Sum(path_vars)

    def get_char(self, pos):
        c = self.board[pos[0]][pos[1]]
        assert c in ['//', '\\', '*']
        return c
    
    def beam(self, start_pos, direction) -> list[SingleBeamResult]:
        assert len(start_pos) == 2 and isinstance(start_pos[0], int) and isinstance(start_pos[1], int)
        cur_result: list[SingleBeamResult] = []
        have_reflected = False
        cur_pos = start_pos
        while True:
            cur_pos = get_next_pos(cur_pos, direction)
            if not in_bounds(cur_pos, self.N):
                break
            cur_pos_char = self.get_char(cur_pos)
            if cur_pos_char == '//':
                direction = {
                    'right': 'up',
                    'up': 'right',
                    'down': 'left',
                    'left': 'down'
                }[direction]
                have_reflected = True
            elif cur_pos_char == '\\':
                direction = {
                    'right': 'down',
                    'down': 'right',
                    'up': 'left',
                    'left': 'up'
                }[direction]
                have_reflected = True
            else:
                # not a mirror
                cur_result.append(SingleBeamResult(cur_pos, have_reflected))
        return cur_result
        
       
    def solve(self):
        assert self.solver is None
        solver = cp_model.CpSolver()
        self.solver = solver
        solver.parameters.num_search_workers = multiprocessing.cpu_count()
        solver.Solve(self.model)
        return solver
       
    def get_solved_pos(self, pos):
        for name in ['zombie', 'ghost', 'vampire']:
            var = self.model_vars[(pos, name)]
            if self.solver.Value(var) == 1:
                return name[0:2].upper()
        return None
            
        


def get_deltas(direction):
  if direction == 'right':
    return +1, 0
  elif direction == 'left':
    return -1, 0
  elif direction == 'down':
    return 0, +1
  elif direction == 'up':
    return 0, -1
  else:
    raise ValueError

def get_next_pos(cur_pos, direction):
    delta_x, delta_y = get_deltas(direction)
    return (cur_pos[0]+delta_y, cur_pos[1]+delta_x)

def in_bounds(pos, N):
  return 0 <= pos[0] < N and 0 <= pos[1] < N
