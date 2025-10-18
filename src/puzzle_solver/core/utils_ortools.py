import time
import json
from dataclasses import dataclass
from typing import Optional, Callable, Any, Union

from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import CpSolverSolutionCallback

from puzzle_solver.core.utils import Pos


@dataclass(frozen=True)
class SingleSolution:
    assignment: dict[Pos, Union[str, int]]

    def get_hashable_solution(self) -> str:
        result = []
        for pos, v in self.assignment.items():
            result.append((pos.x, pos.y, v))
        return json.dumps(result, sort_keys=True)


def and_constraint(model: cp_model.CpModel, target: cp_model.IntVar, cs: list[cp_model.IntVar]):
    for c in cs:
        model.Add(target <= c)
    model.Add(target >= sum(cs) - len(cs) + 1)


def or_constraint(model: cp_model.CpModel, target: cp_model.IntVar, cs: list[cp_model.IntVar]):
    for c in cs:
        model.Add(target >= c)
    model.Add(target <= sum(cs))



class AllSolutionsCollector(CpSolverSolutionCallback):
    def __init__(self,
            board: Any,
            board_to_solution: Callable[Any, SingleSolution],
            max_solutions: Optional[int] = None,
            callback: Optional[Callable[SingleSolution, None]] = None
        ):
        super().__init__()
        self.board = board
        self.board_to_solution = board_to_solution
        self.max_solutions = max_solutions
        self.callback = callback
        self.solutions = []
        self.unique_solutions = set()

    def on_solution_callback(self):
        try:
            result = self.board_to_solution(self.board, self)
            result_json = result.get_hashable_solution()
            if result_json in self.unique_solutions:
                return
            self.unique_solutions.add(result_json)
            self.solutions.append(result)
            if self.callback is not None:
                self.callback(result)
            if self.max_solutions is not None and len(self.solutions) >= self.max_solutions:
                self.StopSearch()
        except Exception as e:
            print(e)
            raise e

def generic_solve_all(board: Any, board_to_solution: Callable[Any, SingleSolution], max_solutions: Optional[int] = None, callback: Optional[Callable[[SingleSolution], None]] = None, verbose: bool = True) -> list[SingleSolution]:
    try:
        solver = cp_model.CpSolver()
        solver.parameters.enumerate_all_solutions = True
        collector = AllSolutionsCollector(board, board_to_solution, max_solutions=max_solutions, callback=callback)
        tic = time.time()
        solver.solve(board.model, collector)
        if verbose:
            print("Solutions found:", len(collector.solutions))
            print("status:", solver.StatusName())
            toc = time.time()
            print(f"Time taken: {toc - tic:.2f} seconds")
        return collector.solutions
    except Exception as e:
        print(e)
        raise e