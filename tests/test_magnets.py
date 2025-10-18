import numpy as np

from puzzle_solver import magnets_solver as solver
from puzzle_solver.core.utils import get_pos

# define board and parameters
# bor = np.array([
#   ['H', 'H', 'H', 'H', 'V'],
#   ['V', 'V', 'H', 'H', 'V'],
#   ['V', 'V', 'H', 'H', 'V'],
#   ['H', 'H', 'H', 'H', 'V'],
#   ['V', 'H', 'H', 'V', 'V'],
#   ['V', 'H', 'H', 'V', 'V'],
# ])
# pos_v = np.array([3, 2, 2, 0, 2])
# neg_v = np.array([2, 2, 1, 2, 2])
# pos_h = np.array([2, 1, 1, 2, 2, 1])
# neg_h = np.array([1, 2, 1, 2, 2, 1])
# https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/magnets.html#10x9:..3533.3.4,5...5.31.,.234.34344,4.4.54.2.,LRLRTTTTLRLRLRBBBBTTLRLRLRLRBBTTTLRLRLRTBBBTTTTLRBTLRBBBBTTTBTTTTLRBBBTBBBBTLRLRBLRLRBLRLR
bor = np.array([
  ['H', 'H', 'H', 'H', 'V', 'V', 'V', 'V', 'H', 'H'],
  ['H', 'H', 'H', 'H', 'V', 'V', 'V', 'V', 'V', 'V'],
  ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'V', 'V'],
  ['V', 'V', 'V', 'H', 'H', 'H', 'H', 'H', 'H', 'V'],
  ['V', 'V', 'V', 'V', 'V', 'V', 'V', 'H', 'H', 'V'],
  ['V', 'H', 'H', 'V', 'V', 'V', 'V', 'V', 'V', 'V'],
  ['V', 'V', 'V', 'V', 'V', 'H', 'H', 'V', 'V', 'V'],
  ['V', 'V', 'V', 'V', 'V', 'V', 'H', 'H', 'H', 'H'],
  ['V', 'H', 'H', 'H', 'H', 'V', 'H', 'H', 'H', 'H'],
])
pos_v = np.array([-1, -1, 3, 5, 3, 3, -1, 3, -1, 4])
neg_v = np.array([-1, 2, 3, 4, -1, 3, 4, 3, 4, 4])
pos_h = np.array([5, -1, -1, -1, 5, -1, 3, 1, -1])
neg_h = np.array([4, -1, 4, -1, 5, 4, -1, 2, -1])


def test_ground():
  binst = solver.Board(board=bor, sides={'pos_v': pos_v, 'neg_v': neg_v, 'pos_h': pos_h, 'neg_h': neg_h})
  solutions = binst.solve_and_print()
  ground = np.array([
    ['-', '+', '-', '+', ' ', '+', '-', '+', '-', '+'],
    [' ', ' ', '+', '-', ' ', '-', '+', '-', '+', '-'],
    ['-', '+', '-', '+', ' ', ' ', '-', '+', '-', '+'],
    ['+', '-', '+', '-', '+', '-', '+', '-', '+', '-'],
    ['-', '+', '-', '+', '-', '+', '-', '+', '-', '+'],
    [' ', '-', '+', '-', '+', '-', '+', ' ', '+', '-'],
    [' ', ' ', ' ', '+', '-', '+', '-', ' ', '-', '+'],
    ['-', ' ', ' ', '-', '+', ' ', ' ', ' ', ' ', ' '],
    ['+', ' ', ' ', '+', '-', ' ', '+', '-', '+', '-'],
  ])
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
  assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
  for pos in solution.keys():
    assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'

if __name__ == '__main__':
  test_ground()
