class Node():
    def __init__(self, state, parent=None, action=None, value=0, cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.value = value
        self.cost = cost