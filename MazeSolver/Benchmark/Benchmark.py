"""
    Benchmark class for comparing solution algorithms
"""

import json
import time
import os

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


    def _get_file_name(file_name, extension):
        create_name = lambda it: f'{file_name}.{extension}' if it == 0 else f'{file_name}({it}).{extension}'

        i = 0
        file = create_name(i)
        while os.path.exists(file):
            i += 1
            file = create_name(i)

        return file


    def _save_mazes(self):
        file_name = Benchmark._get_file_name("results", "json")

        print(f'Results exported: {file_name}')
        with open(file_name, 'w') as file:
            json.dump(self.results, file)


    def _export_stats(self):
        print(f'Exporting stats txt...')
        
        csv_result = f'\"id\";\"dimension\";\"steps\";\"algo\";\"time\";\"nodes\"'
        id = 0
        for dimensions_group in self.results:
            cases = dimensions_group.get("cases")

            if not cases:
                continue

            dimension = dimensions_group.get("dimension")

            if not dimension:
                dimension = '-'

            for case in cases:
                id += 1
                solution = case.get("solution")

                steps = '-'
                if solution:
                    steps = len(solution.split('-'))

                results = case.get("results")
                if not results:
                    continue

                for algorithm, res in results.items():
                    time = res.get("time")
                    nodes = res.get("expanded_nodes")
                    csv_result += f'\n\"{id}\";\"{dimension}\";\"{steps}\";\"{algorithm}\";\"{time}\";\"{nodes}\"'

        file_name = Benchmark._get_file_name("stats", 'txt')
        print(f'Stats exported: {file_name}')

        with open(file_name, 'w') as file:
            file.write(csv_result)


    def generate_results(
        self,
        dimensions=[10, 15, 20, 25, 30, 100],
        number_of_tests=10,
        solvers=[DepthFirst, BreadthFirst, AStar]
    ) -> None:
        for dim in dimensions:
            print(f'Running solutions for dimension {dim}...')
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
