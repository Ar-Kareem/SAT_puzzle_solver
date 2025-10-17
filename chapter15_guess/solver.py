from collections import defaultdict


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
    counts = {triplet: 0 for triplet in possible_triplets}
    for ground_truth in possible_ground_truths:
        counts[tuple(get_triplets(guess, ground_truth))] += 1
    return counts
