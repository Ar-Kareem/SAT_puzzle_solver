from puzzle_solver.core.utils import polyominoes


def test_polyominoes():
    targets = [1, 2, 6, 19, 63, 216, 760, 2725, 9910]#, 36446, 135268, 505861, ]
    for digit in range(1, 10):
        print(f'polyominoes for {digit}:')
        P = polyominoes(digit)
        N = len(P)
        print(f'N: {N}, target: {targets[digit-1]}')
        assert N == targets[digit-1], f'N: {N} != target: {targets[digit-1]}'
