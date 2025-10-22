import numpy as np

from puzzle_solver import galaxies_solver as solver
from puzzle_solver.core.utils import get_pos


def test_ground():
    # 15 x 15 unreasonable
    # https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/galaxies.html#15x15:eofodowmumgzzdkopzlpzkzaezrhefoezejvdtxrzmpgozzemxjdcigcqzrk
    galaxies = np.array([
        ['  ', '  ', '00', '  ', '  ', '01', '01', '02', '02', '03', '03', '  ', '04', '04', '  '],
        ['05', '05', '  ', '  ', '06', '01', '01', '02', '02', '  ', '  ', '  ', '07', '  ', '  '],
        ['08', '  ', '  ', '  ', '06', '  ', '09', '09', '  ', '  ', '10', '  ', '  ', '  ', '  '],
        ['  ', '  ', '  ', '  ', '  ', '  ', '11', '11', '12', '  ', '  ', '  ', '  ', '13', '13'],
        ['14', '  ', '  ', '  ', '15', '  ', '11', '11', '  ', '  ', '  ', '  ', '16', '  ', '  '],
        ['  ', '17', '  ', '  ', '15', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '16', '  ', '18'],
        ['  ', '17', '19', '  ', '  ', '  ', '  ', '  ', '  ', '20', '  ', '  ', '  ', '21', '18'],
        ['  ', '22', '  ', '  ', '23', '  ', '  ', '  ', '  ', '20', '  ', '24', '24', '21', '25'],
        ['26', '27', '27', '28', '28', '29', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '30', '30'],
        ['  ', '27', '27', '28', '28', '31', '31', '  ', '  ', '  ', '  ', '32', '  ', '30', '30'],
        ['  ', '  ', '  ', '33', '33', '31', '31', '34', '  ', '  ', '35', '  ', '  ', '  ', '  '],
        ['36', '  ', '  ', '33', '33', '  ', '  ', '34', '  ', '  ', '  ', '  ', '  ', '37', '  '],
        ['  ', '  ', '38', '38', '  ', '39', '  ', '40', '40', '41', '41', '42', '  ', '37', '  '],
        ['43', '44', '38', '38', '45', '45', '46', '40', '40', '41', '41', '42', '  ', '  ', '  '],
        ['43', '  ', '  ', '  ', '  ', '  ', '  ', '47', '  ', '  ', '  ', '  ', '48', '48', '  ']
    ])
    binst = solver.Board(galaxies=galaxies)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'



def test_easy():
    # 5x5 example
    # https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/galaxies.html#5x5:cfjglmlcg
    galaxies = [
        (get_pos(x=1, y=0),),
        (get_pos(x=4, y=0),),
        (get_pos(x=0, y=1),),
        (get_pos(x=3, y=1), get_pos(x=4, y=1)),
        (get_pos(x=0, y=2), get_pos(x=1, y=2)),
        (get_pos(x=2, y=2), get_pos(x=3, y=2), get_pos(x=2, y=3), get_pos(x=3, y=3)),
        (get_pos(x=1, y=3), get_pos(x=1, y=4)),
        (get_pos(x=4, y=3),),
        (get_pos(x=0, y=4),),
    ]
    binst = solver.Board(V=5, H=5, galaxies=galaxies)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'



def test_dummy():
    # 3x3 toy example
    # https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/galaxies.html#3x3:acn
    galaxies = [
        (get_pos(x=0, y=0),),
        (get_pos(x=1, y=0), get_pos(x=2, y=0)),
        (get_pos(x=1, y=1), get_pos(x=1, y=2)),
    ]
    binst = solver.Board(V=3, H=3, galaxies=galaxies)
    solutions = binst.solve_and_print()
    assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
    ground = np.array([
        [0, 1, 1],
        [2, 2, 2],
        [2, 2, 2],
    ])
    ground_assignment = {get_pos(x=x, y=y): ground[y][x] for x in range(ground.shape[1]) for y in range(ground.shape[0])}
    solution = solutions[0].assignment
    assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
    for pos in solution.keys():
        assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'


if __name__ == '__main__':
    test_dummy()
    test_easy()
    test_ground()
