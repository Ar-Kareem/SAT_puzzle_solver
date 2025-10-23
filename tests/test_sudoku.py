import numpy as np

from puzzle_solver import sudoku_solver as solver
from puzzle_solver.core.utils import get_pos


def test_ground():
  # The link takes a few seconds to load
  # https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/solo.html#4x4du%23149435502448981
  board = np.array([
    [' ', '7', '5', '4',  '9', '1', 'c', 'e',  'd', 'f', ' ', ' ',  '2', ' ', '3', ' '],
    [' ', ' ', ' ', ' ',  'f', 'a', ' ', ' ',  ' ', '6', ' ', 'c',  ' ', ' ', '8', 'b'],
    [' ', ' ', '1', ' ',  ' ', '6', ' ', ' ',  ' ', '9', ' ', ' ',  ' ', 'g', ' ', 'd'],
    [' ', '6', ' ', ' ',  ' ', ' ', ' ', ' ',  ' ', ' ', '5', 'g',  'c', '7', ' ', ' '],

    ['4', 'a', ' ', ' ',  ' ', ' ', ' ', ' ',  ' ', ' ', ' ', '9',  ' ', ' ', ' ', ' '],
    [' ', 'g', 'f', ' ',  'e', ' ', ' ', '5',  '4', ' ', ' ', '1',  ' ', '9', ' ', '8'],
    [' ', ' ', ' ', ' ',  'a', '3', 'b', '7',  'c', 'g', ' ', '6',  ' ', ' ', ' ', '4'],
    [' ', 'b', ' ', '7',  ' ', ' ', ' ', ' ',  'f', ' ', '3', ' ',  ' ', 'a', ' ', '6'],

    ['2', ' ', 'a', ' ',  ' ', 'c', ' ', '1',  ' ', ' ', ' ', ' ',  '7', ' ', '6', ' '],
    ['8', ' ', ' ', ' ',  '3', ' ', 'e', 'f',  '7', '5', 'c', 'd',  ' ', ' ', ' ', ' '],
    ['9', ' ', '3', ' ',  '7', ' ', ' ', 'a',  '6', ' ', ' ', '2',  ' ', 'b', '1', ' '],
    [' ', ' ', ' ', ' ',  '4', ' ', ' ', ' ',  ' ', ' ', ' ', ' ',  ' ', ' ', 'e', 'f'],

    [' ', ' ', 'g', 'd',  '2', '9', ' ', ' ',  ' ', ' ', ' ', ' ',  ' ', ' ', '4', ' '],
    ['a', ' ', 'b', ' ',  ' ', ' ', '5', ' ',  ' ', ' ', 'd', ' ',  ' ', '8', ' ', ' '],
    ['e', '8', ' ', ' ',  '1', ' ', '4', ' ',  ' ', ' ', '6', '7',  ' ', ' ', ' ', ' '],
    [' ', '3', ' ', '9',  ' ', ' ', 'f', '8',  'a', 'e', 'g', '5',  'b', 'c', 'd', ' '],
  ])
  binst = solver.Board(board=board)
  solutions = binst.solve_and_print()
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  ground = np.array([
    ['g', '7', '5', '4', '9', '1', 'c', 'e', 'd', 'f', 'b', '8', '2', '6', '3', 'a'],
    ['3', '9', 'd', 'e', 'f', 'a', '7', 'g', '2', '6', '4', 'c', '5', '1', '8', 'b'],
    ['b', 'c', '1', '8', '5', '6', '3', '2', 'e', '9', '7', 'a', '4', 'g', 'f', 'd'],
    ['f', '6', '2', 'a', 'b', '8', 'd', '4', '1', '3', '5', 'g', 'c', '7', '9', 'e'],
    ['4', 'a', 'e', '3', '8', 'f', '1', '6', '5', 'b', '2', '9', 'g', 'd', 'c', '7'],
    ['6', 'g', 'f', 'c', 'e', 'd', '2', '5', '4', '7', 'a', '1', '3', '9', 'b', '8'],
    ['d', '1', '9', '2', 'a', '3', 'b', '7', 'c', 'g', '8', '6', 'e', 'f', '5', '4'],
    ['5', 'b', '8', '7', 'g', '4', '9', 'c', 'f', 'd', '3', 'e', '1', 'a', '2', '6'],
    ['2', 'e', 'a', 'b', 'd', 'c', 'g', '1', '3', '8', '9', 'f', '7', '4', '6', '5'],
    ['8', '4', '6', '1', '3', 'b', 'e', 'f', '7', '5', 'c', 'd', 'a', '2', 'g', '9'],
    ['9', 'f', '3', 'g', '7', '5', '8', 'a', '6', '4', 'e', '2', 'd', 'b', '1', 'c'],
    ['c', 'd', '7', '5', '4', '2', '6', '9', 'g', 'a', '1', 'b', '8', '3', 'e', 'f'],
    ['7', '5', 'g', 'd', '2', '9', 'a', 'b', '8', 'c', 'f', '3', '6', 'e', '4', '1'],
    ['a', '2', 'b', '6', 'c', 'e', '5', '3', '9', '1', 'd', '4', 'f', '8', '7', 'g'],
    ['e', '8', 'c', 'f', '1', 'g', '4', 'd', 'b', '2', '6', '7', '9', '5', 'a', '3'],
    ['1', '3', '4', '9', '6', '7', 'f', '8', 'a', 'e', 'g', '5', 'b', 'c', 'd', '2'],
  ])
  ground_assignment = {get_pos(x=x, y=y): ord(ground[y][x]) - ord('a') + 10 if ground[y][x].isalpha() else int(ground[y][x]) for x in range(ground.shape[1]) for y in range(ground.shape[0])}
  assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys())} != {set(ground_assignment.keys())}'
  for pos in solution.keys():
    assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_ground_2():
  # 3x4 
  # https://www.puzzle-sudoku.com/?e=Njo3LDE0NywwMTg=
  board = np.array([
    [' ', ' ', 'B', '1',  '2', '6', 'C', ' ',  ' ', ' ', '4', '3'],
    [' ', ' ', ' ', ' ',  'B', ' ', '1', ' ',  ' ', '9', ' ', ' '],
    ['4', ' ', ' ', ' ',  ' ', '5', ' ', 'A',  ' ', ' ', ' ', ' '],

    [' ', ' ', '9', '5',  ' ', ' ', ' ', ' ',  ' ', ' ', '7', ' '],
    [' ', ' ', ' ', 'C',  ' ', ' ', ' ', '5',  ' ', ' ', ' ', 'A'],
    ['6', 'B', ' ', '7',  ' ', '9', ' ', '4',  ' ', '1', '2', '5'],

    ['C', '6', '8', ' ',  '3', ' ', '5', ' ',  '4', ' ', '1', '9'],
    ['2', ' ', ' ', ' ',  'A', ' ', ' ', ' ',  'C', ' ', ' ', ' '],
    [' ', '1', ' ', ' ',  ' ', ' ', ' ', ' ',  '6', '8', ' ', ' '],

    [' ', ' ', ' ', ' ',  '5', ' ', '3', ' ',  ' ', ' ', ' ', '4'],
    [' ', ' ', '1', ' ',  ' ', '2', ' ', '9',  ' ', ' ', ' ', ' '],
    ['9', 'A', ' ', ' ',  ' ', '1', '4', '6',  '3', '5', ' ', ' '],
  ])
  binst = solver.Board(board=board, block_size=(3, 4))
  solutions = binst.solve_and_print()
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  ground = np.array([
    ['8', '9', 'b', '1', '2', '6', 'c', '7', '5', 'a', '4', '3'],
    ['5', 'c', 'a', '2', 'b', '4', '1', '3', '7', '9', '6', '8'],
    ['4', '3', '7', '6', '9', '5', '8', 'a', '2', 'c', 'b', '1'],
    ['a', '4', '9', '5', '1', '3', '2', '8', 'b', '6', '7', 'c'],
    ['1', '8', '2', 'c', '6', 'b', '7', '5', '9', '4', '3', 'a'],
    ['6', 'b', '3', '7', 'c', '9', 'a', '4', '8', '1', '2', '5'],
    ['c', '6', '8', 'a', '3', '7', '5', 'b', '4', '2', '1', '9'],
    ['2', '7', '4', '9', 'a', '8', '6', '1', 'c', '3', '5', 'b'],
    ['b', '1', '5', '3', '4', 'c', '9', '2', '6', '8', 'a', '7'],
    ['7', '2', '6', '8', '5', 'a', '3', 'c', '1', 'b', '9', '4'],
    ['3', '5', '1', '4', '8', '2', 'b', '9', 'a', '7', 'c', '6'],
    ['9', 'a', 'c', 'b', '7', '1', '4', '6', '3', '5', '8', '2'],
  ])
  ground_assignment = {get_pos(x=x, y=y): ord(ground[y][x]) - ord('a') + 10 if ground[y][x].isalpha() else int(ground[y][x]) for x in range(ground.shape[1]) for y in range(ground.shape[0])}
  assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys())} != {set(ground_assignment.keys())}'
  for pos in solution.keys():
    assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


def test_ground_sandwich_sudoku():
  # sandwich
  # https://www.puzzle-sudoku.com/?pl=190ae719ceba799483eadd7264127b3068f9d981c1af0
  board = np.array([
    [ ' ', ' ', ' ',  '6', ' ', ' ',  ' ', '9', ' ' ],
    [ ' ', '8', ' ',  ' ', ' ', '5',  ' ', ' ', ' ' ],
    [ ' ', ' ', ' ',  ' ', '1', ' ',  ' ', '3', ' ' ],

    [ ' ', ' ', ' ',  ' ', ' ', ' ',  '3', ' ', ' ' ],
    [ ' ', ' ', ' ',  ' ', ' ', ' ',  ' ', ' ', ' ' ],
    [ ' ', ' ', '3',  ' ', ' ', ' ',  ' ', ' ', ' ' ],

    [ ' ', '7', ' ',  ' ', '9', ' ',  ' ', ' ', ' ' ],
    [ ' ', ' ', ' ',  '3', ' ', ' ',  ' ', '4', ' ' ],
    [ ' ', '9', ' ',  ' ', ' ', '6',  ' ', ' ', ' ' ],
  ])
  binst = solver.Board(board=board, sandwich={'side': [25, 29, 0, 9, 5, 18, 0, 18, 22], 'bottom': [11, 0, 15, 0, 16, 0, 0, 0, 4]})
  solutions = binst.solve_and_print()
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  ground = np.array([
    ['5', '3', '1', '6', '4', '7', '8', '9', '2'],
    ['9', '8', '7', '2', '3', '5', '4', '1', '6'],
    ['4', '2', '6', '8', '1', '9', '7', '3', '5'],
    ['7', '4', '2', '5', '8', '1', '3', '6', '9'],
    ['1', '5', '9', '7', '6', '3', '2', '8', '4'],
    ['8', '6', '3', '9', '2', '4', '5', '7', '1'],
    ['2', '7', '4', '1', '9', '8', '6', '5', '3'],
    ['6', '1', '8', '3', '5', '2', '9', '4', '7'],
    ['3', '9', '5', '4', '7', '6', '1', '2', '8'],
  ])


def test_ground_x():
  # x variant, no diagonal dups
  # https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/solo.html#3x3x:h1a5a8_7c2a1_3b6d6d3c8e9c9d2d6b2_5a3c5_7a4a5h
  board = np.array([
    [ ' ', ' ', ' ',  ' ', ' ', ' ',  ' ', ' ', '1' ],
    [ ' ', '5', ' ',  '8', '7', ' ',  ' ', ' ', '2' ],
    [ ' ', '1', '3',  ' ', ' ', '6',  ' ', ' ', ' ' ],

    [ ' ', '6', ' ',  ' ', ' ', ' ',  '3', ' ', ' ' ],
    [ ' ', '8', ' ',  ' ', ' ', ' ',  ' ', '9', ' ' ],
    [ ' ', ' ', '9',  ' ', ' ', ' ',  ' ', '2', ' ' ],

    [ ' ', ' ', ' ',  '6', ' ', ' ',  '2', '5', ' ' ],
    [ '3', ' ', ' ',  ' ', '5', '7',  ' ', '4', ' ' ],
    [ '5', ' ', ' ',  ' ', ' ', ' ',  ' ', ' ', ' ' ],
  ])
  binst = solver.Board(board=board, unique_diagonal=True)
  solutions = binst.solve_and_print()
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  ground = np.array([
    ['7', '9', '2', '4', '3', '5', '8', '6', '1'],
    ['6', '5', '4', '8', '7', '1', '9', '3', '2'],
    ['8', '1', '3', '2', '9', '6', '4', '7', '5'],
    ['4', '6', '5', '1', '2', '9', '3', '8', '7'],
    ['2', '8', '7', '5', '6', '3', '1', '9', '4'],
    ['1', '3', '9', '7', '4', '8', '5', '2', '6'],
    ['9', '7', '8', '6', '1', '4', '2', '5', '3'],
    ['3', '2', '1', '9', '5', '7', '6', '4', '8'],
    ['5', '4', '6', '3', '8', '2', '7', '1', '9'],
  ])
  ground_assignment = {get_pos(x=x, y=y): ord(ground[y][x]) - ord('a') + 10 if ground[y][x].isalpha() else int(ground[y][x]) for x in range(ground.shape[1]) for y in range(ground.shape[0])}
  assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys())} != {set(ground_assignment.keys())}'
  for pos in solution.keys():
    assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'

if __name__ == '__main__':
  test_ground()
  test_ground_2()
  test_ground_sandwich_sudoku()
  test_ground_x()
