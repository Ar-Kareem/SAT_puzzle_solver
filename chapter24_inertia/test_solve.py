import numpy as np

from . import solver
from . import tsp
from core.utils import Direction8

# https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/inertia.html#15x12%23919933974949365
bor = np.array([
  ["M", "W", " ", "M", "O", "O", "W", "O", "W", "O", "O", " ", "W", " ", "M"],
  ["M", " ", "O", "M", "W", "O", " ", "M", "W", "G", "W", " ", "M", "W", "G"],
  ["M", "O", " ", "M", " ", "G", " ", "M", "M", "O", "G", " ", "O", "O", "W"],
  ["B", " ", " ", "M", "G", "O", "O", "W", "G", "M", "M", "G", "W", "W", "W"],
  ["G", "M", "G", "O", "M", "G", "M", "O", "G", "G", "G", "G", "G", " ", "O"],
  ["O", "W", "O", "G", "O", "G", "O", "G", "G", "G", " ", "W", "G", " ", "W"],
  ["M", " ", " ", "M", " ", " ", "W", "M", "O", "W", "W", "G", "O", "O", "W"],
  ["W", "O", " ", "W", "W", "W", "O", "G", "G", "O", "W", "G", "O", "M", "O"],
  [" ", " ", " ", "M", "M", "O", "M", "W", "M", "G", "G", "M", "M", " ", " "],
  ["W", "O", "W", "W", "G", "M", "G", "W", "G", " ", "M", "O", "M", "W", "M"],
  ["G", " ", "M", "O", "O", "G", "G", " ", "O", " ", "W", "G", " ", "M", " "],
  ["G", " ", "G", "M", "M", "W", "W", " ", "O", "O", "M", " ", "W", "W", " "]
])
start_pos, edges_to_direction, gems_to_edges = solver.parse_nodes_and_edges(bor)
# print("edges_to_direction", edges_to_direction)
edges = set(edges_to_direction.keys())

optimal_walk = tsp.solve_optimal_walk(start_pos, edges, gems_to_edges)

cost = len(optimal_walk) - 1
for edge in optimal_walk:
  assert edge in edges_to_direction, f'edge {edge} not valid yet was in optimal_walk'
direction_to_str = {Direction8.UP: '↑', Direction8.DOWN: '↓', Direction8.LEFT: '←', Direction8.RIGHT: '→', Direction8.UP_LEFT: '↖', Direction8.UP_RIGHT: '↗', Direction8.DOWN_LEFT: '↙', Direction8.DOWN_RIGHT: '↘'}
optimal_walk_directions = [direction_to_str[edges_to_direction[edge]] for edge in optimal_walk]
print("cost", cost)
for i, direction in enumerate(optimal_walk_directions):
  print(f"{direction}", end=' ')
  if i % 5 == 4:
    print()

# def test_ground():
#   binst = solver.Board(board=bor, sides={'top': top, 'side': side})
#   solutions = binst.solve_and_print()
#   ground = np.array([
#     [' ', 'T', 'E', ' ', ' ', ' ', ' ', 'E', 'T', ' ', 'T', 'E', 'T', 'E', ' '],
#     [' ', ' ', ' ', ' ', 'T', 'E', ' ', 'T', ' ', 'T', ' ', ' ', 'T', ' ', ' '],
#     ['E', 'T', 'E', 'T', ' ', ' ', ' ', 'E', ' ', 'E', ' ', ' ', 'E', ' ', 'E'],
#     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'T', ' ', ' ', ' ', 'T', ' ', 'T'],
#     [' ', 'E', ' ', ' ', 'E', ' ', 'E', ' ', 'E', ' ', ' ', ' ', 'E', ' ', ' '],
#     [' ', 'T', ' ', ' ', 'T', ' ', 'T', ' ', ' ', 'T', 'E', ' ', 'T', 'T', 'E'],
#     [' ', 'T', ' ', ' ', 'T', 'E', ' ', 'E', 'T', ' ', ' ', ' ', 'E', ' ', ' '],
#     [' ', 'E', ' ', ' ', ' ', ' ', 'T', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#     [' ', ' ', ' ', ' ', 'E', 'T', 'E', ' ', ' ', 'E', 'T', ' ', 'E', 'T', 'E'],
#     ['E', ' ', 'E', 'T', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'T', ' ', 'T'],
#     ['T', ' ', ' ', ' ', ' ', ' ', ' ', 'T', 'E', ' ', ' ', 'T', 'E', ' ', 'E'],
#     ['T', ' ', ' ', 'E', 'T', 'E', 'T', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#     ['E', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'T', 'E', 'T', 'E', ' ', 'E', 'T'],
#     [' ', 'T', 'E', ' ', 'E', 'T', 'E', ' ', ' ', ' ', ' ', ' ', 'T', ' ', ' '],
#     ['E', 'T', ' ', ' ', 'T', ' ', ' ', ' ', 'E', 'T', 'E', 'T', 'E', ' ', ' '],
#   ])
#   assert len(solutions) == 1, f'unique solutions != 1, == {len(solutions)}'
#   solution = solutions[0].assignment
#   ground_assignment = {get_pos(x=x, y=y): 1 if ground[y][x] == 'E' else 0 for x in range(ground.shape[1]) for y in range(ground.shape[0]) if ground[y][x] in [' ', 'E']}
#   assert set(solution.keys()) == set(ground_assignment.keys()), f'solution keys != ground assignment keys, {set(solution.keys()) ^ set(ground_assignment.keys())} \n\n\n{solution} \n\n\n{ground_assignment}'
#   for pos in solution.keys():
#     assert solution[pos] == ground_assignment[pos], f'solution[{pos}] != ground_assignment[{pos}], {solution[pos]} != {ground_assignment[pos]}'

# if __name__ == '__main__':
#   test_ground()
