
from MazeSolver import Maze

maze = Maze(dimensions=(50, 100))

with open('maze.txt', 'w') as f:
    f.write(str(maze))

# maze.print()
