import numpy as np

from . import board

# https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/undead.html#7x7:5,12,11,aRdLcRdRRbLRRLRaRLaRaRLaRRaLLLdRe,3,0,3,0,5,6,0,0,8,0,4,2,2,4,0,2,8,3,1,2,5,2,2,0,0,8,4,1
bor = np.array([
  ['**', '//', '**', '**', '**', '**', '\\'],
  ['**', '**', '**', '//', '**', '**', '**'],
  ['**', '//', '//', '**', '**', '\\', '//'],
  ['//', '\\', '//', '**', '//', '\\', '**'],
  ['//', '**', '//', '\\', '**', '//', '//'],
  ['**', '\\', '\\', '\\', '**', '**', '**'],
  ['**', '//', '**', '**', '**', '**', '**'],
])
t = np.array([3, 0, 3, 0, 5, 6, 0])
b = np.array([5, 2, 1, 3, 8, 2, 0])
r = np.array([0, 8, 0, 4, 2, 2, 4])
l = np.array([1, 4, 8, 0, 0, 2, 2])
counts = {board.Monster.GHOST: 5, board.Monster.VAMPIRE: 12, board.Monster.ZOMBIE: 11}

# create board and solve
binst = board.Board(board=bor, sides={'top': t, 'bottom': b, 'right': r, 'left': l}, monster_count=counts)
solutions = binst.solve_and_print()

def test_ground():
  ground = np.array([
    ['VA', '//', 'GH', 'GH', 'ZO', 'GH', '\\'],
    ['VA', 'VA', 'VA', '//', 'ZO', 'ZO', 'ZO'],
    ['VA', '//', '//', 'ZO', 'ZO', '\\', '//'],
    ['//', '\\', '//', 'VA', '//', '\\', 'VA'],
    ['//', 'VA', '//', '\\', 'ZO', '//', '//'],
    ['ZO', '\\', '\\', '\\', 'ZO', 'VA', 'GH'],
    ['ZO', '//', 'VA', 'VA', 'ZO', 'VA', 'GH'],
  ])
  assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
  solution = solutions[0].assignment
  ground_assignment = {board.get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0]) if ground[y][x] in ['VA', 'GH', 'ZO']}
  assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
  for pos in solution.keys():
    assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'
