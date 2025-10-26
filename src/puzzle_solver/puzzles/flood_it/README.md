# Flood It (Puzzle Type #54)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/flood.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/flood.html#flood)

The game is a combinatorial puzzle played on a colored N by N grid where the goal is to make the entire grid a single color using the minimum number of moves.

A move consists of picking a new color, which then floods the connected component of the player's current area that has that chosen color.

The player's current area is the top-leftmost corner of the grid along with any similarly colored orthogonal cells connected to the current area.

This game has a lot of interesting mathematical properties related to Graph Theory (for example many details are referenced in this [2022 Graph Theory paper](https://arxiv.org/pdf/1101.5876))

Finding an optimal solution for any graph is NP-hard. 

**Unsolved puzzle**

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/flood_it_unsolved.png" alt="Flood It unsolved" width="500">

Code to utilize this package and solve the puzzle:

(Note: the ids are arbitrary and simply represent cells that share a cage)

```python
import numpy as np
from puzzle_solver import flood_it_solver as solver
board = np.array([
    ['B', 'Y', 'G', 'Y', 'R', 'B', 'Y', 'Y', 'G', 'B', 'R', 'P'],
    ['P', 'G', 'G', 'Y', 'B', 'O', 'Y', 'O', 'B', 'Y', 'R', 'O'],
    ['B', 'R', 'P', 'Y', 'O', 'R', 'G', 'G', 'G', 'R', 'R', 'Y'],
    ['O', 'G', 'P', 'G', 'Y', 'Y', 'P', 'P', 'O', 'Y', 'B', 'B'],
    ['G', 'Y', 'G', 'O', 'R', 'G', 'R', 'P', 'G', 'O', 'B', 'R'],
    ['R', 'G', 'B', 'G', 'O', 'B', 'O', 'G', 'B', 'O', 'O', 'B'],
    ['G', 'B', 'P', 'R', 'Y', 'P', 'R', 'B', 'Y', 'B', 'Y', 'P'],
    ['G', 'B', 'G', 'P', 'O', 'Y', 'R', 'Y', 'P', 'P', 'O', 'G'],
    ['R', 'P', 'B', 'O', 'B', 'G', 'Y', 'O', 'Y', 'R', 'P', 'O'],
    ['G', 'P', 'P', 'P', 'P', 'Y', 'G', 'P', 'O', 'G', 'O', 'R'],
    ['Y', 'Y', 'B', 'B', 'R', 'B', 'O', 'R', 'O', 'O', 'R', 'O'],
    ['B', 'G', 'B', 'G', 'R', 'B', 'P', 'Y', 'P', 'B', 'R', 'G']
])
solution = solver.solve_minimum_steps(board=board)
```

**Script Output**

```python
Trying with exactly 16 moves... Not possible!
Trying with exactly 32 moves... Possible!
Solution: ['Y', 'G', 'B', 'Y', 'B', 'R', 'B', 'Y', 'G', 'Y', 'G', 'B', 'B', 'G', 'Y', 'Y', 'R', 'B', 'Y', 'G', 'Y', 'B', 'Y', 'B', 'Y', 'B', 'G', 'Y', 'B', 'G', 'R', 'Y']
Trying with exactly 24 moves... Possible!
Solution: ['Y', 'G', 'B', 'Y', 'B', 'R', 'B', 'R', 'Y', 'G', 'R', 'Y', 'R', 'B', 'G', 'B', 'G', 'Y', 'G', 'B', 'Y', 'G', 'R', 'Y']
Trying with exactly 20 moves... Possible!
Solution: ['Y', 'G', 'B', 'Y', 'B', 'R', 'B', 'G', 'Y', 'G', 'B', 'G', 'Y', 'B', 'Y', 'R', 'B', 'G', 'R', 'Y']
Trying with exactly 18 moves... Possible!
Solution: ['Y', 'G', 'B', 'Y', 'R', 'B', 'R', 'Y', 'B', 'G', 'R', 'Y', 'R', 'B', 'G', 'R', 'Y', 'B']
Trying with exactly 17 moves... Not possible!
Best Horizon is: T=18
Best solution is: ['Y', 'G', 'B', 'Y', 'R', 'B', 'R', 'Y', 'B', 'G', 'R', 'Y', 'R', 'B', 'G', 'R', 'Y', 'B']
Time taken: 3.10 seconds
```

**Solved puzzle**

This picture won't mean much as the game is about the sequence and number of moves not the final frame as shown here. 

Note that the solved solution on the bottom left says that only 18 moves were used (based on the above output) despite the website saying 20 total moves are permitted (and the puzzle settings specified 0 extra moves permitted). Thus the solver managed to find a more optimal solution than the website.

<img src="https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/flood_it_solved.png" alt="Flood It solved" width="500">
