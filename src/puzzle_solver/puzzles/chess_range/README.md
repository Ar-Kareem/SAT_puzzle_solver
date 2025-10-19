
# Chess Range (Puzzle Type #23)

These are three dedicated solvers for different types of chess puzzles (all use the same solver under the hood)

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single input board has multiple possible solutions.

(The solver under the hood mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Play online**](https://www.puzzle-chess.com/chess-ranger-11/)

You are given a chess board with $N$ pieces distributed on it. Your aim is to make $N-1$ range of moves where each move is a legal chess move and captures another piece.

- Pieces move as standard chess pieces.
- You can perform only capture moves. A move that does not capture another piece is not allowed.
- You are allowed to capture the king.
- The goal is to end up with one single piece on the board. 


**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/chess_range_unsolved.png" alt="Chess range unsolved" width="500">

Code to utilize this package and solve the puzzle:

(Note that this puzzle does not typically have a unique solution. Thus, we specify here that we only want the first valid solution that the solver finds.)

```python
from puzzle_solver import chess_range_solver as solver
# algebraic notation
board = ['Qe7', 'Nc6', 'Kb6', 'Pb5', 'Nf5', 'Pg4', 'Rb3', 'Bc3', 'Pd3', 'Pc2', 'Rg2']
binst = solver.Board(board)
solutions = binst.solve_and_print(max_solutions=1)
```
**Script Output**

The output is in the form of "pos -> pos" where "pos" is the algebraic notation of the position.

```python
Solution found
['Rg2->Pc2', 'Rc2->Bc3', 'Rc3->Pd3', 'Kb6->Pb5', 'Pg4->Nf5', 'Rd3->Rb3', 'Rb3->Kb5', 'Nc6->Qe7', 'Ne7->Pf5', 'Rb5->Nf5']
Solutions found: 1
status: FEASIBLE
Time taken: 6.27 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/chess_range_solved.png" alt="Chess range solved" width="500">

# Chess Solo (Puzzle Type #24)

* [**Play online**](https://www.puzzle-chess.com/solo-chess-11/)

You are given a chess board with $N$ pieces distributed on it. Your aim is to make $N-1$ range of moves where each move is a legal chess move and captures another piece and end up with the king as the only piece on the board. You are not allowed to move a piece more than twice.

- Pieces move as standard chess pieces.
- You can perform only capture moves. A move that does not capture another piece is not allowed.
- You can move a piece only twice.
- You are NOT allowed to capture the king.
- The goal is to end up with one single piece (the king) on the board. 

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/chess_solo_unsolved.png" alt="Chess solo unsolved" width="500">

Code to utilize this package and solve the puzzle:

(Note that this puzzle does not typically have a unique solution. Thus, we specify here that we only want the first valid solution that the solver finds.)

```python
# algebraic notation
board = ['Kc6', 'Rc5', 'Rc4', 'Pb3', 'Bd3', 'Pd2', 'Pe3', 'Nf2', 'Ng2', 'Qg3', 'Pg6']
binst = solver.Board(board)
solutions = binst.solve_and_print(max_solutions=1)
```
**Script Output**

The output is in the form of "pos -> pos" where "pos" is the algebraic notation of the position.

```python
Solution found
['Pd2->Pe3', 'Pb3->Rc4', 'Ng2->Pe3', 'Qg3->Pg6', 'Qg6->Bd3', 'Nf2->Qd3', 'Nd3->Rc5', 'Ne3->Pc4', 'Kc6->Nc5', 'Kc5->Nc4']
Solutions found: 1
status: FEASIBLE
Time taken: 4.33 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/chess_solo_solved.png" alt="Chess solo solved" width="500">

# Chess Melee (Puzzle Type #25)

* [**Play online**](https://www.puzzle-chess.com/chess-melee-13/)

You are given a chess board with $N$ pieces distributed on it (equal white and black pieces, one more black if $N$ is odd). Your aim is to make $N-1$ sequence of moves where each move is a legal chess move and captures another piece of the opposite color and end up with a single piece on the board. White starts and colors alternate as usual.

- Pieces move as standard chess pieces.
- White moves first.
- You can perform only capture moves. A move that does not capture another piece of the opposite color is not allowed.
- The goal is to end up with one single piece on the board. 

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/chess_melee_unsolved.png" alt="Chess melee unsolved" width="500">

Code to utilize this package and solve the puzzle:

(Note that this puzzle does not typically have a unique solution. Thus, we specify here that we only want the first valid solution that the solver finds.)

```python
# algebraic notation
board = ['Pb7', 'Nc7', 'Bc6', 'Ne6', 'Pb5', 'Rc4', 'Qb3', 'Rf7', 'Rb6', 'Pe5', 'Nc3', 'Pd3', 'Nf3']
colors = ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'W', 'W', 'W', 'W', 'W', 'W']
binst = solver.Board(board, colors)
solutions = binst.solve_and_print()
```
**Script Output**

The output is in the form of "pos -> pos" where "pos" is the algebraic notation of the position.

```python
Solution found
['Rf7->Nc7', 'Ne6->Rc7', 'Pd3->Rc4', 'Qb3->Nc3', 'Pc4->Pb5', 'Qc3->Pe5', 'Nf3->Qe5', 'Nc7->Pb5', 'Ne5->Bc6', 'Pb7->Nc6', 'Rb6->Nb5', 'Pc6->Rb5']
Solutions found: 1
status: OPTIMAL
Time taken: 6.24 seconds
```

**Solved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/chess_melee_solved.png" alt="Chess melee solved" width="500">
