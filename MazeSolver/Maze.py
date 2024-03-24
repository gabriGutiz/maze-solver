"""
    Maze class
"""

import random
from colorama import init, Fore


class Maze:
    wall: str
    cell: str
    start: str
    end: str
    unvisited: str
    paths: str
    maze: list[list[str]]
    start_position: tuple[int]
    end_position: tuple[int]
    height: int
    width: int
    
    def __init__(
        self,
        dimensions = 10,
        wall_char = '#',
        cell_char = '.',
        start_char = 'I',
        end_char = 'F'
    ) -> None:
        
        if isinstance(dimensions, tuple):
            self.height = dimensions[-1]
            self.width = dimensions[0]
        else:
            self.width = self.height = dimensions
        self.wall = wall_char
        self.cell = cell_char
        self.start = start_char
        self.end = end_char
        self.unvisited = 'u'
        self.paths = ['╯', '╭', '╰','╮','|','—']
        self.maze = []
        self.solved = False
        self.start_position = ()
        self.end_position = ()

        self._generate()


    def _set_start_and_end(self):
        paths = []
        for i in range(0, len(self.maze)):
            for j in range(0, len(self.maze[i])):
                if self.maze[i][j] == self.cell:
                    paths.append((i, j))

        self.start_position = random.choice(paths)
        self.end_position = random.choice(paths)

        while self.start_position == self.end_position:
            self.end_position = random.choice(paths)

        self.maze[self.start_position[0]][self.start_position[1]] = self.start
        self.maze[self.end_position[0]][self.end_position[1]] = self.end
                

    def _generate(self):
        for i in range(0, self.height):
            line = []
            for j in range(0, self.width):
                line.append(self.unvisited)
            self.maze.append(line)

        # Randomize starting point and set it a cell
        starting_height = int(random.random()*self.height)
        starting_width = int(random.random()*self.width)
        if (starting_height == 0):
            starting_height += 1
        if (starting_height == self.height-1):
            starting_height -= 1
        if (starting_width == 0):
            starting_width += 1
        if (starting_width == self.width-1):
            starting_width -= 1

        # Mark it as cell and add surrounding walls to the list
        self.maze[starting_height][starting_width] = self.cell
        walls = []
        walls.append([starting_height - 1, starting_width])
        walls.append([starting_height, starting_width - 1])
        walls.append([starting_height, starting_width + 1])
        walls.append([starting_height + 1, starting_width])

        # Denote walls in maze
        self.maze[starting_height-1][starting_width] = self.wall
        self.maze[starting_height][starting_width - 1] = self.wall
        self.maze[starting_height][starting_width + 1] = self.wall
        self.maze[starting_height + 1][starting_width] = self.wall

        while (walls):
            # Pick a random wall
            rand_wall = walls[int(random.random()*len(walls))-1]

            # Check if it is a left wall
            if (rand_wall[1] != 0):
                if (self.maze[rand_wall[0]][rand_wall[1]-1] == self.unvisited and self.maze[rand_wall[0]][rand_wall[1]+1] == self.cell):
                    # Find the number of surrounding cells
                    s_cells = self._surrounding_cells(rand_wall)

                    if (s_cells < 2):
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = self.cell

                        # Mark the new walls
                        # Upper cell
                        if (rand_wall[0] != 0):
                            if (self.maze[rand_wall[0]-1][rand_wall[1]] != self.cell):
                                self.maze[rand_wall[0]-1][rand_wall[1]] = self.wall
                            if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]-1, rand_wall[1]])


                        # Bottom cell
                        if (rand_wall[0] != self.height-1):
                            if (self.maze[rand_wall[0]+1][rand_wall[1]] != self.cell):
                                self.maze[rand_wall[0]+1][rand_wall[1]] = self.wall
                            if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]+1, rand_wall[1]])

                        # Leftmost cell
                        if (rand_wall[1] != 0):	
                            if (self.maze[rand_wall[0]][rand_wall[1]-1] != self.cell):
                                self.maze[rand_wall[0]][rand_wall[1]-1] = self.wall
                            if ([rand_wall[0], rand_wall[1]-1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]-1])
                    

                    # Delete wall
                    for wall in walls:
                        if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                            walls.remove(wall)

                    continue

            # Check if it is an upper wall
            if (rand_wall[0] != 0):
                if (self.maze[rand_wall[0]-1][rand_wall[1]] == self.unvisited and self.maze[rand_wall[0]+1][rand_wall[1]] == self.cell):

                    s_cells = self._surrounding_cells(rand_wall)
                    if (s_cells < 2):
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = self.cell

                        # Mark the new walls
                        # Upper cell
                        if (rand_wall[0] != 0):
                            if (self.maze[rand_wall[0]-1][rand_wall[1]] != self.cell):
                                self.maze[rand_wall[0]-1][rand_wall[1]] = self.wall
                            if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]-1, rand_wall[1]])

                        # Leftmost cell
                        if (rand_wall[1] != 0):
                            if (self.maze[rand_wall[0]][rand_wall[1]-1] != self.cell):
                                self.maze[rand_wall[0]][rand_wall[1]-1] = self.wall
                            if ([rand_wall[0], rand_wall[1]-1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]-1])

                        # Rightmost cell
                        if (rand_wall[1] != self.width-1):
                            if (self.maze[rand_wall[0]][rand_wall[1]+1] != self.cell):
                                self.maze[rand_wall[0]][rand_wall[1]+1] = self.wall
                            if ([rand_wall[0], rand_wall[1]+1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]+1])

                    # Delete wall
                    for wall in walls:
                        if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                            walls.remove(wall)

                    continue

            # Check the bottom wall
            if (rand_wall[0] != self.height-1):
                if (self.maze[rand_wall[0]+1][rand_wall[1]] == self.unvisited and self.maze[rand_wall[0]-1][rand_wall[1]] == self.cell):

                    s_cells = self._surrounding_cells(rand_wall)
                    if (s_cells < 2):
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = self.cell

                        # Mark the new walls
                        if (rand_wall[0] != self.height-1):
                            if (self.maze[rand_wall[0]+1][rand_wall[1]] != self.cell):
                                self.maze[rand_wall[0]+1][rand_wall[1]] = self.wall
                            if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]+1, rand_wall[1]])
                        if (rand_wall[1] != 0):
                            if (self.maze[rand_wall[0]][rand_wall[1]-1] != self.cell):
                                self.maze[rand_wall[0]][rand_wall[1]-1] = self.wall
                            if ([rand_wall[0], rand_wall[1]-1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]-1])
                        if (rand_wall[1] != self.width-1):
                            if (self.maze[rand_wall[0]][rand_wall[1]+1] != self.cell):
                                self.maze[rand_wall[0]][rand_wall[1]+1] = self.wall
                            if ([rand_wall[0], rand_wall[1]+1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]+1])

                    # Delete wall
                    for wall in walls:
                        if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                            walls.remove(wall)


                    continue

            # Check the right wall
            if (rand_wall[1] != self.width-1):
                if (self.maze[rand_wall[0]][rand_wall[1]+1] == self.unvisited and self.maze[rand_wall[0]][rand_wall[1]-1] == self.cell):

                    s_cells = self._surrounding_cells(rand_wall)
                    if (s_cells < 2):
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = self.cell

                        # Mark the new walls
                        if (rand_wall[1] != self.width-1):
                            if (self.maze[rand_wall[0]][rand_wall[1]+1] != self.cell):
                                self.maze[rand_wall[0]][rand_wall[1]+1] = self.wall
                            if ([rand_wall[0], rand_wall[1]+1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]+1])
                        if (rand_wall[0] != self.height-1):
                            if (self.maze[rand_wall[0]+1][rand_wall[1]] != self.cell):
                                self.maze[rand_wall[0]+1][rand_wall[1]] = self.wall
                            if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]+1, rand_wall[1]])
                        if (rand_wall[0] != 0):	
                            if (self.maze[rand_wall[0]-1][rand_wall[1]] != self.cell):
                                self.maze[rand_wall[0]-1][rand_wall[1]] = self.wall
                            if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]-1, rand_wall[1]])

                    # Delete wall
                    for wall in walls:
                        if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                            walls.remove(wall)

                    continue

            # Delete the wall from the list anyway
            for wall in walls:
                if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                    walls.remove(wall)
            
        # Mark the remaining unvisited cells as walls
        for i in range(0, self.height):
            for j in range(0, self.width):
                if (self.maze[i][j] == self.unvisited):
                    self.maze[i][j] = self.wall

        self._set_start_and_end()


    def _surrounding_cells(self, rand_wall):
        s_cells = 0
        if (self.maze[rand_wall[0]-1][rand_wall[1]] == self.cell):
            s_cells += 1
        if (self.maze[rand_wall[0]+1][rand_wall[1]] == self.cell):
            s_cells += 1
        if (self.maze[rand_wall[0]][rand_wall[1]-1] == self.cell):
            s_cells +=1
        if (self.maze[rand_wall[0]][rand_wall[1]+1] == self.cell):
            s_cells += 1

        return s_cells


    def print(self, print_coords=False) -> None:
        init()

        if print_coords:
            print(' '*len(str(self.height)), end=' ')
            for i in range(0, self.width):
                print(Fore.YELLOW + str(i)[-1], end=' ')
            print('\n', end='')


        for i in range(0, self.height):
            if print_coords:
                print(Fore.YELLOW + (len(str(self.height)) - len(str(i)))*' ' + str(i), end=' ')

            for j in range(0, self.width):
                char = self.maze[i][j].strip()
                if char in self.paths:
                    print(Fore.GREEN + char, end=' ')
                    continue
                
                match char:
                    case self.unvisited:
                        print(Fore.WHITE + char, end=' ')
                    case self.cell:
                        print(Fore.MAGENTA + char, end=' ')
                    case self.start:
                        print(Fore.WHITE + char, end=' ')
                    case self.end:
                        print(Fore.CYAN + char, end=' ')
                    case _:
                        print(Fore.RED + char, end=' ')

            print(Fore.RESET + '\n', end='')


    def get_coordinates_type(self, row, col):
        if row >= self.height or col >= self.width:
            return self.unvisited
        return self.maze[row][col]


    def solve(self, path: list[tuple]):
        self.maze_solved = self.maze.copy()

        paths = {
            ( 1,  1): {
                ( 0,  1): '╮',
                ( 1,  0): '╰'
            },
            ( 1, -1): {
                ( 0,  1): '╭',
                ( 0, -1): '╭',
                ( 1,  0): '╯'
            },
            (-1, -1): {
                (-1,  0): '╮',
                ( 0,  1): '╯',
                ( 1,  0): '╰',
                ( 0, -1): '╰'
            },
            (-1,  1): {
                (-1,  0): '╭',
                ( 0,  1): '╯'
            },
            (-2,  0): '|',
            ( 2,  0): '|',
            ( 0, -2): '—',
            ( 0,  2): '—'
        }


        for i in range(1, len(path)-1):
            x, y = path[i]

            last_x, last_y = path[i-1]
            next_x, next_y = path[i+1]

            difference = (next_x-last_x, next_y-last_y)
            chars = paths.get(difference)

            if not isinstance(chars, dict):
                self.maze_solved[x][y] = chars
            else:
                diff_actual_last = (x-last_x, y-last_y)
                char = chars.get(diff_actual_last)
                self.maze_solved[x][y] = char

        self.solved = True


    def __str__(self) -> str:
        return '\n'.join([' '.join(row) for row in self.maze])
