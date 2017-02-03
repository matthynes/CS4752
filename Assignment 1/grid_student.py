import sys  # used for file reading

import collections

import itertools

from settings import *  # use a separate file for all the constant settings


# the class we will use to store the map, and make calls to path finding
class Grid:
    # set up all the default values for the frid and read in the map from a given file
    def __init__(self, filename):
        # 2D list that will hold all of the grid tile information 
        self.__grid = []
        self.__load_data(filename)
        self.__width, self.__height = len(self.__grid), len(self.__grid[0])

    # loads the grid data from a given file name
    def __load_data(self, filename):
        # turn each line in the map file into a list of integers
        temp_grid = [list(map(int, line.strip())) for line in open(filename, 'r')]
        # transpose the input since we read it in as (y, x) 
        self.__grid = [list(i) for i in zip(*temp_grid)]

    # return the cost of a given action
    # note: this only works for actions in our LEGAL_ACTIONS defined set (8 directions)
    def __get_action_cost(self, action):
        return CARDINAL_COST if (action[0] == 0 or action[1] == 0) else DIAGONAL_COST

        # returns the tile type of a given position

    def get(self, tile):
        return self.__grid[tile[0]][tile[1]]

    def width(self):
        return self.__width

    def height(self):
        return self.__height

    # returns true if an object of a given size can navigate from start to goal
    def is_connected(self, start, goal, size):
        grid = self.sector_grid[size - 1]

        if grid[start[0]][start[1]] == grid[goal[0]][goal[1]]:
            return True
        return False

        # Student TODO: Replace this function with your A* implementation

    # returns a sample path from start tile to end tile which is probably illegal
    def get_path(self, start, end, size):
        # path = []
        # action = (1 if start[0] <= end[0] else -1, 1 if start[1] <= end[1] else -1)
        # d = (abs(start[0] - end[0]), abs(start[1] - end[1]))
        # # add the diagonal actions until we hit the row or column of the end tile
        # for diag in range(d[1] if d[0] > d[1] else d[0]):
        #     path.append(action)
        # # add the remaining straight actions to reach the end tile
        # for straight in range(d[0] - d[1] if d[0] > d[1] else d[1] - d[0]):
        #     path.append((action[0], 0) if d[0] > d[1] else (0, action[1]))
        # # return the path, the cost of the path, and the set of expanded nodes (for A*)
        # return path, sum(map(self.__get_action_cost, path)), set()

        path = AStar(start, end, self, size)
        ppath = path.a_star()
        return ppath, 0, set()

    # Student TODO: Replace this function with a better (but admissible) heuristic
    # estimate the cost for moving between start and end
    def estimate_cost(self, start, goal):
        return 0


class AStar:
    def __init__(self, start, goal, grid, size):
        self.start = Node(start)
        self.closed = set()
        self.open = {self.start}
        self.goal = goal
        self.size = size
        self.grid = grid

    def remove_min_from(self, olist):
        # return node from open list with the minimum f-cost (f=g + h)
        node = min(olist, key=lambda n: n.g + self.grid.estimate_cost(n, self.goal))
        olist.remove(node)
        return node

    def add_to_open(self, node):
        self.open.add(node)

    def is_in_open(self, node):
        return node in self.open

    def is_in_closed(self, state):
        return state in self.closed

    def a_star(self):
        while self.open:
            node = self.remove_min_from(self.open)
            if node.state == self.goal:
                return self.reconstruct_path(node)

            self.closed.add(node.state)

            for child in children(node, self.grid, self.size):
                if child.state not in self.closed:
                    child.f = child.g + self.grid.estimate_cost(child, self.goal)
                    self.open.add(child)

        return []

    def reconstruct_path(self, node):
        return []


# Node class used in A* search
def children(node, grid, size):
    x, y = node.state[0], node.state[1]
    type = grid.sector_grid[size][x][y]
    children = []

    for d in [(x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)]:
        if (d[0] > 0 and d[1] > 0) and (d[0] < grid.width() and d[1] < grid.height()):
            if grid.sector_grid[size][d[0]][d[1]] == type:
                children.append(Node(d))

    return children


class Node:
    def __init__(self, tile):
        self.state = tile
        self.action = (0, 0)
        self.g = self.f = 0
        self.parents = None

    def __lt__(self, other):
        return self.f < other.f
