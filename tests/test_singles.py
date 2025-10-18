import numpy as np

from puzzle_solver import singles_solver as solver
from puzzle_solver.core.utils import get_pos

# https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/singles.html#12x12dk%23215229029446280
board = np.array([
  [1, 6, 5, 4, 9, 8, 9, 3, 5, 1, 3, 7],
  [2, 8, 5, 7, 1, 1, 4, 3, 6, 3, 10, 7],
  [6, 7, 7, 11, 2, 6, 3, 10, 10, 2, 3, 3],
  [11, 9, 4, 3, 6, 1, 2, 5, 3, 10, 7, 8], 
  [5, 5, 4, 9, 7, 9, 6, 6, 11, 5, 4, 11],
  [1, 3, 7, 9, 12, 5, 4, 2, 9, 6, 12, 4],
  [6, 11, 1, 3, 6, 4, 11, 2, 2, 10, 8, 10],
  [3, 11, 12, 6, 2, 9, 9, 1, 4, 8, 12, 5],
  [4, 8, 8, 5, 11, 3, 3, 6, 5, 9, 1, 4],
  [2, 4, 6, 2, 1, 10, 1, 10, 8, 5, 4, 6],
  [5, 1, 6, 10, 9, 4, 8, 4, 8, 3, 2, 12],
  [11, 2, 12, 10, 8, 3, 5, 4, 10, 4, 8, 11],
])

def test_ground():
  binst = solver.Board(board=board)
  solutions = binst.solve_and_print()
  ground = np.array([
    ['B', ' ', 'B', ' ', 'B', ' ', ' ', 'B', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', 'B', ' ', 'B'],
    ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B', ' '],
    [' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['B', ' ', 'B', ' ', ' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'],
    [' ', ' ', ' ', 'B', ' ', ' ', 'B', ' ', ' ', ' ', 'B', ' '],
    [' ', 'B', ' ', ' ', 'B', ' ', ' ', 'B', ' ', 'B', ' ', ' '],
    [' ', ' ', 'B', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' '],
    [' ', 'B', ' ', ' ', ' ', 'B', ' ', ' ', 'B', ' ', ' ', 'B'],
    ['B', ' ', 'B', ' ', 'B', ' ', ' ', 'B', ' ', ' ', 'B', ' '],
    [' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', 'B', ' ', ' ', ' '],
    ['B', ' ', ' ', 'B', ' ', ' ', ' ', 'B', ' ', ' ', 'B', ' '],
  ])
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  ground_assignment = {get_pos(x=x, y=y): 1 if ground[y][x] == 'B' else 0 for x in range(ground.shape[1]) for y in range(ground.shape[0])}
  assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
  for pos in solution.keys():
    assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'

if __name__ == '__main__':
  test_ground()
