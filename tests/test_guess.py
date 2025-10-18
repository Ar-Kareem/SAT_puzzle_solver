from puzzle_solver import guess_solver as solver

assert solver.get_triplets(guess=((0, 'Y'), (1, 'R'), (2, 'R'), (3, 'R')), ground_truth=((0, 'Y'), (1, 'Y'), (2, 'R'), (3, 'R'))) == (3, 0, 1)
assert solver.get_triplets(guess=((0, 'R'), (1, 'Y'), (2, 'Y'), (3, 'Y')), ground_truth=((0, 'Y'), (1, 'Y'), (2, 'R'), (3, 'R'))) == (1, 2, 1)
assert solver.get_triplets(guess=((0, 'Y'), (1, 'Y'), (2, 'Y'), (3, 'R'), (4, 'R'), (5, 'R')), ground_truth=((0, 'R'), (1, 'G'), (2, 'B'), (3, 'Y'), (4, 'B'), (5, 'P'))) == (0, 2, 4)
assert solver.get_triplets(guess=((0, 'B'), (1, 'B'), (2, 'B'), (3, 'G'), (4, 'G'), (5, 'G')), ground_truth=((0, 'R'), (1, 'G'), (2, 'B'), (3, 'Y'), (4, 'B'), (5, 'P'))) == (1, 2, 3)
assert solver.get_triplets(guess=((0, 'P'), (1, 'P'), (2, 'P'), (3, 'O'), (4, 'O'), (5, 'O')), ground_truth=((0, 'R'), (1, 'G'), (2, 'B'), (3, 'Y'), (4, 'B'), (5, 'P'))) == (0, 1, 5)





def test_ground_1():
  binst = solver.Board()
  binst.add_guess(('R', 'Y', 'G', 'B'), (1, 1, 2))
  binst.add_guess(('R', 'G', 'O', 'P'), (0, 2, 2))
  ng, best_next_guess = binst.best_next_guess()
  print(best_next_guess)

def test_ground_2():
  binst = solver.Board()
  binst.add_guess(('R', 'Y', 'G', 'B'), (1, 1, 2))
  binst.add_guess(('R', 'G', 'O', 'P'), (0, 2, 2))
  binst.add_guess(('P', 'Y', 'Y', 'G'), (2, 1, 1))
  ng, best_next_guess = binst.best_next_guess()
  print(best_next_guess)

def test_ground_3():
  binst = solver.Board()
  binst.add_guess(('R', 'Y', 'G', 'B'), (0, 2, 2))  
  ng, best_next_guess = binst.best_next_guess()
  assert round(best_next_guess[1], 4) == 3.2269  # entropy of best next guess

def test_ground_4():
  binst = solver.Board()
  binst.add_guess(('R', 'Y', 'G', 'B'), (0, 2, 2))
  binst.add_guess(('Y', 'G', 'O', 'P'), (0, 2, 2))
  ng, best_next_guess = binst.best_next_guess()
  assert round(best_next_guess[1], 4) == 3.3037  # entropy of best next guess

def test_ground_5():
  binst = solver.Board()
  binst.add_guess(('R', 'Y', 'G', 'B'), (0, 2, 2))
  binst.add_guess(('Y', 'G', 'O', 'P'), (0, 2, 2))
  binst.add_guess(('G', 'P', 'B', 'P'), (1, 3, 0))
  ng, best_next_guess = binst.best_next_guess()
  assert isinstance(best_next_guess, list), 'when solution is found, best_next_guess should simply be a list of the solution'
  assert tuple(best_next_guess) == ('B', 'P', 'P', 'G')

def test_ground_6():
  binst = solver.Board(num_pegs=5, all_colors=['R', 'Y', 'G', 'B', 'O', 'P', 'Br', 'Cy'])
  binst.add_guess(('R', 'Y', 'G', 'B', 'O'), (0, 2, 3))
  binst.add_guess(('P', 'P', 'Br', 'Br', 'Cy'), (1, 1, 3))
  binst.add_guess(('G', 'Cy', 'Cy', 'Br', 'R'), (0, 1, 4))
  binst.add_guess(('Br', 'Br', 'B', 'Y', 'B'), (0, 1, 4))
  binst.add_guess(('P', 'R', 'Y', 'P', 'P'), (0, 3, 2))
  ng, best_next_guess = binst.best_next_guess()
  assert round(best_next_guess[1], 4) == 1.0000, 'only 2 possible ground truths left, so next guess cuts that in half (i.e. entropy is 1.0000)'

def test_ground_7():
  binst = solver.Board(num_pegs=5, all_colors=['R', 'Y', 'G', 'B', 'O', 'P', 'Br', 'Cy'])
  binst.add_guess(('R', 'Y', 'G', 'B', 'O'), (0, 2, 3))
  binst.add_guess(('P', 'P', 'Br', 'Br', 'Cy'), (1, 1, 3))
  binst.add_guess(('G', 'Cy', 'Cy', 'Br', 'R'), (1, 0, 4))
  binst.add_guess(('Br', 'Br', 'B', 'Y', 'B'), (0, 1, 4))
  binst.add_guess(('P', 'R', 'Y', 'P', 'P'), (0, 3, 2))
  ng, best_next_guess = binst.best_next_guess()
  assert round(best_next_guess[1], 4) == 1.0000, 'only 2 possible ground truths left, so next guess cuts that in half (i.e. entropy is 1.0000)'

# binst = solver.Board()
# binst.add_guess(('R', 'Y', 'G', 'B'), (1, 1, 2))  # 1 black dot, 1 white dot, 2 grey dots
# binst.add_guess(('R', 'G', 'O', 'P'), (0, 2, 2))  # 0 black dots, 2 white dots, 2 grey dots
# binst.add_guess(('P', 'Y', 'Y', 'G'), (2, 1, 1))  # 2 black dots, 1 white dot, 1 grey dot
# binst.best_next_guess()

# this is expected to take almost a year to run
# binst = solver.Board(num_pegs=6, all_colors=['R', 'Y', 'G', 'B', 'O', 'P', 'BB', 'GG', 'RR', 'YY', 'PP', 'OO'], show_progress=True)
# binst.best_next_guess()

if __name__ == '__main__':
  test_ground_1()
  test_ground_2()
  test_ground_3()
  test_ground_4()
  test_ground_5()
  test_ground_6()
  test_ground_7()