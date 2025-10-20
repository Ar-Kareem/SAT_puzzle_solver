import numpy as np

from puzzle_solver import minesweeper_solver as solver
from puzzle_solver.core.utils import get_pos, get_all_pos, get_char


def test_ground_1():
  # (click on (12, 5) initially to seed the puzzle) https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/mines.html#30x16n170%23833313602317986
  board = np.array([
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', '1', '1', '3', 'F', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '2', '2', '1', 'F', '4', 'F', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'F', '2', '1', '3', 'F', '5', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '2', '4', 'F', '3', '0', '3', 'F', 'F', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '3', '4', 'F', '3', '0', '2', 'F', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'F', '4', 'F', '2', '0', '2', '3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'F', '4', '1', '1', '0', '1', 'F', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'F', '4', '2', '1', '1', '2', '2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  ])
  mine_count = 30
  safe_positions, new_garuneed_mine_positions, wrong_flag_positions = solver.give_next_guess(board=board, mine_count=mine_count)
  ground_1 = {get_pos(x=9, y=0), get_pos(x=15, y=8), get_pos(x=15, y=7), get_pos(x=9, y=2), get_pos(x=15, y=6), get_pos(x=7, y=2), get_pos(x=9, y=1), get_pos(x=12, y=8)}
  ground_2 = {get_pos(x=8, y=2), get_pos(x=7, y=5), get_pos(x=10, y=0), get_pos(x=9, y=8)}
  ground_3 = {get_pos(x=15, y=3)}
  assert set(safe_positions) == ground_1, f'safe_positions != ground_1, {set(safe_positions) ^ ground_1}'
  assert set(new_garuneed_mine_positions) == ground_2, f'new_garuneed_mine_positions != ground_2, {set(new_garuneed_mine_positions) ^ ground_2}'
  assert set(wrong_flag_positions) == ground_3, f'wrong_flag_positions != ground_3, {set(wrong_flag_positions) ^ ground_3}'


def test_ground_2():
  # https://www.puzzle-minesweeper.com/minesweeper-10x10-hard/?e=NTo5LDk2Nyw1Njg=
  board = np.array([
    [' ', '1', '1', '1', '1', ' ', '2', ' ', ' ', ' '],
    [' ', ' ', '3', ' ', ' ', '2', ' ', '2', ' ', '1'],
    ['1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['1', '1', ' ', '2', ' ', ' ', '0', '1', ' ', '1'],
    ['0', '1', ' ', ' ', ' ', ' ', '3', ' ', ' ', ' '],
    [' ', '1', ' ', ' ', '1', ' ', ' ', ' ', '2', ' '],
    [' ', '3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1'],
    [' ', ' ', ' ', ' ', ' ', '2', ' ', '2', '1', ' '],
    ['2', '3', ' ', ' ', '1', ' ', '2', ' ', ' ', ' '],
    [' ', ' ', '2', '2', ' ', '0', ' ', ' ', ' ', '2'],
  ])
  safe_positions, new_garuneed_mine_positions, wrong_flag_positions = solver.give_next_guess(board=board)
  ground = np.array([
    ['M', ' ', ' ', ' ', ' ', 'S', ' ', 'M', 'S', 'M'],
    ['S', 'S', ' ', 'M', 'S', ' ', 'M', ' ', 'S', ' '],
    [' ', 'M', 'S', 'M', 'M', 'S', 'S', 'S', 'S', 'S'],
    [' ', ' ', 'S', ' ', 'S', 'S', ' ', ' ', 'M', ' '],
    [' ', ' ', 'S', 'S', 'S', 'S', ' ', 'S', 'S', 'S'],
    ['S', ' ', 'M', 'S', ' ', 'M', 'M', 'M', ' ', 'M'],
    ['S', ' ', 'S', 'S', 'S', 'S', 'M', 'S', 'S', ' '],
    ['M', 'M', 'S', 'S', 'S', ' ', 'M', ' ', ' ', 'S'],
    [' ', ' ', 'M', 'M', ' ', 'S', ' ', 'S', 'S', 'M'],
    ['S', 'S', ' ', ' ', 'S', ' ', 'S', 'M', 'M', ' '],
  ])
  ground_safe_positions = {p for p in get_all_pos(ground.shape[0], ground.shape[1]) if get_char(ground, p) == 'S'}
  ground_mine_positions = {p for p in get_all_pos(ground.shape[0], ground.shape[1]) if get_char(ground, p) == 'M'}
  assert set(safe_positions) == ground_safe_positions, f'safe_positions != ground_safe_positions, {set(safe_positions) ^ ground_safe_positions}'
  assert set(new_garuneed_mine_positions) == ground_mine_positions, f'new_garuneed_mine_positions != ground_mine_positions, {set(new_garuneed_mine_positions) ^ ground_mine_positions}'
  solver.print_board(
    board=board,
    safe_positions=safe_positions,
    new_garuneed_mine_positions=new_garuneed_mine_positions,
    wrong_flag_positions=wrong_flag_positions,
  )

if __name__ == '__main__':
  test_ground_1()
  test_ground_2()