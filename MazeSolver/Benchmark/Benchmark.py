"""
    Benchmark class for comparing solution algorithms
"""

import json
import time

from MazeSolver import Maze
from MazeSolver.Solver import AStar, BreadthFirst, DepthFirst
from .Result import Result

class Benchmark:

    def __init__(self) -> None:
        self.results = []


    def _get_result(self, solver) -> Result:
        start = time.time()
        solution = solver.solve()
        end = time.time()

        exec_time = (end - start) * 10**3
        result = Result(exec_time, solution, solver.expanded_nodes)

        return result


    def _save_mazes(self):
        with open("results.json", 'w') as file:
            json.dump(self.results, file)


    def _export_stats(self):
        algorithms = []
        result_cases = []
        for dimensions_group in self.results:
            cases = dimensions_group.get("cases")

            if not cases:
                continue

            dimension = dimensions_group.get("dimension")

            if not dimension:
                dimension = '-'

            for case in cases:
                solution = case.get("solution")

                steps = '-'
                if solution:
                    steps = len(solution.split('-'))

                results = case.get("results")
                if not results:
                    continue

                for algorithm in results.keys():
                    if algorithm not in algorithms:
                        algorithms.append(algorithm)

                result_cases.append({
                    "dimension": dimension,
                    "steps": steps,
                    "results": results
                })

        algos = ";".join([f"\"{a}(time|nodes)\"" for a in algorithms])
        csv_result = f'\"dimension\";\"steps\";{algos}'
        for result in result_cases:
            values = ''
            for algo in algorithms:
                algo_res = result.get("results").get(algo)
                values += '"' + '|'.join([str(val) for val in algo_res.values()]) + '";'
            values = values.removesuffix(';')

            csv_result += f'\n\"{result.get("dimension")}\";\"{result.get("steps")}\";{values}'

        with open("stats.txt", 'w') as file:
            file.write(csv_result)


    def generate_results(
        self,
        dimensions=[10, 15, 20, 25, 30, 100],
        number_of_tests=10,
        solvers=[DepthFirst, BreadthFirst, AStar]
    ) -> None:
        for dim in dimensions:
            cases = []
            for _ in range(number_of_tests):
                maze = Maze(dim)
                maze_group = {
                    "maze": str(maze)
                }

                results = {}
                for solver in solvers:
                    result = self._get_result(solver(maze))
                    results[solver.__name__] = {
                        "time": result.time,
                        "expanded_nodes": result.expanded_nodes
                    }
                    maze_group["solution"] = str(result.solution).replace('>', '-')

                maze_group["results"] = results
                cases.append(maze_group)
    
            self.results.append({
                "dimension": dim,
                "cases": cases
            })
        return self.results


    def get_result(self, solver) -> Result:
        return self._get_result(solver)


    def export_results(self):
        self._save_mazes()

        self._export_stats()
