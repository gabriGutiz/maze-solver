from simple_term_menu import TerminalMenu
from MazeSolver import Maze, Benchmark, AStar, BreadthFirst, DepthFirst


def main():
    funcs = [exec_example, benchmark]
    terminal_menu = TerminalMenu(["Example", "Benchmark"])
    choice_index = terminal_menu.show()

    funcs[choice_index]()


def benchmark():
    benchmark = Benchmark()
    benchmark.generate_results()
    benchmark.export_results()


def exec_example():
    dimension = input('Maze dimension (default 10): ')

    if not dimension:
        dimension = 10

    maze = Maze(int(dimension))

    print('='*10 + ' GENERATED MAZE ' + '='*10)
    maze.print()

    solvers = [AStar, DepthFirst, BreadthFirst]
    terminal_menu = TerminalMenu(["A*", "Depth First Search", "Breadth First Search"])
    choice_index = terminal_menu.show()

    solver = solvers[choice_index](maze)

    print('='*13 + ' SOLUTION ' + '='*13)
    solution = solver.solve()
    print(str(solution).replace('>', '-'))

    print('='*12 + ' SOLVED MAZE ' + '='*12)
    maze.solve(solution.get_positions())
    maze.print()


if __name__ == '__main__':
    main()
