# Bridges (Puzzle Type #20)

This is a dedicated solver for Bridges

Below are the details of how to utilize the solver. In addition, the solver gives all possible solutions to the input thus it can be utilized to figure out if a single partial input board has multiple possible solutions.

(The solver under the hood mainly utilizes the CP-SAT solver from Google OR-Tools)

* [**Play online**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/bridges.html)

* [**Instructions**](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/bridges.html#bridges)

You have a set of islands distributed across the playing area. Each island contains a number. Your aim is to connect the islands together with bridges, in such a way that:

  - Bridges run horizontally or vertically.
  - The number of bridges terminating at any island is equal to the number written in that island.
  - Two bridges may run in parallel between the same two islands, but no more than two may do so.
  - No bridge crosses another bridge.
  - All the islands are connected together.

There are some configurable alternative modes, which involve changing the parallel-bridge limit to something other than 2

**Unsolved puzzle**

<img src="../images/bridges_unsolved.png" alt="Bridges unsolved" width="500">

Code to utilize this package and solve the puzzle:
```python
import numpy as np
from . import solver
bor = np.array([
  [' ', ' ', ' ', ' ', ' ', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '3'],
  ['2', ' ', ' ', ' ', ' ', ' ', ' ', '4', ' ', ' ', '4', ' ', ' ', '2', ' '],
  [' ', ' ', ' ', '2', ' ', '4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', '1', ' ', ' ', ' ', ' ', ' ', ' ', '1', ' ', '2', ' ', ' ', ' ', '4'],
  [' ', '2', ' ', '3', ' ', '6', ' ', '4', ' ', ' ', '3', ' ', '1', ' ', ' '],
  ['2', ' ', ' ', ' ', '2', ' ', ' ', ' ', '1', ' ', ' ', '2', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  ['2', ' ', ' ', ' ', ' ', ' ', '5', ' ', ' ', '3', ' ', '4', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', '3', ' ', ' ', ' ', '3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', '2', ' ', '2', ' ', ' ', ' ', ' ', ' ', ' ', '5', ' ', ' ', '4'],
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
  [' ', ' ', '1', ' ', ' ', '2', ' ', ' ', ' ', '1', ' ', '2', ' ', ' ', ' '],
  [' ', '4', ' ', ' ', '4', ' ', '3', ' ', ' ', ' ', '4', ' ', ' ', ' ', '4'],
])
binst = solver.Board(bor)
solutions = binst.solve_and_print()
```
**Script Output**

Note that the four numbers indicate how many bridges in the 4 directions (right, left, down, up) respectively.
```
Solution found
|    |    |    |    |    |1000|    |    |    |    |    |    |    |    |0120|

|1010|    |    |    |    |    |    |2110|    |    |2200|    |    |0200|    |

|    |    |    |2000|    |0220|    |    |    |    |    |    |    |    |    |

|    |0010|    |    |    |    |    |    |1000|    |1100|    |    |    |0112|

|    |1001|    |2100|    |2202|    |1201|    |    |1110|    |0100|    |    |

|1001|    |    |    |1100|    |    |    |0100|    |    |0020|    |    |    |

|    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |

|2000|    |    |    |    |    |2210|    |    |0210|    |0022|    |    |    |

|    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |

|    |1020|    |    |    |0120|    |    |    |    |    |    |    |    |    |

|    |    |1010|    |0110|    |    |    |    |    |    |1022|    |    |0121|

|    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |

|    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |

|    |    |0001|    |    |0002|    |    |    |0001|    |0002|    |    |    |

|    |2002|    |    |1201|    |1101|    |    |    |2101|    |    |    |0202|

Solutions found: 1
status: OPTIMAL
Time taken: 0.01 seconds
```

**Solved puzzle**

<img src="../images/bridges_solved.png" alt="Bridges solved" width="500">
