from . import solver

assert solver.get_triplets(guess=((0, 'Y'), (1, 'R'), (2, 'R'), (3, 'R')), ground_truth=((0, 'Y'), (1, 'Y'), (2, 'R'), (3, 'R'))) == (3, 0, 1)
assert solver.get_triplets(guess=((0, 'R'), (1, 'Y'), (2, 'Y'), (3, 'Y')), ground_truth=((0, 'Y'), (1, 'Y'), (2, 'R'), (3, 'R'))) == (1, 2, 1)
assert solver.get_triplets(guess=((0, 'Y'), (1, 'Y'), (2, 'Y'), (3, 'R'), (4, 'R'), (5, 'R')), ground_truth=((0, 'R'), (1, 'G'), (2, 'B'), (3, 'Y'), (4, 'B'), (5, 'P'))) == (0, 2, 4)
assert solver.get_triplets(guess=((0, 'B'), (1, 'B'), (2, 'B'), (3, 'G'), (4, 'G'), (5, 'G')), ground_truth=((0, 'R'), (1, 'G'), (2, 'B'), (3, 'Y'), (4, 'B'), (5, 'P'))) == (1, 2, 3)
assert solver.get_triplets(guess=((0, 'P'), (1, 'P'), (2, 'P'), (3, 'O'), (4, 'O'), (5, 'O')), ground_truth=((0, 'R'), (1, 'G'), (2, 'B'), (3, 'Y'), (4, 'B'), (5, 'P'))) == (0, 1, 5)


all_colors = ['R', 'Y', 'G', 'B', 'O', 'P']
num_pegs = 4
previous_guesses = [
  (('R', 'Y', 'G', 'B'), (0, 2, 2)),
  (('Y', 'G', 'O', 'P'), (0, 2, 2)),
  (('G', 'P', 'B', 'P'), (1, 3, 0)),
]

best_next_guess = solver.best_next_guess(previous_guesses=previous_guesses[:1], num_pegs=num_pegs, all_colors=all_colors)
assert round(best_next_guess[1], 4) == 3.2269  # entropy of best next guess
best_next_guess = solver.best_next_guess(previous_guesses=previous_guesses[:2], num_pegs=num_pegs, all_colors=all_colors)
assert round(best_next_guess[1], 4) == 3.3037  # entropy of best next guess
best_next_guess = solver.best_next_guess(previous_guesses=previous_guesses, num_pegs=num_pegs, all_colors=all_colors)
assert isinstance(best_next_guess, list), 'when solution is found, best_next_guess should simply be a list of the solution'
assert tuple(best_next_guess) == ('B', 'P', 'P', 'G')