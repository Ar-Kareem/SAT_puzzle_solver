import json
from dataclasses import dataclass
from typing import Union
from enum import Enum

from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_pos
from puzzle_solver.core.utils_ortools import and_constraint, generic_solve_all, or_constraint


class PieceType(Enum):
    KING   = 1
    QUEEN  = 2
    ROOK   = 3
    BISHOP = 4
    KNIGHT = 5
    PAWN   = 6

@dataclass(frozen=True)
class SingleSolution:
    assignment: dict[int, tuple[str, Pos, Pos, str]]  # every time step a single piece moves from one position to another and eats another piece
    position_occupied: dict[Pos, int]
    # pos_assignment: dict[tuple[int, int, Union[Pos, str]], int]
    # mover: dict[int, tuple[int, PieceType]]
    # victim: dict[int, tuple[int, PieceType]]

    def get_hashable_solution(self) -> str:
        # only hash assignment
        result = []
        for _, (_, from_pos, to_pos, _) in sorted(self.assignment.items()):
            result.append((from_pos.x, from_pos.y, to_pos.x, to_pos.y))
        # order doesnt matter for uniqueness
        result = sorted(result)
        return json.dumps(result)


def parse_algebraic_notation(algebraic: str) -> tuple[PieceType, Pos]:
    assert isinstance(algebraic, str), f'algebraic notation must be a string, got {type(algebraic)}'
    assert len(algebraic) == 3, 'algebraic notation must be 3 characters'
    p = {'K': PieceType.KING, 'Q': PieceType.QUEEN, 'R': PieceType.ROOK, 'B': PieceType.BISHOP, 'N': PieceType.KNIGHT, 'P': PieceType.PAWN}
    assert algebraic[0] in p, 'invalid piece type'
    assert algebraic[1] in 'abcdefgh', f'invalid file: {algebraic[1]}'
    assert algebraic[2] in '12345678', f'invalid rank: {algebraic[2]}'
    piece_type = p[algebraic[0]]
    file, rank = algebraic[1:]
    file = ord(file) - ord('a')
    rank = int(rank) - 1
    pos = get_pos(x=file, y=rank)
    return (piece_type, pos)


def to_algebraic_notation_single_move(piece_type: str, from_pos: Pos, to_pos: Pos, victim_type: str) -> str:
    letter = {PieceType.KING.name: 'K', PieceType.QUEEN.name: 'Q', PieceType.ROOK.name: 'R', PieceType.BISHOP.name: 'B', PieceType.KNIGHT.name: 'N', PieceType.PAWN.name: 'P'}
    from_file_letter = chr(from_pos.x + ord('a'))
    from_rank_letter = str(from_pos.y + 1)
    to_file_letter = chr(to_pos.x + ord('a'))
    to_rank_letter = str(to_pos.y + 1)
    return f'{letter[piece_type]}{from_file_letter}{from_rank_letter}->{letter[victim_type]}{to_file_letter}{to_rank_letter}'


def to_algebraic_notation(single_solution: SingleSolution) -> list[str]:
    move_sequence = single_solution.assignment
    move_sequence = sorted(move_sequence.items(), key=lambda x: x[0])
    move_sequence = [x[1] for x in move_sequence]
    return [to_algebraic_notation_single_move(piece_type, from_pos, to_pos, victim_type) for piece_type, from_pos, to_pos, victim_type in move_sequence]


def is_same_row_col(from_pos: Pos, to_pos: Pos) -> bool:
    return from_pos.x == to_pos.x or from_pos.y == to_pos.y


def is_diagonal(from_pos: Pos, to_pos: Pos) -> bool:
    return abs(from_pos.x - to_pos.x) == abs(from_pos.y - to_pos.y)


def squares_between_rook(from_pos: Pos, to_pos: Pos) -> list[Pos]:
    if not is_same_row_col(from_pos, to_pos):
        return []
    if abs(from_pos.x - to_pos.x) <= 1 and abs(from_pos.y - to_pos.y) <= 1:  # within 2x2 thus no intermediate squares
        return []
    squares: list[Pos] = []
    if from_pos.x == to_pos.x:
        x = from_pos.x
        step = 1 if to_pos.y > from_pos.y else -1
        for y in range(from_pos.y + step, to_pos.y, step):
            squares.append(get_pos(x=x, y=y))
    else:
        y = from_pos.y
        step = 1 if to_pos.x > from_pos.x else -1
        for x in range(from_pos.x + step, to_pos.x, step):
            squares.append(get_pos(x=x, y=y))
    return squares


def squares_between_bishop(from_pos: Pos, to_pos: Pos) -> list[Pos]:
    if not is_diagonal(from_pos, to_pos):
        return []
    if abs(from_pos.x - to_pos.x) <= 1 and abs(from_pos.y - to_pos.y) <= 1:  # within 2x2 thus no intermediate squares
        return []
    squares: list[Pos] = []
    step_x = 1 if to_pos.x > from_pos.x else -1
    step_y = 1 if to_pos.y > from_pos.y else -1
    x = from_pos.x + step_x
    y = from_pos.y + step_y
    while x != to_pos.x and y != to_pos.y:
        squares.append(get_pos(x=x, y=y))
        x += step_x
        y += step_y
    return squares



def is_move_valid(from_pos: Pos, to_pos: Pos, piece_type: PieceType, color=None) -> tuple[bool, list[Pos]]:
    """Returns: (is_valid, list of positions that must be empty for the move to be valid)
    For Kings, Pawns, and Knights, no positions must be empty for the move to be valid.
    A Queen is equivalent to a Rook and a Bishop.
    A Rook needs all positions directly between the from and to position to be empty for the move to be valid.
    Similarly, a Bishop needs all positions diagonally between the from and to position to be empty for the move to be valid.

    Args:
        from_pos (Pos): from position
        to_pos (Pos): to position
        piece_type (PieceType): piece type
        color (str, optional): color of the piece (default: None, all pieces are assumed white)

    Returns:
        tuple[bool, list[Pos]]: (is_valid, list of positions that must be empty for the move to be valid)
    """
    if piece_type == PieceType.KING:
        dx = abs(from_pos.x - to_pos.x)
        dy = abs(from_pos.y - to_pos.y)
        is_valid = dx <= 1 and dy <= 1
        return is_valid, []
    elif piece_type == PieceType.QUEEN:  # rook + bishop
        rook_valid = is_move_valid(from_pos, to_pos, PieceType.ROOK, color)
        if rook_valid[0]:
            return rook_valid
        return is_move_valid(from_pos, to_pos, PieceType.BISHOP, color)
    elif piece_type == PieceType.ROOK:
        return is_same_row_col(from_pos, to_pos), squares_between_rook(from_pos, to_pos)
    elif piece_type == PieceType.BISHOP:
        return is_diagonal(from_pos, to_pos), squares_between_bishop(from_pos, to_pos)
    elif piece_type == PieceType.KNIGHT:
        dx = abs(from_pos.x - to_pos.x)
        dy = abs(from_pos.y - to_pos.y)
        is_valid = (dx == 2 and dy == 1) or (dx == 1 and dy == 2)
        return is_valid, []
    elif piece_type == PieceType.PAWN:  # will always eat because the this is how the puzzle works
        dx = to_pos.x - from_pos.x
        dy = to_pos.y - from_pos.y
        is_valid = abs(dx) == 1 and dy == (1 if color != 'B' else -1)
        return is_valid, []


class Board:
    def __init__(self, pieces: list[str], colors: list[str] = None, max_moves_per_piece: int = None, last_piece_alive: Union[PieceType, str] = None):
        """
        Args:
            pieces: list of algebraic notation of the pieces
            colors: list of colors of the pieces (default: None, all pieces are assumed white (i.e. all pieces are the same except for pawns move only up))
            max_moves_per_piece: maximum number of moves per piece (default: None, no limit)
            last_piece_alive: force the last piece alive to be of this type (default: None, any piece can be last man standing)
        """
        self.pieces: dict[int, tuple[PieceType, Pos]] = {i: parse_algebraic_notation(p) for i, p in enumerate(pieces)}
        assert colors is None or (len(colors) == len(self.pieces) and all(c in ['B', 'W'] for c in colors)), f'if provided, colors must be a list of length {len(self.pieces)} with elements B or W, got {colors}'
        self.colors = colors
        self.N = len(self.pieces)  # number of pieces
        self.T = self.N  # (N-1) moves + 1 initial state
        self.max_moves_per_piece = max_moves_per_piece
        self.last_piece_alive = last_piece_alive
        self.V = 8  # board size
        self.H = 8  # board size
        # the puzzle rules mean the only legal positions are the starting positions of the pieces
        self.all_legal_positions: set[Pos] = {pos for _, pos in self.pieces.values()}
        assert len(self.all_legal_positions) == len(self.pieces), f'positions are not unique'

        self.model = cp_model.CpModel()
        # Input numbers: N is number of piece, T is number of time steps (=N here), B is board size (=N here because the only legal positions are the starting positions of the pieces):
        # Number of variables 
        # piece_positions: O(NTB)
        # is_dead: O(NT)
        # mover: O(NT)
        # victim: O(NT)
        # position_occupied: O(TB)
        # dies_this_timestep: O(NT)
        # pos_is_p_star: O(NTB)
        # Total: ~ (2*N)N^2 + 6N^2 = 2N^3 + 6N^2

        # (piece_index, time_step, position) -> boolean variable (possible all false if i'm dead)
        self.piece_positions: dict[tuple[int, int, Pos], cp_model.IntVar] = {}
        self.is_dead: dict[tuple[int, int], cp_model.IntVar] = {}  # Am I currently dead

        # (piece_index, time_step) -> boolean variable indicating if the piece [moved/died]
        self.mover: dict[tuple[int, int], cp_model.IntVar] = {}  # did i move this timestep?
        self.victim: dict[tuple[int, int], cp_model.IntVar] = {}  # did i die this timestep?

        # (time_step, position) -> boolean variable indicating if the position is occupied by any piece at this timestep
        self.position_occupied: dict[tuple[int, Pos], cp_model.IntVar] = {}

        self.create_vars()
        self.add_all_constraints()

    def can_move(self, p: int, t: int) -> bool:
        c = self.colors[p]
        return (c == 'W' and t % 2 == 0) or (c == 'B' and t % 2 == 1)

    def can_be_victim(self, p: int, t: int) -> bool:
        c = self.colors[p]
        return (c == 'W' and t % 2 == 1) or (c == 'B' and t % 2 == 0)

    def create_vars(self):
        for p in range(self.N):
            for t in range(self.T):
                for pos in self.all_legal_positions:
                    self.piece_positions[(p, t, pos)] = self.model.NewBoolVar(f'piece_positions[{p},{t},{pos}]')
                self.is_dead[(p, t)] = self.model.NewBoolVar(f'is_dead[{p},{t}]')
        for p in range(self.N):
            for t in range(self.T - 1):  # final state does not have a mover or victim
                self.mover[(p, t)] = self.model.NewIntVar(0, 1, f'mover[{p},{t}]')
                self.victim[(p, t)] = self.model.NewIntVar(0, 1, f'victim[{p},{t}]')

        for t in range(self.T):
            for pos in self.all_legal_positions:
                self.position_occupied[(t, pos)] = self.model.NewBoolVar(f'position_occupied[{t},{pos}]')

    def add_all_constraints(self):
        self.enforce_initial_state()
        self.enforce_board_state_constraints()
        self.enforce_mover_victim_constraints()
        self.enforce_position_occupied_constraints()

    def enforce_initial_state(self):
        # initial state
        for p, (_, initial_pos) in self.pieces.items():
            self.model.Add(self.piece_positions[(p, 0, initial_pos)] == 1)
            # cant be initially dead
            self.model.Add(self.is_dead[(p, 0)] == 0)
            # all others are blank
            for pos in self.all_legal_positions:
                if pos == initial_pos:
                    continue
                self.model.Add(self.piece_positions[(p, 0, pos)] == 0)

    def enforce_board_state_constraints(self):
        # at each timestep and each piece, it can only be at exactly one position or dead
        for p in range(self.N):
            for t in range(self.T):
                pos_vars = [self.piece_positions[(p, t, pos)] for pos in self.all_legal_positions]
                pos_vars.append(self.is_dead[(p, t)])
                self.model.AddExactlyOne(pos_vars)
        # if im dead this timestep then im also dead next timestep
        for p in range(self.N):
            for t in range(self.T - 1):
                self.model.Add(self.is_dead[(p, t + 1)] == 1).OnlyEnforceIf(self.is_dead[(p, t)])
        # every move must be legal chess move
        for p in range(self.N):
            color = self.colors[p] if self.colors is not None else None
            for t in range(self.T - 1):
                for from_pos in self.all_legal_positions:
                    for to_pos in self.all_legal_positions:
                        if from_pos == to_pos:
                            continue
                        is_valid, need_to_be_empty = is_move_valid(from_pos, to_pos, self.pieces[p][0], color=color)
                        # remove non legal moves
                        need_to_be_empty = set(need_to_be_empty) & self.all_legal_positions
                        if not is_valid:
                            self.model.Add(self.piece_positions[(p, t + 1, to_pos)] == 0).OnlyEnforceIf([self.piece_positions[(p, t, from_pos)]])
                        elif len(need_to_be_empty) > 0:
                            occupied_between = self.model.NewBoolVar(f'occupied_between[{from_pos},{to_pos},{t},{p}]')
                            or_constraint(self.model, occupied_between, [self.position_occupied[(t, pos)] for pos in need_to_be_empty])
                            self.model.Add(self.piece_positions[(p, t + 1, to_pos)] == 0).OnlyEnforceIf([self.piece_positions[(p, t, from_pos)], occupied_between])

        # if mover is i and victim is j then i HAS to be at the position of j at the next timestep
        for p_mover in range(self.N):
            for p_victim in range(self.N):
                if p_mover == p_victim:
                    continue
                for t in range(self.T - 1):
                    for pos in self.all_legal_positions:
                        self.model.Add(self.piece_positions[(p_mover, t + 1, pos)] == self.piece_positions[(p_victim, t, pos)]).OnlyEnforceIf([self.mover[(p_mover, t)], self.victim[(p_victim, t)]])

        # optional parameter to force last piece alive
        if self.last_piece_alive is not None:
            target_ps = [p for p in range(self.N) if self.pieces[p][0] == self.last_piece_alive]
            assert len(target_ps) == 1, f'multiple pieces of type {self.last_piece_alive} found'
            target_p = target_ps[0]
            # target piece is force to be last man standing
            self.model.Add(self.is_dead[(target_p, self.T - 1)] == 0)
            for p in range(self.N):
                if p == target_p:
                    continue
                self.model.Add(self.is_dead[(p, self.T - 1)] == 1)

        if self.colors is not None:
            # t=0 and even timesteps are white, odd timesteps are black
            for p in range(self.N):
                for t in range(self.T - 1):
                    if not self.can_move(p, t):
                        self.model.Add(self.mover[(p, t)] == 0)
            # t=0 and even timesteps only black victims, odd timesteps only white victims
            for p in range(self.N):
                for t in range(self.T - 1):
                    if not self.can_be_victim(p, t):
                        self.model.Add(self.victim[(p, t)] == 0)

    def enforce_mover_victim_constraints(self):
        for p in range(self.N):
            for t in range(self.T - 1):
                # if i'm dead at time step t then I did not move nor victimized
                self.model.Add(self.mover[(p, t)] == 0).OnlyEnforceIf(self.is_dead[(p, t)])
                self.model.Add(self.victim[(p, t)] == 0).OnlyEnforceIf(self.is_dead[(p, t)])
                # if I was the mover or victim at time step t then I was not dead
                self.model.Add(self.is_dead[(p, t)] == 0).OnlyEnforceIf(self.mover[(p, t)])
                self.model.Add(self.is_dead[(p, t)] == 0).OnlyEnforceIf(self.victim[(p, t)])
                # a victim cannot be the mover and vice versa
                self.model.Add(self.mover[(p, t)] == 0).OnlyEnforceIf(self.victim[(p, t)])
                self.model.Add(self.victim[(p, t)] == 0).OnlyEnforceIf(self.mover[(p, t)])

                # if im dead next timestep and i was alive this timestep then im the victim
                # cant rely on victim var here because the goal it to constrain it
                dies_this_timestep = self.model.NewBoolVar(f'dies_this_timestep[{p},{t}]')
                and_constraint(self.model, dies_this_timestep, [self.is_dead[(p, t + 1)], self.is_dead[(p, t)].Not()])
                self.model.Add(self.victim[(p, t)] == dies_this_timestep)

                # if next timestep im somewhere else then i was the mover
                # i.e. there exists a position p* s.t. (piece_positions[p, t + 1, p*] AND NOT piece_positions[p, t, p*])
                pos_is_p_star = []
                for pos in self.all_legal_positions:
                    v = self.model.NewBoolVar(f'pos_is_p_star[{p},{t},{pos}]')
                    self.model.Add(v == 1).OnlyEnforceIf([self.piece_positions[(p, t + 1, pos)], self.piece_positions[(p, t, pos)].Not()])
                    self.model.Add(v == 0).OnlyEnforceIf([self.piece_positions[(p, t + 1, pos)].Not()])
                    self.model.Add(v == 0).OnlyEnforceIf([self.piece_positions[(p, t, pos)]])
                    pos_is_p_star.append(v)
                or_constraint(self.model, self.mover[(p, t)], pos_is_p_star)

        # at each timestep only one piece can be the mover
        for t in range(self.T - 1):
            self.model.AddExactlyOne([self.mover[(p, t)] for p in range(self.N)])
        # at each timestep only one piece can be victimized
        for t in range(self.T - 1):
            self.model.AddExactlyOne([self.victim[(p, t)] for p in range(self.N)])

        # optional parameter to force 
        if self.max_moves_per_piece is not None:
            for p in range(self.N):
                self.model.Add(sum([self.mover[(p, t)] for t in range(self.T - 1)]) <= self.max_moves_per_piece)

    def enforce_position_occupied_constraints(self):
        for t in range(self.T):
            for pos in self.all_legal_positions:
                self.model.Add(self.position_occupied[(t, pos)] == sum([self.piece_positions[(p, t, pos)] for p in range(self.N)]))


    def solve_and_print(self, verbose: bool = True, max_solutions: int = None):
        def board_to_solution(board: "Board", solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            pos_assignment: dict[tuple[int, int, Union[Pos, str]], int] = {}
            for t in range(board.T):
                for i in range(board.N):
                    for pos in board.all_legal_positions:
                        pos_assignment[(i, t, pos)] = solver.Value(board.piece_positions[(i, t, pos)])
                    pos_assignment[(i, t, 'DEAD')] = solver.Value(board.is_dead[(i, t)])
            mover = {}
            for t in range(board.T - 1):
                for i in range(board.N):
                    if solver.Value(board.mover[(i, t)]):
                        mover[t] = (i, board.pieces[i][0].name)
            victim = {}
            for t in range(board.T - 1):
                for i in range(board.N):
                    if solver.Value(board.victim[(i, t)]):
                        victim[t] = (i, board.pieces[i][0].name)

            assignment: dict[int, tuple[int, Pos, Pos]] = {}  # final result
            for t in range(board.T - 1):
                mover_i = mover[t][0]
                victim_i = victim[t][0]
                from_pos = next(pos for pos in board.all_legal_positions if pos_assignment[(mover_i, t, pos)])
                to_pos = next(pos for pos in board.all_legal_positions if pos_assignment[(mover_i, t + 1, pos)])
                assignment[t] = (board.pieces[mover_i][0].name, from_pos, to_pos, board.pieces[victim_i][0].name)
            # return SingleSolution(assignment=assignment, pos_assignment=pos_assignment, mover=mover, victim=victim)
            position_occupied = {(t, pos): int(solver.Value(board.position_occupied[(t, pos)])) for t in range(board.T) for pos in board.all_legal_positions}
            return SingleSolution(assignment=assignment, position_occupied=position_occupied)

        def callback(single_res: SingleSolution):
            print("Solution found")
            # pieces = sorted(set(i for (i, _, _) in single_res.assignment.keys()))
            # for piece in pieces:
            #     print(f"Piece {piece} type: {single_res.piece_types[piece]}")
            #     # at each timestep a piece can only be in one position
            #     t_to_pos = {t: pos for (i, t, pos), v in single_res.assignment.items() if i == piece and v == 1}
            #     print(t_to_pos)
            # print('victims:', single_res.victim)
            # print('movers:', single_res.mover)
            # print()
            # for t in range(self.T):
            #     print('at timestep', t, 'the following positions are occupied', [pos for pos in self.all_legal_positions if single_res.position_occupied[(t, pos)] == 1])
            move_sequence = to_algebraic_notation(single_res)
            print(move_sequence)
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose, max_solutions=max_solutions)
