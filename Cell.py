from math import sqrt

from CellType import CellType


class Cell:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.g_score = 0
        self.h_score = 0
        self.f_score = 0
        self.neighbors = []
        self.previous_cell = None
        self.color, self.outline, self.path_cost = self.calculate_color_and_cost()

    def calculate_color_and_cost(self):
        if self.type is CellType.floor.value:
            return 'white', 'black', 1
        elif self.type is CellType.obstacle.value:
            return 'black', 'white', 1
        elif self.type is CellType.initial_state.value:
            return 'red', 'black', 0
        elif self.type is CellType.goal_state.value:
            return '#00ff00', 'black', 1
        elif self.type is CellType.water.value:
            return '#4d4dff', 'black', 100
        elif self.type is CellType.mountain.value:
            return '#a6a6a6', 'black', 50
        elif self.type is CellType.forest.value:
            return '#008000', 'black', 10
        elif self.type is CellType.grass.value:
            return '#80ff80', 'black', 5
        elif self.type is CellType.road.value:
            return '#bf8040', 'black', 1
        else:
            return '#e426ff', 'black', 1

    def initialize(self, board, goal_state_coordinates, current_g_score):
        if self.type is '#':
            print('CellType is obstacle')
        else:
            self.g_score = self.path_cost + current_g_score  # The cost of the path from the start node to n
            self.h_score = self.calculate_manhattan_distance(
                goal_state_coordinates)  # Heuristic function that estimates the cost of the cheapest path from n to the goal
            self.f_score = self.g_score + self.h_score  # f(n) = g(n) + h(n)
            self.neighbors = self.calculate_neighbors(board)

    def calculate_euclidean_distance(self, goal_state_coordinates):
        print('========= Calculating euclidean distance =========')
        print('Goal state coordinates: ' + str(goal_state_coordinates))
        print('Cell coordinates: ' + str((self.x, self.y)))
        distance = sqrt((self.x - goal_state_coordinates[0]) ** 2 + (self.y - goal_state_coordinates[1]) ** 2)
        print('Euclidean distance: ' + str(distance))
        return distance

    def calculate_manhattan_distance(self, goal_state_coordinates):
        print('========= Calculating manhattan distance =========')
        print('Goal state coordinates: ' + str(goal_state_coordinates))
        print('Cell coordinates: ' + str((self.x, self.y)))
        distance = abs(self.x - goal_state_coordinates[0]) + abs(self.y - goal_state_coordinates[1])
        print('Manhattan distance: ' + str(distance))
        return distance

    def calculate_neighbors(self, board):
        print('========= Calculating neighbors =========')

        neighbors = []

        # North neighbor
        if self.y <= 0:
            print('No cell found in y = ' + str((self.x, self.y - 1)))
        elif board[self.y - 1][self.x].type is '#':
            print(str((self.x, self.y - 1)) + ' is an obstacle, skipping add')
        else:
            neighbors.append(board[self.y - 1][self.x])

        # East neighbor
        if self.x >= len(board[self.y]) - 1:
            print('No cell found in ' + str((self.x + 1, self.y)))
        elif board[self.y][self.x + 1].type is '#':
            print(str((self.x + 1, self.y)) + ' is an obstacle, skipping add')
        else:
            neighbors.append(board[self.y][self.x + 1])

        # South neighbor
        if self.y >= len(board) - 1:
            print('No cell found in y = ' + str((self.x, self.y + 1)))
        elif board[self.y + 1][self.x].type is '#':
            print(str((self.x, self.y + 1)) + ' is an obstacle, skipping add')
        else:
            neighbors.append(board[self.y + 1][self.x])

        # West neighbor
        if self.x <= 0:
            print('No cell found in x = ' + str((self.x - 1, self.y)))
        elif board[self.y][self.x - 1].type is '#':
            print(str((self.x - 1, self.y)) + ' is an obstacle, skipping add')
        else:
            neighbors.append(board[self.y][self.x - 1])

        return neighbors

    def __lt__(self, other):
        return self.f_score < other.f_score
