"""
    DepthFirst class with Depth First Search algorithm implementation
"""

from MazeSolver.Maze import Maze
from MazeSolver.Tree import Tree
from MazeSolver.Solver.SolverBase import SolverBase


class DepthFirst(SolverBase):

    def __init__(self, maze: Maze):
        SolverBase.__init__(self, maze) 


    def _solve(self, node=None) -> Tree:
        if not node:
            node = Tree(self.maze.start_position)

        new_nodes = []
        for possible_state in self._get_possible_paths(node.state):
            if self.maze.get_coordinates_type(possible_state[0], possible_state[1]) == self.maze.end:
                self.expanded_nodes += 1
                return node.new_state(possible_state)
            if possible_state in node.get_positions():
                continue
            new_nodes.append(node.new_state(possible_state))

        if not new_nodes:
            return None

        for new_node in new_nodes:
            solution = self._solve(new_node)
            self.expanded_nodes += 1
            if solution:
                return solution

        return None


    def solve(self) -> Tree:
        if self.maze.solved:
            return None
        return self._solve()
