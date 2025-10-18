import numpy as np

from puzzle_solver import mosaic_solver as solver
from puzzle_solver.core.utils import get_pos

# https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/mosaic.html#15x15:b21c3a422b43c4e4a2b4b5a5b5a3325c7a4b5e5b67b4a7d77a3b3a57764a4a5c4a578a5a1345b5a43c7a3a3b3f5a6e4a7a5b467a3a3a5g6b35e5453a7b566a2c34c7b7a31b5c5c6a6c3a2a3a2f
board = np.array([
  [' ', ' ', '2', '1', ' ', ' ', ' ', '3', ' ', '4', '2', '2', ' ', ' ', '4'],
  ['3', ' ', ' ', ' ', '4', ' ', ' ', ' ', ' ', ' ', '4', ' ', '2', ' ', ' '],
  ['4', ' ', ' ', '5', ' ', '5', ' ', ' ', '5', ' ', '3', '3', '2', '5', ' '],
  [' ', ' ', '7', ' ', '4', ' ', ' ', '5', ' ', ' ', ' ', ' ', ' ', '5', ' '],
  [' ', '6', '7', ' ', ' ', '4', ' ', '7', ' ', ' ', ' ', ' ', '7', '7', ' '],
  ['3', ' ', ' ', '3', ' ', '5', '7', '7', '6', '4', ' ', '4', ' ', '5', ' '],
  [' ', ' ', '4', ' ', '5', '7', '8', ' ', '5', ' ', '1', '3', '4', '5', ' '],
  [' ', '5', ' ', '4', '3', ' ', ' ', ' ', '7', ' ', '3', ' ', '3', ' ', ' '],
  ['3', ' ', ' ', ' ', ' ', ' ', ' ', '5', ' ', '6', ' ', ' ', ' ', ' ', ' '],
  ['4', ' ', '7', ' ', '5', ' ', ' ', '4', '6', '7', ' ', '3', ' ', '3', ' '],
  ['5', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '6', ' ', ' ', '3', '5', ' ', ' '],
  [' ', ' ', ' ', '5', '4', '5', '3', ' ', '7', ' ', ' ', '5', '6', '6', ' '],
  ['2', ' ', ' ', ' ', '3', '4', ' ', ' ', ' ', '7', ' ', ' ', '7', ' ', '3'],
  ['1', ' ', ' ', '5', ' ', ' ', ' ', '5', ' ', ' ', ' ', '6', ' ', '6', ' '],
  [' ', ' ', '3', ' ', '2', ' ', '3', ' ', '2', ' ', ' ', ' ', ' ', ' ', ' ']
])

def test_ground():
  binst = solver.Board(board=board)
  solutions = binst.solve_and_print()
  ground = np.array([
    [' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', 'B', ' ', 'B', ' ', ' ', 'B', 'B'],
    [' ', 'B', ' ', ' ', 'B', 'B', ' ', 'B', 'B', ' ', 'B', ' ', ' ', 'B', 'B'],
    [' ', 'B', 'B', ' ', 'B', 'B', ' ', ' ', ' ', 'B', 'B', ' ', ' ', ' ', 'B'],
    ['B', 'B', 'B', 'B', ' ', ' ', 'B', 'B', 'B', ' ', ' ', ' ', 'B', ' ', 'B'],
    [' ', 'B', 'B', ' ', ' ', 'B', ' ', 'B', 'B', 'B', ' ', 'B', 'B', 'B', ' '],
    [' ', 'B', ' ', 'B', ' ', 'B', 'B', ' ', 'B', ' ', ' ', 'B', 'B', 'B', 'B'],
    ['B', ' ', 'B', ' ', ' ', 'B', 'B', 'B', 'B', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', 'B', ' ', 'B', 'B', 'B', 'B', 'B', ' ', ' ', ' ', 'B', ' ', 'B'],
    [' ', 'B', 'B', ' ', ' ', ' ', ' ', 'B', 'B', 'B', 'B', 'B', ' ', 'B', ' '],
    ['B', 'B', 'B', 'B', 'B', 'B', ' ', ' ', ' ', 'B', 'B', ' ', ' ', 'B', ' '],
    [' ', 'B', ' ', 'B', 'B', ' ', 'B', ' ', 'B', 'B', ' ', ' ', ' ', 'B', ' '],
    ['B', 'B', ' ', ' ', 'B', ' ', ' ', 'B', 'B', 'B', ' ', 'B', 'B', 'B', 'B'],
    [' ', ' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B', 'B', 'B', 'B', 'B', ' ', 'B'],
    [' ', ' ', 'B', 'B', ' ', ' ', 'B', ' ', 'B', 'B', ' ', 'B', 'B', ' ', ' '],
    ['B', ' ', 'B', ' ', ' ', 'B', 'B', ' ', ' ', ' ', ' ', ' ', 'B', 'B', 'B'],
  ])
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  ground_assignment = {get_pos(x=x, y=y): 1 if ground[y][x] == 'B' else 0 for x in range(ground.shape[1]) for y in range(ground.shape[0])}
  assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
  for pos in solution.keys():
    assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'

if __name__ == '__main__':
  test_ground()
