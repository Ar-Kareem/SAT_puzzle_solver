import hashlib

from puzzle_solver.core.utils import Pos, Direction, get_next_pos

# a shape on the 2d board is just a set of positions
Shape = frozenset[Pos]


def polyominoes(N):
    """Generate all polyominoes of size N. Every rotation and reflection is considered different and included in the result.
    Translation is not considered different and is removed from the result (otherwise the result would be infinite).

    Below is the number of unique polyominoes of size N (not including rotations and reflections) and the lenth of the returned result (which includes all rotations and reflections)
    N	name		#shapes		#results
    1	monomino	1			1
    2	domino		1			2
    3	tromino		2			6
    4	tetromino	5			19
    5	pentomino	12			63
    6	hexomino	35			216
    7	heptomino	108			760
    8	octomino	369			2,725
    9	nonomino	1,285		9,910
    10	decomino	4,655		36,446
    11	undecomino	17,073		135,268
    12	dodecomino	63,600		505,861
    Source: https://en.wikipedia.org/wiki/Polyomino

    Args:
        N (int): The size of the polyominoes to generate.

    Returns:
        set[(frozenset[Pos], int)]: A set of all polyominoes of size N (rotated and reflected up to D4 symmetry) along with a unique ID for each polyomino.
    """
    assert N >= 1, 'N cannot be less than 1'
    # need a frozenset because regular sets are not hashable
    shapes: set[Shape] = {frozenset({Pos(0, 0)})}
    for i in range(1, N):
        next_shapes: set[Shape] = set()
        for s in shapes:
            # frontier: all 4-neighbors of existing cells not already in the shape
            frontier = {get_next_pos(pos, direction)
                        for pos in s
                        for direction in Direction
                        if get_next_pos(pos, direction) not in s}
            for cell in frontier:
                t = s | {cell}
                # normalize by translation only: shift so min x,y is (0,0). This removes translational symmetries.
                minx = min(pos.x for pos in t)
                miny = min(pos.y for pos in t)
                t0 = frozenset(Pos(x=pos.x - minx, y=pos.y - miny) for pos in t)
                next_shapes.add(t0)
        shapes = next_shapes
    # shapes is now complete, now classify up to D4 symmetry (rotations/reflections), translations ignored
    mats = (
        ( 1, 0,  0, 1),  # regular
        (-1, 0,  0, 1),  # reflect about x
        ( 1, 0,  0,-1),  # reflect about y
        (-1, 0,  0,-1),  # reflect about x and y
        # trnaspose then all 4 above
        ( 0, 1,  1, 0), ( 0, 1, -1, 0), ( 0,-1,  1, 0), ( 0,-1, -1, 0),
    )
    # compute canonical representative for each shape (lexicographically smallest normalized transform)
    shape_to_canon: dict[Shape, tuple[Pos, ...]] = {}
    for s in shapes:
        reps: list[tuple[Pos, ...]] = []
        for a, b, c, d in mats:
            pts = {Pos(x=a*p.x + b*p.y, y=c*p.x + d*p.y) for p in s}
            minx = min(p.x for p in pts)
            miny = min(p.y for p in pts)
            rep = tuple(sorted(Pos(x=p.x - minx, y=p.y - miny) for p in pts))
            reps.append(rep)
        canon = min(reps)
        shape_to_canon[s] = canon

    canon_set = set(shape_to_canon.values())
    canon_to_id = {canon: i for i, canon in enumerate(sorted(canon_set))}
    result = {(s, canon_to_id[shape_to_canon[s]]) for s in shapes}
    return result