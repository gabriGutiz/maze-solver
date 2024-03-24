
class Tree:
    def __init__(self, state):
        self.state = state
        self.nodes = []
        self.path = str(state)


    def get_positions(self):
        positions = []
        for coordinate in self.path.split('>'):
            coordinate = coordinate.strip(')').strip('(')

            coordinates = coordinate.split(', ')
            positions.append((int(coordinates[0]), int(coordinates[1])))
        return positions


    def new_state(self, state):
        new_tree = Tree(state)

        new_tree.nodes = []
        new_tree.path = self.path + f'>{state}'

        return new_tree


    def __str__(self):
        return self.path
