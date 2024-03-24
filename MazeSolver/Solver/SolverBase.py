"""
    SolverBase class with basic methods to be inherit from diferent solution classes
"""

from MazeSolver import Maze


class SolverBase:
    maze: Maze
    

    def __init__(self, maze: Maze):
        self.maze = maze


    def _get_possible_paths(self, coordinates) -> list[tuple[int]]:
        movements = [
            (0, -1),
            (0, 1),
            (-1, 0),
            (1, 0)
        ]

        possible_coords = []

        for move in movements:
            next_position = (coordinates[0] + move[0], coordinates[1] + move[1])
            char = self.maze.get_coordinates_type(next_position[0], next_position[1])

            if char == self.maze.cell or char == self.maze.end:
                possible_coords.append(next_position)

        return possible_coords


    def _is_end(self, coordinates):
        return coordinates[0] == self.maze.end_position[0] and coordinates[1] == self.maze.end_position[1]
