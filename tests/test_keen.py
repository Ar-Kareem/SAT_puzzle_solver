import numpy as np

from puzzle_solver import keen_solver as solver
from puzzle_solver.core.utils import get_pos


# https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/keen.html#9dn%23388677227852840
board = np.array([
  ['d01', 'd01', 'd03', 'd03', 'd05', 'd05', 'd08', 'd08', 'd10'],
  ['d02', 'd02', 'd03', 'd04', 'd06', 'd06', 'd09', 'd09', 'd10'],
  ['d12', 'd13', 'd14', 'd04', 'd07', 'd07', 'd07', 'd11', 'd11'],
  ['d12', 'd13', 'd14', 'd14', 'd15', 'd16', 'd11', 'd11', 'd18'],
  ['d19', 'd20', 'd24', 'd26', 'd15', 'd16', 'd16', 'd17', 'd18'],
  ['d19', 'd20', 'd24', 'd26', 'd28', 'd28', 'd29', 'd17', 'd33'],
  ['d21', 'd21', 'd24', 'd27', 'd30', 'd30', 'd29', 'd33', 'd33'],
  ['d22', 'd23', 'd25', 'd27', 'd31', 'd32', 'd34', 'd34', 'd36'],
  ['d22', 'd23', 'd25', 'd25', 'd31', 'd32', 'd35', 'd35', 'd36'],
])
block_results = {
  'd01': ('-', 1), 'd02': ('-', 1), 'd03': ('*', 378), 'd04': ('/', 4), 'd05': ('/', 2),
  'd06': ('-', 2), 'd07': ('*', 6), 'd08': ('+', 9), 'd09': ('/', 2), 'd10': ('+', 9),
  'd11': ('+', 22), 'd12': ('-', 1), 'd13': ('*', 30), 'd14': ('+', 12), 'd15': ('-', 1),
  'd16': ('*', 196), 'd17': ('*', 63), 'd18': ('-', 1), 'd19': ('/', 3), 'd20': ('/', 3),
  'd21': ('*', 21), 'd22': ('/', 4), 'd23': ('-', 7), 'd24': ('*', 64), 'd25': ('+', 15),
  'd26': ('-', 1), 'd27': ('+', 11), 'd28': ('-', 4), 'd29': ('/', 4), 'd30': ('*', 54),
  'd31': ('+', 11), 'd32': ('/', 4), 'd33': ('+', 16), 'd34': ('+', 15), 'd35': ('*', 30),
  'd36': ('-', 7),
}
clues = None
# clues = np.array([
#   [5, 4, 7, 9, 3, 6, 8, 1, 2],
#   [9, 8, 6, 1, 5, 3, 2, 4, 7],
#   [7, 5, 0, 0, 0, 0, 0, 0, 0],
#   [0, 0, 0, 0, 0, 0, 0, 0, 0],
#   [0, 0, 0, 0, 0, 0, 0, 0, 0],
#   [0, 0, 0, 0, 0, 0, 0, 0, 0],
#   [0, 0, 0, 0, 0, 0, 0, 0, 0],
#   [0, 0, 0, 0, 0, 0, 0, 0, 0],
#   [0, 0, 0, 0, 0, 0, 0, 0, 0],
# ])
# board = np.array([
#   ['d01', 'd03', 'd03', 'd08'],
#   ['d01', 'd04', 'd04', 'd08'],
#   ['d02', 'd05', 'd06', 'd06'],
#   ['d02', 'd05', 'd07', 'd07'],
# ])
# block_results = {
#   'd01': ('-', 1), 'd02': ('*', 12), 'd03': ('-', 1), 'd04': ('+', 5),
#   'd05': ('/', 2),
#   'd06': ('+', 4),
#   'd07': ('/', 2),
#   'd08': ('*', 6)
# }

def test_ground():
  binst = solver.Board(board=board, block_results=block_results, clues=clues)
  solutions = binst.solve_and_print()
  ground = np.array([
    [5, 4, 7, 9, 3, 6, 8, 1, 2],
    [9, 8, 6, 1, 5, 3, 2, 4, 7],
    [7, 5, 9, 4, 2, 1, 3, 8, 6],
    [8, 6, 1, 2, 9, 7, 5, 3, 4],
    [6, 1, 2, 5, 8, 4, 7, 9, 3],
    [2, 3, 8, 6, 1, 5, 4, 7, 9],
    [3, 7, 4, 8, 6, 9, 1, 2, 5],
    [4, 2, 5, 3, 7, 8, 9, 6, 1],
    [1, 9, 3, 7, 4, 2, 6, 5, 8],
  ])
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  ground_assignment = {get_pos(x=x, y=y): int(ground[y][x]) for x in range(ground.shape[1]) for y in range(ground.shape[0])}
  assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
  for pos in solution.keys():
    assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'

if __name__ == '__main__':
  test_ground()
