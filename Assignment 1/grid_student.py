import collections
import heapq

import itertools
from queue import PriorityQueue

from settings import *  # use a separate file for all the constant settings


# the class we will use to store the map, and make calls to path finding
class Grid:
    # set up all the default values for the frid and read in the map from a given file
    def __init__(self, filename):
        # 2D list that will hold all of the grid tile information 
        self.__grid = []
        self.__load_data(filename)
        self.__width, self.__height = len(self.__grid), len(self.__grid[0])

        # flood fill algorithm to create connectivity/sector map
        def flood_fill(grid, start, label, size):
            start_type = self.get(start)

            # initialize queue with starting tile
            # queue is a set to avoid unnecessarily adding length with duplicate tiles before
            # they're visited
            queue = {start}
            visited = []

            while queue:
                node = queue.pop()

                if node not in visited:
                    visited.append(node)

                    x = node[0]
                    y = node[1]
                    node_type = self.get(node)

                    # if currently checked tile different type than first then do nothing
                    if node_type != start_type:
                        continue

                    # check type of each tile in the object itself, starting from top left
                    # corner (x,y). if any tile is different then abandon the search
                    try:
                        for xx in range(size):
                            for yy in range(size):
                                if (x + xx) < self.width() and \
                                                (y + yy) < self.height():
                                    check_type = self.get((x + xx, y + yy))
                                    # make sure all tiles inside the object are same type
                                    assert check_type == node_type
                    except AssertionError:
                        continue

                    # assign label to tile if it's unvisited (0)
                    if grid[x][y] == 0:
                        grid[x][y] = label
                        # add surrounding 4 spaces (up, down, left, right) to search queue
                        if x > 0:
                            queue.add((x - 1, y))
                        if x < len(grid[y]) - 1:
                            queue.add((x + 1, y))
                        if y > 0:
                            queue.add((x, y - 1))
                        if y < len(grid) - 1:
                            queue.add((x, y + 1))

            return grid

        # generate 2D grids initialized to 0s for each object size
        #  format of 3D grid is [size][x][y]
        # TODO: fix magic number 3
        self.sector_grid = [[[0] * self.width() for _ in range(self.height())] for _ in range(3)]

        # call flood fill on each 2D grid, starting at first 0-labelled tile
        for i in range(3):
            c = 1
            for j, row in enumerate(self.sector_grid[i]):
                for k, tile in enumerate(row):
                    if tile == 0:
                        self.sector_grid[i] = flood_fill(self.sector_grid[i], (j, k), c, i + 1)
                        c += 1

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
        if self.is_connected(start, end, size):
            astar = AStar(start, end, self, size)
            path = astar.a_star()
            return path, 0, set(path)

        return [], 0, set()

    # Student TODO: Replace this function with a better (but admissible) heuristic
    # estimate the cost for moving between start and end
    def estimate_cost(self, start, goal):
        return 1


class AStar:
    def __init__(self, start, goal, grid, size):
        self.start = Node(start)
        self.closed = set()
        self.open = []
        heapq.heappush(self.open, self.start)
        self.goal = goal
        self.size = size
        self.grid = grid

    def remove_min_from(self, olist):
        # return node from open list with the minimum f-cost (f=g + h)
        # node = min(olist, key=lambda n: n.f)
        # olist.remove(node)
        # return node
        return heapq.heappop(olist)

    def add_to_open(self, node):
        heapq.heappush(self.open, node)

    def add_to_closed(self, state):
        self.closed.add(state)

    def is_in_open(self, node):
        return node in self.open

    def is_in_closed(self, state):
        return state in self.closed

    def a_star(self):
        while self.open:
            node = self.remove_min_from(self.open)
            # check if we have found the goal
            if node.state == self.goal:
                path = self.reconstruct_path(node)
                return path

            self.add_to_closed(node.state)

            for child in children(node, self.grid, self.size):
                if self.is_in_closed(child.state):
                    continue
                # if child is already in open but has more efficient g-cost then update it
                if self.is_in_open(child):
                    new_g = node.g + self.grid.estimate_cost(node, child)
                    if child.g > new_g:
                        child.g = new_g
                        child.parent = node
                        child.action = node.state
                # calculate child's g-cost and add it to the open list
                else:
                    child.g = node.g + self.grid.estimate_cost(node, child)
                    child.f = child.g + self.grid.estimate_cost(child, self.goal)

                    child.parent = node
                    child.action = node.state

                    self.add_to_open(child)
        return []

    def reconstruct_path(self, node):
        path = []

        while node.parent:
            path.append(node)
            node = node.parent
        path.append(node)
        state_path = []
        for n in path:
            state_path.append(n.state)
        return state_path[::-1]


def children(node, grid, size):
    x, y = node.state[0], node.state[1]
    children = []

    # add tiles above, below, and to the left and right of current node if they are connected
    for d in [(x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)]:
        if (0 < d[0] < grid.width()) and (0 < d[1] < grid.height()):
            if grid.is_connected((x, y), (d[0], d[1]), size):
                children.append(Node(d))

    return children


class Node:
    def __init__(self, tile):
        self.state = tile
        self.action = (0, 0)
        self.g = self.f = 0
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.state == other.state
