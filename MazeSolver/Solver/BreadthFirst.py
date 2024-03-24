"""
    BreadthFirst class with Breadth First Search algorithm implementation
"""

from MazeSolver.Maze import Maze
from MazeSolver.Tree import Tree
from MazeSolver.Solver.SolverBase import SolverBase


class BreadthFirst(SolverBase):

    def __init__(self, maze: Maze):
       SolverBase.__init__(self, maze) 


    def solve(self, nodes: list[Tree] = None) -> Tree:
        if not nodes:
            nodes = [Tree(self.maze.start_position)]

        new_nodes = []

        for node in nodes:
            possible_states = self._get_possible_paths(node.state)

            for possible_state in possible_states:
                if self.maze.get_coordinates_type(possible_state[0], possible_state[1]) == self.maze.end:
                    return node.new_state(possible_state)
                if possible_state in node.get_positions():
                    continue

                new_nodes.append(node.new_state(possible_state))

        return self.solve(new_nodes)
