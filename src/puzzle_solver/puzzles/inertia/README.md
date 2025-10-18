# Inertia (Puzzle Type #21)

This is a dedicated solver for Inertia.

This solver is a bit different from the other solvers in this repo because this game does not have a unique solution (you simply move the ball to collect all the gems).

Thus the solver was developed with the additional much harder goal of collecting all the gems with the least number of moves.

It does so using the following high level steps:

1. Model the board as a directed graph where the cells are nodes and legal moves as directed edges with unit cost. Each gem has to a group of edges where traversing any one of them collects that gem.
2. Model step (1) as a [Generalized Traveling Salesman Problem (GTSP)](https://en.wikipedia.org/wiki/Set_TSP_problem), where each gem’s edge group forms a cluster.
3. Apply the [Noon–Bean transformation](https://deepblue.lib.umich.edu/bitstream/handle/2027.42/6834/ban3102.0001.001.pdf?sequence=5) **(Noon & Bean, 1991)** to convert the GTSP from step (2) into an equivalent Asymmetric TSP (ATSP) that can be solved with OR-Tools’ routing solver. (Noon-Bean transformation is mentioned but not described in the [TSP wikipedia page](https://en.wikipedia.org/wiki/Travelling_salesman_problem).)
4. Use a [Vehicle Routing Problem (VRP)](https://en.wikipedia.org/wiki/Vehicle_routing_problem) solver using the [OR-Tools VRP solver](https://developers.google.com/optimization/routing/routing_tasks) to solve the ATSP.

This achieves a final sequence of moves that is empirically always faster than the website's solution.

Below are the details of how to utilize the solver.

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/inertia.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/inertia.html#inertia)

You are a small green ball sitting in a grid full of obstacles. Your aim is to collect all the gems without running into any mines.

You can move the ball in any orthogonal or diagonal direction. Once the ball starts moving, it will continue until something stops it. A wall directly in its path will stop it (but if it is moving diagonally, it will move through a diagonal gap between two other walls without stopping). Also, some of the squares are ‘stops’; when the ball moves on to a stop, it will stop moving no matter what direction it was going in. Gems do not stop the ball; it picks them up and keeps on going.

Running into a mine is fatal. Even if you picked up the last gem in the same move which then hit a mine, the game will count you as dead rather than victorious. 

**Unsolved puzzle**

<img src="../images/inertia_unsolved.png" alt="Inertia unsolved" width="500">

Code to utilize this package and solve the puzzle:

(Note: there is a script that parses a screenshot of the board and outputs the below array that the solver uses. The script uses classical computer vision techniques and is called `parse_map.py`)
```python
import numpy as np
from . import solver
bor = np.array([
  ["O", "O", "M", " ", "G", "O", "G", "O", " ", " ", "M", " ", " ", "O", "G", "G", "W", "O", "O", "O"],
  ["O", " ", "W", " ", "W", "O", "G", "M", " ", " ", " ", "G", "M", "O", "W", "G", " ", "M", "M", "O"],
  ["O", "M", "O", "O", " ", "M", " ", "W", "W", "M", "G", "W", " ", " ", "G", " ", "W", "G", "O", "G"],
  ["O", " ", "O", "M", "G", "O", "W", "G", "M", "O", " ", " ", "G", "G", "G", " ", "M", "W", "M", "O"],
  ["M", "M", "O", "G", " ", "W", " ", " ", "O", "G", " ", "M", "M", " ", "W", "W", " ", "W", "W", "O"],
  ["G", " ", "G", "W", "M", "W", "W", " ", "G", "G", "W", "M", "G", "G", " ", "G", "O", "O", "M", "M"],
  ["M", " ", "M", " ", "W", "W", "M", "M", "M", "O", "M", "G", "O", "M", "M", "W", "B", "O", "W", "M"],
  ["G", "G", " ", "W", "M", "M", "W", "O", "W", "G", "W", "O", "O", "M", " ", "W", "W", "G", "G", "M"],
  [" ", "M", "M", " ", " ", " ", "G", "G", "M", "O", "M", "O", "M", "G", "W", "M", "W", " ", "O", " "],
  ["G", " ", "M", " ", " ", " ", "W", "O", "W", "W", "M", "M", "G", "W", " ", " ", "W", "M", "G", "W"],
  ["G", "O", "M", "M", "G", "M", "W", "O", "O", "G", "W", "M", "M", "G", "G", " ", "O", " ", "W", "W"],
  ["G", "G", "W", "G", "M", " ", "G", "W", "W", " ", "G", " ", "O", "W", "G", "G", "O", " ", "M", "M"],
  ["W", "M", "O", " ", "W", "O", "O", "M", "M", "O", "G", "W", " ", "G", "O", "G", "G", "O", "O", "W"],
  ["W", "W", "W", " ", "W", "O", "W", "M", "O", "M", "G", "O", "O", " ", " ", "W", "W", "G", "W", "W"],
  ["O", "W", "O", "M", "O", "G", " ", "O", "O", "M", "O", " ", "M", "M", "O", "G", "W", "G", "M", " "],
  ["M", "G", "O", "G", "O", "G", "O", "G", " ", "W", "W", "G", "O", " ", "W", "M", "G", " ", "W", " "]
])
start_pos, edges, edges_to_direction, gems_to_edges = solver.parse_nodes_and_edges(bor)
optimal_walk = solver.solve_optimal_walk(start_pos, edges, gems_to_edges)
moves = solver.get_moves_from_walk(optimal_walk, edges_to_direction, verbose=True)
```
**Script Output**

Note that the output is the sequence of moves to collect all the gems. This particular solution is 106 moves, which is 15 moves better than the website's solution.
```
number of moves 106
↗ ↖ ↖ ↙ ↙ ↖ ↖ ↙ → ↘ 
↙ → ↖ → ↙ ↓ → ↘ ↗ ↓
↘ → ↘ ↓ ↗ ↓ ↑ → ↗ ↖
↑ ↗ ↑ ↗ → ↓ ← ↙ ↖ ↗
↓ ↙ ↙ ↑ ← ↘ ↙ ↓ → ↘
↘ ↙ ↖ ↙ ↗ ↘ ↗ ↘ ↑ ↘
↖ ↑ ↗ → → ↘ → ↘ ↗ ↑
← ↑ ↖ ↖ ↗ → ↘ ↓ ↖ ←
↖ ↓ ← ↓ ↓ ↑ ↖ → ↗ ↗
↘ ↘ ↙ ↘ ↓ ↗ ↖ ↘ ↙ ←
↘ ↖ ↗ ↑ ↗ →
Time taken: 13.92 seconds
```

**Solved puzzle**

This picture won't mean much as the game is about the sequence of moves not the final frame as shown here.

<img src="../images/inertia_solved.png" alt="Inertia solved" width="500">
