from math import inf


class AStarFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def containsState(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception('empty')
        else:
            minValue = inf
            idx = None

            for i, node in enumerate(self.frontier):
                nodeValue = node.value + node.cost
                if nodeValue < minValue:
                    minValue = nodeValue
                    idx = i

            return self.frontier.pop(idx)
