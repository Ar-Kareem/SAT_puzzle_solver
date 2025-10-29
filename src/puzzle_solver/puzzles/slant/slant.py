from typing import Literal, Optional, Union
from dataclasses import dataclass

import numpy as np
from ortools.sat.python import cp_model

from puzzle_solver.core.utils import Pos, get_all_pos, in_bounds, get_pos
from puzzle_solver.core.utils_ortools import force_no_loops, generic_solve_all, SingleSolution
from puzzle_solver.core.utils_visualizer import combined_function


@dataclass(frozen=True)
class Node:
    """The grid is represented as a graph of cells connected to corners."""
    node_type: Union[Literal["Cell"], Literal["Corner"]]
    pos: Pos
    slant: Union[Literal["/"], Literal["\\"], None]

    def get_neighbors(self, board_nodes: dict[tuple[str, Pos, Optional[str]], "Node"]) -> list["Node"]:
        if self.node_type == "Cell" and self.slant == "/":
            n1 = board_nodes[("Corner", get_pos(self.pos.x+1, self.pos.y), None)]
            n2 = board_nodes[("Corner", get_pos(self.pos.x, self.pos.y+1), None)]
            return [n1, n2]
        elif self.node_type == "Cell" and self.slant == "\\":
            n1 = board_nodes[("Corner", get_pos(self.pos.x, self.pos.y), None)]
            n2 = board_nodes[("Corner", get_pos(self.pos.x+1, self.pos.y+1), None)]
            return [n1, n2]
        elif self.node_type == "Corner":
            # 4 cells, 2 cells per slant
            n1 = ("Cell", get_pos(self.pos.x-1, self.pos.y-1), "\\")
            n2 = ("Cell", get_pos(self.pos.x, self.pos.y-1), "/")
            n3 = ("Cell", get_pos(self.pos.x-1, self.pos.y), "/")
            n4 = ("Cell", get_pos(self.pos.x, self.pos.y), "\\")
            return {board_nodes[n] for n in [n1, n2, n3, n4] if n in board_nodes}


class Board:
    def __init__(self, numbers: Union[list[tuple[Pos, int]], np.array], V: int = None, H: int = None):
        if isinstance(numbers, np.ndarray):
            V, H = numbers.shape
            V = V - 1
            H = H - 1
            numbers = [(get_pos(x=pos[1], y=pos[0]), int(d)) for pos, d in np.ndenumerate(numbers) if str(d).isdecimal()]
            numbers = [(p, n) for p, n in numbers if n >= 0]
        else:
            assert V is not None and H is not None, 'V and H must be provided if numbers is not a numpy array'
        assert V >= 1 and H >= 1, 'V and H must be at least 1'
        assert all(isinstance(number, int) and number >= 0 for (pos, number) in numbers), 'numbers must be a list of integers'
        self.V = V
        self.H = H
        self.numbers = numbers
        self.pos_to_number: dict[Pos, int] = {pos: number for pos, number in numbers}

        self.model = cp_model.CpModel()
        self.model_vars: dict[tuple[Pos, str], cp_model.IntVar] = {}
        self.nodes: dict[Node, cp_model.IntVar] = {}
        self.neighbor_dict: dict[Node, set[Node]] = {}

        self.create_vars()
        self.add_all_constraints()


    def create_vars(self):
        for pos in get_all_pos(self.V, self.H):
            self.model_vars[(pos, '/')] = self.model.NewBoolVar(f'{pos}:/')
            self.model_vars[(pos, '\\')] = self.model.NewBoolVar(f'{pos}:\\')
            self.model.AddExactlyOne([self.model_vars[(pos, '/')], self.model_vars[(pos, '\\')]])
        for (pos, slant), v in self.model_vars.items():
            self.nodes[Node(node_type="Cell", pos=pos, slant=slant)] = v
        for pos in get_all_pos(self.V + 1, self.H + 1):
            self.nodes[Node(node_type="Corner", pos=pos, slant=None)] = self.model.NewConstant(1)


    def add_all_constraints(self):
        for pos, number in self.pos_to_number.items():
            # pos is a position on the intersection of 4 cells
            # when pos is (xi, yi) then it gets a +1 contribution for each:
            # - cell (xi-1, yi-1) is a "\\"
            # - cell (xi, yi) is a "\\"
            # - cell (xi, yi-1) is a "/"
            # - cell (xi-1, yi) is a "/"
            xi, yi = pos.x, pos.y
            tl_pos = get_pos(xi-1, yi-1)
            br_pos = get_pos(xi, yi)
            tr_pos = get_pos(xi, yi-1)
            bl_pos = get_pos(xi-1, yi)
            tl_var = self.model_vars[(tl_pos, '\\')] if in_bounds(tl_pos, self.V, self.H) else 0
            br_var = self.model_vars[(br_pos, '\\')] if in_bounds(br_pos, self.V, self.H) else 0
            tr_var = self.model_vars[(tr_pos, '/')] if in_bounds(tr_pos, self.V, self.H) else 0
            bl_var = self.model_vars[(bl_pos, '/')] if in_bounds(bl_pos, self.V, self.H) else 0
            self.model.Add(sum([tl_var, tr_var, bl_var, br_var]) == number)
        board_nodes = {(node.node_type, node.pos, node.slant): node for node in self.nodes.keys()}
        self.neighbor_dict = {node: node.get_neighbors(board_nodes) for node in self.nodes.keys()}
        no_loops_vars = force_no_loops(self.model, self.nodes, is_neighbor=lambda n1, n2: n1 in self.neighbor_dict[n2])
        self.no_loops_vars = no_loops_vars


    def solve_and_print(self, verbose: bool = True):
        def board_to_solution(board: Board, solver: cp_model.CpSolverSolutionCallback) -> SingleSolution:
            assignment: dict[Pos, int] = {}
            # graph = {node: solver.Value(var) for node, var in board.nodes.items()}
            for (pos, s), var in board.model_vars.items():
                if solver.Value(var) == 1:
                    assignment[pos] = s
            for p in get_all_pos(self.V, self.H):
                assert p in assignment, f'position {p} is not assigned a number'
            return SingleSolution(assignment=assignment)
        def callback(single_res: SingleSolution):
            print("Solution found")
            print(combined_function(self.V, self.H, center_char=lambda r, c: single_res.assignment[get_pos(x=c, y=r)]))
        return generic_solve_all(self, board_to_solution, callback=callback if verbose else None, verbose=verbose)
