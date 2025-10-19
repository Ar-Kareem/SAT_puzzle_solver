
## Chess Sequence(Puzzle Type #23)

* [**Play online**](https://www.puzzle-chess.com/chess-ranger-11/)

* [**Solver Code**][23]

<details>
  <summary><strong>Rules</strong></summary>

You are given a chess board with $N$ pieces distributed on it. Your aim is to make $N-1$ sequence of moves where each move is a legal chess move and captures another piece.

This means that at the end of the $N-1$ moves, there is only one piece left alive on the board.

A move that does not capture another piece is not allowed.

</details>

**Unsolved puzzle**

<img src="../images/chess_sequence_unsolved.png" alt="Chess sequence unsolved" width="500">

Code to utilize this package and solve the puzzle:

(Note that this puzzle does not typically have a unique solution. Thus, we specify here that we only want the first valid solution that the solver finds.)

```python
from puzzle_solver import chess_sequence_solver as solver
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

<img src="../images/chess_sequence_solved.png" alt="Chess sequence solved" width="500">
