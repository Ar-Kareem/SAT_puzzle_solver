from collections import Counter, defaultdict
from itertools import product

import numpy as np


class Board:
    def __init__(self, num_pegs: int = 4, all_colors: list[str] = ['R', 'Y', 'G', 'B', 'O', 'P'], show_warnings: bool = True, show_progress: bool = False):
        assert num_pegs >= 1, 'num_pegs must be at least 1'
        assert len(all_colors) == len(set(all_colors)), 'all_colors must contain only unique colors'
        self.previous_guesses = []
        self.num_pegs = num_pegs
        self.all_colors = all_colors
        self.show_progress = show_progress
        self.tqdm = None
        if self.show_progress:
            try:
                from tqdm import tqdm
                self.tqdm = tqdm
            except ImportError:
                print('tqdm is not installed, so progress bar will not be shown')
                self.tqdm = None
        self.possible_triplets = set((i, j, num_pegs-i-j) for i in range(num_pegs+1) for j in range(num_pegs+1-i))
        int_to_color = {i: c for i, c in enumerate(self.all_colors)}
        c = len(self.all_colors)**num_pegs
        if c > 10**5 and show_warnings:
            print(f'Warning: len(all_colors)**num_pegs is too large (= {c:,}). The solver may take infinitely long to run.')
        self.all_possible_pegs = tuple({(i, int_to_color[int_]) for i, int_ in enumerate(ints)} for ints in product(range(len(self.all_colors)), repeat=num_pegs))

    def add_guess(self, guess: tuple[tuple[int, str]], guess_result: tuple[int, int, int]):
        assert len(guess) == self.num_pegs, 'previous guess must have the same number of pegs as the game'
        assert not set(guess) - set(self.all_colors), f'previous guess must contain only colors in all_colors; invalid colors: {set(guess) - set(self.all_colors)}'
        assert sum(guess_result) == self.num_pegs, 'guess result must sum to num_pegs'
        self.previous_guesses.append((guess, guess_result))

    def get_possible_ground_truths(self):
        """
        Returns the possible ground truths based on the previous guesses.
        """
        previous_guesses = self.previous_guesses
        all_possible_pegs = self.all_possible_pegs
        possible_triplets = self.possible_triplets
        if self.tqdm is not None:
            previous_guesses = self.tqdm(previous_guesses, desc='Step 1/2: Filtering possible ground truths')
        # filter possible ground truths based on previous guesses
        pair_mask = np.full((len(all_possible_pegs), ), True, dtype=bool)
        for previous_guess, guess_result in previous_guesses:
            previous_guess = tuple(tuple((i, c) for i, c in enumerate(previous_guess)))
            pairs = np_information_gain(guess=previous_guess, possible_ground_truths=all_possible_pegs, possible_triplets=possible_triplets, return_pairs=True)
            mask = np.all(pairs == guess_result, axis=1)
            pair_mask &= mask
        possible_ground_truths = tuple(all_possible_pegs[i] for i in range(len(all_possible_pegs)) if pair_mask[i])
        return possible_ground_truths

    def best_next_guess(
        self,
        return_guess_entropy: bool = False,
        verbose: bool = True,
    ):
        """
        Returns the best next guess that would maximize the Shannon entropy of the next guess.
        """
        possible_triplets = self.possible_triplets
        all_possible_pegs = self.all_possible_pegs
        possible_ground_truths = self.get_possible_ground_truths()
        ng = len(possible_ground_truths)  # number of possible ground truths
        if ng == 0:
            print('No possible ground truths found. This should not happen in a real game, please check your inputted guesses.')
            return ng, None
        elif ng == 1:
            answer = [c for i, c in sorted(possible_ground_truths[0], key=lambda x: x[0])]
            if verbose:
                print(f'Solution found! The solution is: {answer}')
            return ng, answer
        if verbose:
            print(f'out of {len(all_possible_pegs)} possible ground truths, only {ng} are still possible.')

        if self.tqdm is not None:
            all_possible_pegs = self.tqdm(all_possible_pegs, desc='Step 2/2: Calculating entropy for each guess')
        guess_entropy = []
        possible_ground_truths_set = set(tuple((i, c) for i, c in guess) for guess in possible_ground_truths)
        for guess in all_possible_pegs:
            entropy = np_information_gain(guess=guess, possible_ground_truths=possible_ground_truths, possible_triplets=possible_triplets)
            is_possible = tuple(guess) in possible_ground_truths_set
            guess_entropy.append((guess, entropy, is_possible))
        guess_entropy = sorted(guess_entropy, key=lambda x: (x[1], x[2]), reverse=True)
        max_entropy_guess = guess_entropy[0]
        if verbose:
            answer = [c for i, c in sorted(max_entropy_guess[0], key=lambda x: x[0])]
            print(f'max entropy guess is: {answer} with entropy {max_entropy_guess[1]:.4f}')
        if return_guess_entropy:
            return ng, max_entropy_guess, guess_entropy
        else:
            return ng, max_entropy_guess




def get_triplets(guess, ground_truth, verbose=False):
    """
    Returns
        1. Number of guesses that match the color and location
        2. Number of guesses that match the color but not the location
        3. Number of guesses that do not match the color or the location
    e.g.
        if guess is ((0, 'Y'), (1, 'R'), (2, 'R'), (3, 'R')) and ground_truth is ((0, 'Y'), (1, 'Y'), (2, 'R'), (3, 'R')), then the triplets are (3, 0, 1)
        if guess is ((0, 'R'), (1, 'Y'), (2, 'Y'), (3, 'Y')) and ground_truth is ((0, 'Y'), (1, 'Y'), (2, 'R'), (3, 'R')), then the triplets are (1, 2, 1)
    """
    color_count = defaultdict(int)
    for _, color in ground_truth:
        color_count[color] += 1
    matching_color_and_location = 0
    matching_color_but_not_location = 0
    not_matching = 0
    done_locs = set()
    for (loc, color) in guess:
        if (loc, color) in ground_truth:
            if verbose:
                print(f'loc {loc} color {color} matched perfectly')
            matching_color_and_location += 1
            color_count[color] -= 1
            done_locs.add(loc)
    for (loc, color) in guess:
        if loc in done_locs:
            continue
        if color_count.get(color, 0) > 0:
            if verbose:
                print(f'loc {loc} color {color} matched but not in the right location')
            matching_color_but_not_location += 1
            color_count[color] -= 1
        else:
            not_matching += 1
    return matching_color_and_location, matching_color_but_not_location, not_matching

def slow_information_gain(guess: set[tuple[int, str]], possible_ground_truths: set[set[tuple[int, str]]], possible_triplets: set[tuple[int, int, int]]):
    # safe but slow solution used as a reference
    counts = {triplet: 0 for triplet in possible_triplets}
    for ground_truth in possible_ground_truths:
        counts[tuple(get_triplets(guess, ground_truth))] += 1
    px = {triplet: count / len(possible_ground_truths) for triplet, count in counts.items()}
    entropy = -sum(px[triplet] * np.log2(px[triplet]) for triplet in possible_triplets if px[triplet] > 0)
    # print(counts)
    return entropy


def np_information_gain(guess: tuple[tuple[int, str]], possible_ground_truths: tuple[set[tuple[int, str]]], possible_triplets: set[tuple[int, int, int]], return_pairs: bool = False):
    # my attempt of a vectorized np solution
    n = len(guess)
    all_colors = set()
    for _, color in guess:
        all_colors.add(color)
    for gt in possible_ground_truths:
        for _, color in gt:
            all_colors.add(color)
    guess_mask = {c: np.full((n, 1), 0, dtype=np.int8) for c in all_colors}
    for loc, color in guess:
        guess_mask[color][loc] = 1
    guess_mask_repeated = {c: np.repeat(guess_mask[c].T, len(possible_ground_truths), axis=0) for c in all_colors}

    color_matrices = {c: np.full((len(possible_ground_truths), n), 0, dtype=np.int8) for c in all_colors}
    for i, gt in enumerate(possible_ground_truths):
        for loc, color in gt:
            color_matrices[color][i, loc] = 1

    pair_1 = sum(color_matrices[c] @ guess_mask[c] for c in all_colors)

    pair_2_diff = {c: guess_mask_repeated[c] - color_matrices[c] for c in all_colors}
    pos_mask = {c: pair_2_diff[c] > 0 for c in all_colors}
    pair_2_extra_guess = {c: pair_2_diff[c].copy() for c in all_colors}
    pair_2_extra_ground = {c: pair_2_diff[c].copy() for c in all_colors}
    pair_2 = {}
    for c in all_colors:
        pair_2_extra_guess[c][~pos_mask[c]] = 0
        pair_2_extra_guess[c] = np.sum(pair_2_extra_guess[c], axis=1)
        pair_2_extra_ground[c][pos_mask[c]] = 0
        pair_2_extra_ground[c] = np.abs(np.sum(pair_2_extra_ground[c], axis=1))
        pair_2[c] = np.minimum(pair_2_extra_guess[c], pair_2_extra_ground[c])

    pair_2 = sum(pair_2[c] for c in all_colors)
    pair_2 = pair_2[:, None]

    pair_3 = n - pair_1 - pair_2

    pair = np.concatenate([pair_1, pair_2, pair_3], axis=1)
    pair_counter = Counter(tuple(t) for t in pair)
    counts = {triplet: pair_counter[triplet] for triplet in possible_triplets}
    px = {triplet: count / len(possible_ground_truths) for triplet, count in counts.items()}
    entropy = -sum(px[triplet] * np.log2(px[triplet]) for triplet in possible_triplets if px[triplet] > 0)
    # print(counts)
    if return_pairs:
        return pair
    else:
        return entropy






def fast_information_gain(guess: set[tuple[int, str]],
                          possible_ground_truths: set[set[tuple[int, str]]],
                          possible_triplets: set[tuple[int, int, int]]):
    # chatgpt fast solution + many modifications by me
    counts = {t: 0 for t in possible_triplets}

    for gt in possible_ground_truths:
        color_count = {}
        for _, c in gt:
            color_count[c] = color_count.get(c, 0) + 1

        H = 0
        for loc, c in guess:
            if (loc, c) in gt:
                H += 1
                color_count[c] -= 1  # safe: gt contributes this occurrence

        color_only = 0
        for loc, c in guess:
            if (loc, c) in gt:
                continue
            remain = color_count.get(c, 0)
            if remain > 0:
                color_only += 1
                color_count[c] = remain - 1

        triplet = (H, color_only, len(guess) - H - color_only)
        counts[triplet] += 1

    px = {triplet: count / len(possible_ground_truths) for triplet, count in counts.items()}
    entropy = -sum(px[triplet] * np.log2(px[triplet]) for triplet in possible_triplets if px[triplet] > 0)
    # print(counts)
    return entropy
