import numpy as np

from . import board

# https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/filling.html#17x13%23390801013916720
# bor = np.array([
#   ['*', '*', '*', '*', '*', '4', '*', '*', '*', '5', '*', '*', '*', '3', '2', '*', '*'],
#   ['6', '2', '*', '*', '*', '8', '*', '8', '8', '*', '*', '*', '4', '*', '5', '3', '*'],
#   ['*', '*', '2', '6', '*', '*', '8', '*', '8', '8', '*', '4', '4', '5', '*', '*', '*'],
#   ['*', '3', '*', '*', '7', '*', '7', '*', '*', '*', '4', '*', '9', '*', '4', '*', '*'],
#   ['*', '*', '*', '*', '*', '*', '7', '9', '*', '5', '3', '*', '2', '2', '4', '4', '1'],
#   ['*', '8', '*', '4', '4', '*', '*', '*', '5', '*', '*', '*', '*', '*', '*', '*', '*'],
#   ['*', '8', '*', '*', '*', '*', '*', '*', '*', '5', '3', '9', '6', '6', '6', '*', '8'],
#   ['*', '3', '*', '2', '8', '3', '8', '2', '2', '3', '*', '*', '6', '*', '*', '*', '3'],
#   ['*', '*', '*', '2', '4', '*', '*', '4', '*', '*', '*', '*', '5', '*', '*', '*', '*'],
#   ['*', '7', '*', '*', '*', '3', '*', '*', '*', '9', '*', '*', '*', '*', '7', '*', '*'],
#   ['*', '*', '7', '*', '7', '*', '*', '*', '*', '6', '*', '5', '6', '8', '*', '*', '*'],
#   ['6', '*', '*', '*', '7', '*', '6', '9', '*', '3', '*', '*', '5', '7', '*', '4', '*'],
#   ['2', '*', '*', '*', '7', '*', '*', '*', '*', '*', '9', '*', '*', '*', '7', '2', '*'],
# ])
# https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/filling.html#13x9%23954909678226244
# bor = np.array([
#   ['*', '*', '*', '*', '8', '*', '3', '*', '*', '*', '7', '*', '*'],
#   ['8', '8', '*', '*', '8', '*', '2', '5', '*', '*', '*', '*', '*'],
#   ['5', '*', '*', '*', '*', '*', '3', '*', '3', '*', '7', '2', '*'],
#   ['*', '*', '5', '*', '*', '*', '*', '5', '5', '*', '*', '7', '*'],
#   ['*', '*', '*', '8', '*', '6', '*', '*', '*', '8', '*', '3', '4'],
#   ['6', '*', '8', '*', '*', '9', '5', '7', '*', '*', '*', '*', '*'],
#   ['*', '6', '3', '*', '*', '*', '7', '*', '8', '*', '*', '4', '*'],
#   ['*', '*', '*', '5', '5', '5', '*', '3', '*', '*', '*', '*', '*'],
#   ['*', '*', '*', '4', '*', '4', '*', '*', '3', '5', '*', '2', '2'],
# ])

print('\n\nshould have 1 solution')
binst = board.Board(board=np.array([
  ['1', '3', '*'],
  ['3', '3', '*'],
]))
solutions = binst.solve_and_print()

print('\n\nshould have 1 solution')
binst = board.Board(board=np.array([
  ['4', '4', '*'],
  ['4', '4', '*'],
]))
solutions = binst.solve_and_print()

print('\n\nshould have 2 solutions')
binst = board.Board(board=np.array([
  ['1', '*', '*'],
  ['3', '3', '*'],
]))
solutions = binst.solve_and_print()

# https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/filling.html#9x7%23656829517556831
bor = np.array([
  ['*', '9', '4', '8', '*', '*', '8', '*', '*'],
  ['*', '*', '*', '*', '*', '8', '8', '*', '4'],
  ['*', '*', '2', '*', '*', '*', '*', '*', '3'],
  ['*', '*', '*', '*', '*', '4', '*', '7', '*'],
  ['*', '9', '4', '*', '*', '4', '8', '*', '7'],
  ['9', '*', '*', '3', '*', '8', '*', '*', '4'],
  ['*', '3', '3', '*', '*', '*', '8', '*', '*'],
])
# bor = np.array([
#   ['2', '5', '5', '5', '5'],
#   ['2', '1', '5', '3', '3'],
#   ['1', '*', '2', '3', '*'],
#   ['2', '*', '2', '*', '*'],
#   ['2', '*', '6', '6', '*'],
# ])
# bor = np.array([
#   ['1', '3', '*'],
#   ['3', '3', '*'],
# ])
binst = board.Board(board=bor)
solutions = binst.solve_and_print()

# def test_ground():
#   ground = np.array([
#   ])
#   assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
#   solution = solutions[0].assignment
#   ground_assignment = {board.get_pos(x=x, y=y): 1 if ground[y][x] == 'E' else 0 for x in range(ground.shape[1]) for y in range(ground.shape[0]) if ground[y][x] in [' ', 'E']}
#   assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
#   for pos in solution.keys():
#     assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'
