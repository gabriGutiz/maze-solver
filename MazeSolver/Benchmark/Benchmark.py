"""
    Benchmark class for comparing solution algorithms
"""

import json
import time

from MazeSolver import Maze
from MazeSolver.Solver import AStar, BreadthFirst, DepthFirst
from .Result import Result

class Benchmark:

    def __init__(self, dimensions=[10, 15, 20, 25, 30, 100]) -> None:
        self.dimensions = dimensions
        self.results = []


    def _get_result(self, solver) -> Result:
        start = time.time()
        solution = solver.solve()
        end = time.time()

        exec_time = (end - start) * 10**3
        result = Result(exec_time, solution)

        return result


    def _save_mazes(self):
        with open("results.json", 'w') as file:
            json.dump(self.results, file)


    def generate_results(self, solvers=[DepthFirst, BreadthFirst, AStar]) -> None:
        for dim in self.dimensions:
            cases = []
            for _ in range(5):
                maze = Maze(dim)
                maze_group = {
                    "maze": str(maze)
                }

                results = []
                for solver in solvers:
                    result = self._get_result(solver(maze))
                    results.append({
                        "algorithm": solver.__name__,
                        "ms_time": result.time,
                        "solution": str(result.solution).replace('>', '-')
                    })

                maze_group["results"] = results
                cases.append(maze_group)
    
            self.results.append({
                "dimension": dim,
                "cases": cases
            })
        return self.results


    def export_results(self):
        self._save_mazes()
