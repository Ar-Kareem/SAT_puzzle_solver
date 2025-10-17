import time
import numpy as np

from . import solver
from core.utils import get_pos

assert solver.get_triplets(guess=((0, 'Y'), (1, 'R'), (2, 'R'), (3, 'R')), ground_truth=((0, 'Y'), (1, 'Y'), (2, 'R'), (3, 'R'))) == (3, 0, 1)
assert solver.get_triplets(guess=((0, 'R'), (1, 'Y'), (2, 'Y'), (3, 'Y')), ground_truth=((0, 'Y'), (1, 'Y'), (2, 'R'), (3, 'R'))) == (1, 2, 1)


all_colors = ['R', 'Y', 'G', 'B', 'O', 'P']
int_to_color = {i: c for i, c in enumerate(all_colors)}

guess=((0, 'R'), (1, 'Y'), (2, 'Y'), (3, 'G'))
n = len(guess)
POSSIBLE_TRIPLETS = set((i, j, n-i-j) for i in range(n+1) for j in range(n+1-i))
possible_ground_truths=set(
  (int_to_color[i], int_to_color[j], int_to_color[k], int_to_color[l]) for i in range(len(all_colors)) for j in range(len(all_colors)) for k in range(len(all_colors)) for l in range(len(all_colors))
)
possible_ground_truths = tuple({(i, color) for i, color in enumerate(ground_truth)} for ground_truth in possible_ground_truths)
print('# possible ground truths:', len(possible_ground_truths))
print('# possible triplets:', len(POSSIBLE_TRIPLETS))

r = solver.slow_information_gain(guess=guess, possible_ground_truths=possible_ground_truths, possible_triplets=POSSIBLE_TRIPLETS)
print(sorted(r.items()))


tic = time.time()
N = 10**3
for _ in range(N):
  r = solver.slow_information_gain(guess=guess, possible_ground_truths=possible_ground_truths, possible_triplets=POSSIBLE_TRIPLETS)
toc = time.time()
ttaken = ((toc - tic)*1000) / N # milliseconds
print(f'Time taken: {ttaken:.2f} ms')
