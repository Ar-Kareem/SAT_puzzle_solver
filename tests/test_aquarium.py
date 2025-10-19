import numpy as np

from puzzle_solver import aquarium_solver as solver
from puzzle_solver.core.utils import get_pos

def test_ground_1():
  # https://www.puzzle-aquarium.com/?e=ODo0LDc2MCwxMDI=
  board = np.array([
    ['01', '01', '01', '01', '02', '02', '02', '03', '03', '03', '03', '04', '05', '05', '05'],
    ['01', '02', '02', '02', '02', '06', '07', '07', '03', '08', '03', '04', '04', '05', '09'],
    ['01', '01', '02', '11', '06', '06', '06', '12', '12', '08', '13', '13', '13', '09', '09'],
    ['01', '11', '11', '11', '14', '06', '06', '12', '12', '15', '15', '13', '09', '09', '09'],
    ['01', '01', '11', '11', '14', '12', '12', '12', '16', '16', '15', '13', '13', '17', '09'],
    ['45', '11', '11', '14', '14', '12', '42', '42', '42', '15', '15', '13', '13', '17', '18'],
    ['45', '11', '11', '14', '14', '12', '12', '43', '15', '15', '20', '13', '13', '17', '18'],
    ['46', '46', '11', '19', '19', '19', '43', '43', '44', '20', '20', '20', '13', '17', '18'],
    ['46', '22', '23', '23', '23', '19', '43', '21', '21', '24', '24', '24', '25', '17', '17'],
    ['22', '22', '22', '23', '19', '19', '26', '24', '24', '24', '28', '28', '25', '17', '33'],
    ['22', '22', '23', '23', '27', '27', '26', '26', '24', '24', '29', '29', '25', '25', '33'],
    ['22', '22', '35', '27', '27', '26', '26', '26', '26', '30', '30', '30', '25', '34', '34'],
    ['37', '22', '35', '35', '35', '35', '35', '26', '26', '30', '31', '31', '32', '32', '40'],
    ['37', '37', '37', '36', '36', '35', '26', '26', '26', '40', '40', '40', '40', '40', '40'],
    ['37', '37', '37', '37', '35', '35', '38', '38', '39', '39', '40', '40', '40', '41', '41'],
  ])
  top = np.array([6, 6, 5, 3, 3, 4, 7, 6, 9, 6, 3, 4, 9, 6, 7])
  side = np.array([3, 5, 1, 2, 5, 3, 10, 10, 5, 3, 7, 3, 7, 8, 12])
  binst = solver.Board(board=board, top=top, side=side)
  solutions = binst.solve_and_print()
  ground = np.array([
    ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '1', '1', '1', '1', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['1', '1', '0', '0', '0', '0', '0', '0', '1', '1', '0', '0', '0', '0', '1'],
    ['0', '0', '0', '0', '0', '0', '1', '1', '1', '0', '0', '0', '0', '0', '0'],
    ['1', '1', '1', '0', '0', '1', '1', '0', '1', '1', '0', '1', '1', '0', '1'],
    ['1', '1', '1', '0', '0', '0', '1', '1', '0', '1', '1', '1', '1', '0', '1'],
    ['1', '0', '0', '0', '0', '0', '1', '1', '1', '0', '0', '0', '1', '0', '0'],
    ['0', '0', '0', '0', '1', '1', '0', '0', '0', '0', '0', '0', '1', '0', '0'],
    ['0', '0', '1', '1', '0', '0', '0', '0', '1', '1', '0', '0', '1', '1', '1'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1'],
    ['0', '1', '0', '0', '0', '0', '0', '1', '1', '0', '1', '1', '1', '1', '0'],
    ['1', '1', '1', '1', '1', '0', '1', '1', '1', '0', '0', '0', '0', '0', '0'],
    ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '0', '0', '1', '1'],
  ])
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  ground_assignment = {get_pos(x=x, y=y): int(ground[y][x]) for x in range(ground.shape[1]) for y in range(ground.shape[0])}
  assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
  for pos in solution.keys():
    assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_ground_2():
  # https://www.puzzle-aquarium.com/?e=MDo4LDU1Myw3MjE=
  board = np.array([
    ['1', '1', '2', '2', '3', '3'],
    ['4', '5', '3', '3', '3', '6'],
    ['4', '5', '3', '3', '6', '6'],
    ['4', '5', '3', '3', '3', '6'],
    ['5', '5', '6', '6', '3', '6'],
    ['5', '5', '6', '6', '6', '6'],
  ])
  top = np.array([2, 1, 3, 3, 3, 5])
  side = np.array([4, 1, 2, 2, 4, 4])
  binst = solver.Board(board=board, top=top, side=side)
  solutions = binst.solve_and_print()
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  ground = np.array([
    ['1', '1', '1', '1', '0', '0'],
    ['0', '0', '0', '0', '0', '1'],
    ['0', '0', '0', '0', '1', '1'],
    ['1', '0', '0', '0', '0', '1'],
    ['0', '0', '1', '1', '1', '1'],
    ['0', '0', '1', '1', '1', '1'],
  ])
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  ground_assignment = {get_pos(x=x, y=y): int(ground[y][x]) for x in range(ground.shape[1]) for y in range(ground.shape[0])}
  assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
  for pos in solution.keys():
    assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'

if __name__ == '__main__':
  test_ground_1()
  test_ground_2()