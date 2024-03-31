
class Tree:
    def __init__(self, state):
        self.state = state
        self.nodes = []
        self.path = [state]


    def get_positions(self):
        return self.path


    def new_state(self, state):
        new_tree = Tree(state)

        new_tree.nodes = []
        new_tree.path = self.path + [state]

        return new_tree


    def path_size(self):
        return len(self.path) - 1


    def __str__(self):
        return '-'.join([str(p) for p in self.path])
