from AStarFrontier import *
from Node import *

class Maze():
    def __init__(self):
        maze = '''
#          B
# ######### 
# #       # 
# # ##### # 
#   #     # 
### # ##### 
A   #       
'''

        self.solution = None

        if maze.count('A') != 1:
            raise Exception('must have ONE starting (A) position')
        if maze.count('B') != 1:
            raise Exception('must have ONE ending (B) position')

        maze = maze[1:-1].splitlines()
        self.height = len(maze)
        self.width = max(len(line) for line in maze)

        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if maze[i][j] == 'A':
                        self.start = (i, j)
                        row.append(False)
                    elif maze[i][j] == 'B':
                        self.goal = (i, j)
                        row.append(False)
                    elif maze[i][j] == ' ':
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()

        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print('█', end='')
                elif (i, j) == self.start:
                    print('A', end='')
                elif (i, j) == self.goal:
                    print('B', end='')
                elif solution is not None and (i, j) in solution:
                    print('*', end='')
                else:
                    print(' ', end='')

            print()
        print()

    def neighbors(self, state):
        row, col = state

        actions = list(filter(lambda x: x is not None, [
            ('up', (row - 1, col)) if row - 1 >= 0 else None,
            ('down', (row + 1, col)) if row + 1 < self.height else None,
            ('left', (row, col - 1)) if col - 1 >= 0 else None,
            ('right', (row, col + 1)) if col + 1 < self.width else None
        ]))

        result = []
        for action, (r, c) in actions:
            try:
                if not self.walls[r][c]:
                    result.append((action, (r, c), self.heuristic((r, c))))
            except IndexError:
                pass

        return result

    def heuristic(self, state):
        row, col = state
        goalRow, goalCol = self.goal

        # Manhattan distance
        return abs(row - goalRow) + abs(col - goalCol)

    def solve(self):
        start = Node(state=self.start)

        frontier = AStarFrontier()
        frontier.add(start)

        explored = set()

        while True:
            if frontier.empty():
                raise Exception('no solution')

            node = frontier.remove()

            if node.state == self.goal:
                actions = []
                cells = []

                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent

                actions.reverse()
                cells.reverse()

                self.solution = (actions, cells)
                return

            explored.add(node.state)

            for action, state, value in self.neighbors(node.state):
                if not frontier.containsState(state) and state not in explored:
                    frontier.add(Node(state=state, parent=node,
                                 action=action, value=value, cost=node.cost + 1))

