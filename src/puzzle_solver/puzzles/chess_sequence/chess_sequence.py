import json
from dataclasses import dataclass
from typing import Union
from enum import Enum

import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_pos, get_all_pos, get_char, set_char, get_row_pos, get_col_pos, Direction, get_next_pos, in_bounds
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

def to_algebraic_notation(move_sequence: dict[int, tuple[str, Pos, Pos, str]]) -> list[str]:
    move_sequence = sorted(move_sequence.items(), key=lambda x: x[0])
    move_sequence = [x[1] for x in move_sequence]
    return [to_algebraic_notation_single_move(piece_type, from_pos, to_pos, victim_type) for piece_type, from_pos, to_pos, victim_type in move_sequence]


def is_same_row_col(from_pos: Pos, to_pos: Pos) -> bool:
    return from_pos.x == to_pos.x or from_pos.y == to_pos.y

def is_diagonal(from_pos: Pos, to_pos: Pos) -> bool:
    return abs(from_pos.x - to_pos.x) == abs(from_pos.y - to_pos.y)

def is_move_valid(from_pos: Pos, to_pos: Pos, piece_type: PieceType) -> bool:
    if piece_type == PieceType.KING:
        dx = abs(from_pos.x - to_pos.x)
        dy = abs(from_pos.y - to_pos.y)
        return dx <= 1 and dy <= 1
    elif piece_type == PieceType.QUEEN:
        return is_same_row_col(from_pos, to_pos) or is_diagonal(from_pos, to_pos)
    elif piece_type == PieceType.ROOK:
        return is_same_row_col(from_pos, to_pos)
    elif piece_type == PieceType.BISHOP:
        return is_diagonal(from_pos, to_pos)
    elif piece_type == PieceType.KNIGHT:
        dx = abs(from_pos.x - to_pos.x)
        dy = abs(from_pos.y - to_pos.y)
        return (dx == 2 and dy == 1) or (dx == 1 and dy == 2)
    elif piece_type == PieceType.PAWN:  # will always eat because the this is how the puzzle works
        dx = to_pos.x - from_pos.x
        dy = to_pos.y - from_pos.y
        return abs(dx) == 1 and dy == 1


class Board:
    def __init__(self, pieces: list[str]):
        self.pieces: dict[int, tuple[PieceType, Pos]] = {i: parse_algebraic_notation(p) for i, p in enumerate(pieces)}
        self.N = len(self.pieces)  # number of pieces
        self.T = self.N  # (N-1) moves + 1 initial state
        
        self.V = 8  # board size
        self.H = 8  # board size
        self.num_positions = self.V * self.H  # 8x8 board

        self.model = cp_model.CpModel()
        # Input numbers: N is number of piece, T is number of time steps (=N here), B is board size (=64 here):
        # Number of variables 
        # piece_positions: O(NTB)
        # is_dead: O(NT)
        # mover: O(NT)
        # victim: O(NT)
        # dies_this_timestep: O(NT)
        # pos_is_p_star: O(NTB)
        # Total: ~ (2*64)N^2 + 5N^2 = 132N^2

        # (piece_index, time_step, position) -> boolean variable (possible all false if i'm dead)
        self.piece_positions: dict[tuple[int, int, Pos], cp_model.IntVar] = {}
        self.is_dead: dict[tuple[int, int], cp_model.IntVar] = {}  # Am I currently dead

        # (piece_index, time_step) -> boolean variable indicating if the piece [moved/died]
        self.mover: dict[tuple[int, int], cp_model.IntVar] = {}  # did i move this timestep?
        self.victim: dict[tuple[int, int], cp_model.IntVar] = {}  # did i die this timestep?

        self.create_vars()
        self.add_all_constraints()
    
    def create_vars(self):
        for p in range(self.N):
            for t in range(self.T):
                for pos in get_all_pos(self.V, self.H):
                    self.piece_positions[(p, t, pos)] = self.model.NewBoolVar(f'piece_positions[{p},{t},{pos}]')
                self.is_dead[(p, t)] = self.model.NewBoolVar(f'is_dead[{p},{t}]')
        for p in range(self.N):
            for t in range(self.T - 1):  # final state does not have a mover or victim
                self.mover[(p, t)] = self.model.NewIntVar(0, 1, f'mover[{p},{t}]')
                self.victim[(p, t)] = self.model.NewIntVar(0, 1, f'victim[{p},{t}]')

    def add_all_constraints(self):
        self.enforce_initial_state()
        self.enforce_board_state_constraints()
        self.enforce_mover_victim_constraints()

    def enforce_initial_state(self):
        # initial state
        for p, (_, initial_pos) in self.pieces.items():
            self.model.Add(self.piece_positions[(p, 0, initial_pos)] == 1)
            # cant be initially dead
            self.model.Add(self.is_dead[(p, 0)] == 0)
            # all others are blank
            for pos in get_all_pos(self.V, self.H):
                if pos == initial_pos:
                    continue
                self.model.Add(self.piece_positions[(p, 0, pos)] == 0)

    def enforce_board_state_constraints(self):
        # at each timestep and each piece, it can only be at exactly one position or dead
        for p in range(self.N):
            for t in range(self.T):
                pos_vars = [self.piece_positions[(p, t, pos)] for pos in get_all_pos(self.V, self.H)]
                pos_vars.append(self.is_dead[(p, t)])
                self.model.AddExactlyOne(pos_vars)
        # if im dead this timestep then im also dead next timestep
        for p in range(self.N):
            for t in range(self.T - 1):
                self.model.Add(self.is_dead[(p, t + 1)] == 1).OnlyEnforceIf(self.is_dead[(p, t)])
        # every move must be legal chess move
        for p in range(self.N):
            for t in range(self.T - 1):
                for from_pos in get_all_pos(self.V, self.H):
                    for to_pos in get_all_pos(self.V, self.H):
                        if from_pos == to_pos:
                            continue
                        if not is_move_valid(from_pos, to_pos, self.pieces[p][0]):
                            self.model.Add(self.piece_positions[(p, t + 1, to_pos)] == 0).OnlyEnforceIf([self.piece_positions[(p, t, from_pos)]])
        # if mover is i and victim is j then i HAS to be at the position of j at the next timestep
        for p_mover in range(self.N):
            for p_victim in range(self.N):
                if p_mover == p_victim:
                    continue
                for t in range(self.T - 1):
                    for pos in get_all_pos(self.V, self.H):
                        self.model.Add(self.piece_positions[(p_mover, t + 1, pos)] == self.piece_positions[(p_victim, t, pos)]).OnlyEnforceIf([self.mover[(p_mover, t)], self.victim[(p_victim, t)]])

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
                for pos in get_all_pos(self.V, self.H):
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


    def solve_and_print(self, verbose: bool = True, max_solutions: int = None):
        def board_to_solution(board: "Board", solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            pos_assignment: dict[tuple[int, int, Union[Pos, str]], int] = {}
            for t in range(board.T):
                for i in range(board.N):
                    for pos in get_all_pos(board.V, board.H):
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
                from_pos = next(pos for pos in get_all_pos(board.V, board.H) if pos_assignment[(mover_i, t, pos)])
                to_pos = next(pos for pos in get_all_pos(board.V, board.H) if pos_assignment[(mover_i, t + 1, pos)])
                assignment[t] = (board.pieces[mover_i][0].name, from_pos, to_pos, board.pieces[victim_i][0].name)
            # return SingleSolution(assignment=assignment, pos_assignment=pos_assignment, mover=mover, victim=victim)
            return SingleSolution(assignment=assignment)

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
            move_sequence = to_algebraic_notation(single_res.assignment)
            print(move_sequence)
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose, max_solutions=max_solutions)
