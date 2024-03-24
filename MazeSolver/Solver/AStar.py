"""
    AStar class with A* algorithm implementation
"""

from MazeSolver.Maze import Maze
from MazeSolver.Tree import Tree
from MazeSolver.Solver.SolverBase import SolverBase


class AStar(SolverBase):

    def __init__(self, maze: Maze):
       SolverBase.__init__(self, maze) 


    def _calculate_cost(self, coor: tuple) -> float:
        diff = (
            abs(self.maze.end_position[0] - coor[0]),
            abs(self.maze.end_position[1] - coor[1])
        )

        return (diff[0]**2 + diff[1]**2)**0.5


    def _solve(self, node=None) -> Tree:
        if not node:
            node = Tree(self.maze.start_position)

        new_nodes = []
        for possible_state in self._get_possible_paths(node.state):
            if self.maze.get_coordinates_type(possible_state[0], possible_state[1]) == self.maze.end:
                return node.new_state(possible_state)
            if possible_state in node.get_positions():
                continue
            new_nodes.append(node.new_state(possible_state))

        new_nodes = sorted(new_nodes, key=lambda x: self._calculate_cost(x.state))
        if not new_nodes:
            return None

        for new_node in new_nodes:
            solution = self._solve(new_node)
            if solution:
                return solution

        return None


    def solve(self) -> Tree:
        if self.maze.solved:
            return None
        return self._solve()
