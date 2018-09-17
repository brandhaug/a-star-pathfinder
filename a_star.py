import time
import heapq

from Cell import Cell, CellType
from tkinter import *

cols = 0
rows = 0


# Loads board from file
# Returns 2d board with symbols, initial_state_coordinates as tuple and goal_state_coordinates as tuple
def load_board(board_name):
    print('========= Loading board =========')
    initial_state_coordinates_symbol = 'A'
    goal_state_coordinates_symbol = 'B'

    board = []
    initial_state_coordinates = ()
    goal_state_coordinates = ()

    with open('./boards/' + board_name) as inputfile:
        for y, line in enumerate(inputfile):
            print('y', y)
            print('line', line)
            line_list = []
            for x, char in enumerate(line):
                # print(x)
                # print(char)

                cell = Cell(x, y, char)

                if char is initial_state_coordinates_symbol:
                    initial_state_coordinates = (x, y)
                    print('initial_state_coordinates', initial_state_coordinates)
                elif char is goal_state_coordinates_symbol:
                    goal_state_coordinates = (x, y)
                    print('goal_state_coordinates', goal_state_coordinates)

                if char is '\n':
                    print('New line')
                else:
                    line_list.append(cell)
            print('Appending ' + str(line_list) + ' in board')
            board.append(line_list)

    print(str(board))
    return board, initial_state_coordinates, goal_state_coordinates


# Initializes each cell from board
# Calculates heuristic cost estimate
# Calculates neighbors
# Returns 2d board with cell objects
def initialize_board(board, goal_state_coordinates):
    print('========= Initializing board =========')
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            cell.initialize(board, goal_state_coordinates)

    return board


def draw_path(path):
    for cell in path:
        canvas.create_oval((cell_width * cell.x) + (cell_width / 4),
                           (cell_height * cell.y) + (cell_height / 4),
                           (cell_width * cell.x) + cell_width - (cell_width / 4),
                           (cell_height * cell.y) + cell_height - (cell_height / 4),
                           fill="black")


def reconstruct_path(current_cell):
    cell = current_cell
    path = []

    while cell.previous_cell:
        path.append(cell)
        cell = cell.previous_cell

    path.append(cell)

    draw_path(path)
    return []


def start_a_star(sleeping_time):
    current_cell = board[initial_state_coordinates[1]][initial_state_coordinates[0]]
    initialized = False

    # Open set contains floors not yet visited
    open_set = [current_cell]
    heapq.heapify(open_set)

    # Closed set contains floors already visited
    closed_set = []

    while open_set or initialized is False:
        initialized = True
        print('========= Open set exists - Looping =========')
        print('Current cell: ' + str((current_cell.x, current_cell.y)))
        print('Goal_state coords: ' + str(goal_state_coordinates))

        print('Removing current cell from open set')
        heapq.heappop(open_set)

        print('Adding current cell to closed set')
        closed_set.append(current_cell)

        if current_cell.type is CellType.goal_state.value:
            print('Optimal solution found!')
            return reconstruct_path(current_cell)

        # lowest_cost_neighbor = None

        print('Looping through current cell\'s neighbors')
        for neighbor in current_cell.neighbors:
            print('Checking neighbor: ' + str((neighbor.x, neighbor.y)))
            if neighbor in closed_set:
                print('Neighbor already evaluated')
                continue  # Ignore the neighbor which is already evaluated.

            if neighbor in open_set:
                print('Neighbor already in open set')
                continue

            neighbor.update_g_score(current_cell.g_score + neighbor.cost)
            neighbor.previous_cell = current_cell
            heapq.heappush(open_set, neighbor)

            # if lowest_cost_neighbor is None or lowest_cost_neighbor.f_score > neighbor.f_score:
            #     print('Lowest cost neighbor: ' + str((neighbor.x, neighbor.y)))
            #     lowest_cost_neighbor = neighbor
            # else:
            #     print('Better neighbor already found')

        time.sleep(sleeping_time)
        draw(board, current_cell, open_set, closed_set)

        if open_set:
            print('Switching current cell to the one with lowest f_score')
            current_cell = open_set[0]



        # if lowest_cost_neighbor is None and open_set:
        #     print('Can\'t find any neighbor not visited, going back to open set')
        #     current_cell = open_set[-1]  # Switching to last added cell in open set
        # elif lowest_cost_neighbor is not None:
        #     print('The lowest cost neighbor is not discovered before')
        #     previous_cell = current_cell
        #     lowest_cost_neighbor.previous_cell = previous_cell
        #     current_cell = lowest_cost_neighbor
        # else:
        #     print('None lowest_cost_neighbor and empty open set')

    print('No solutions')


def draw(board, current_cell, open_set, closed_set):
    canvas.delete("all")

    for y, row in enumerate(board):
        for x, element in enumerate(row):
            canvas.create_rectangle(cell_width * x, cell_height * y, (cell_width * x) + cell_width,
                                    (cell_height * y) + cell_height,
                                    fill=element.color, outline=element.outline)
            canvas.create_text(cell_width * x + 20, cell_height * y + 20, text='g: ' + str(element.g_score))
            canvas.create_text(cell_width * x + 20, cell_height * y + 40, text='h: ' + str(element.h_score))
            canvas.create_text(cell_width * x + 20, cell_height * y + 60, text='f: ' + str(element.f_score))
            canvas.create_text(cell_width * x + 20, cell_height * y + 80, text=str((x, y)))

    # Open set (light blue), lowest_f_score (cyan)
    for i, cell in enumerate(open_set):
        if i is 0:
            canvas.create_rectangle(cell_width * cell.x,
                                    cell_height * cell.y,
                                    (cell_width * cell.x) + cell_width,
                                    (cell_height * cell.y) + (cell_height / 10),
                                    fill="cyan", outline="black")
        else:
            canvas.create_rectangle(cell_width * cell.x,
                                    cell_height * cell.y,
                                    (cell_width * cell.x) + cell_width,
                                    (cell_height * cell.y) + (cell_height / 10),
                                    fill="blue", outline="black")

    # Closed set (light red)
    for cell in closed_set:
        canvas.create_rectangle(cell_width * cell.x,
                                cell_height * cell.y,
                                (cell_width * cell.x) + cell_width,
                                (cell_height * cell.y) + (cell_height / 10),
                                fill="#ffb2b2", outline="black")

    # Current cell
    canvas.create_oval((cell_width * current_cell.x) + (cell_width / 4),
                       (cell_height * current_cell.y) + (cell_height / 4),
                       (cell_width * current_cell.x) + cell_width - (cell_width / 4),
                       (cell_height * current_cell.y) + cell_height - (cell_height / 4),
                       fill="black")

    canvas.create_rectangle(board_width, 0, canvas_width, canvas_height, fill="#DDDDDD")
    canvas.create_text(board_width + 80, 20, text='Current cell: ' + str((current_cell.x, current_cell.y)))

    if not current_cell.previous_cell:
        canvas.create_text(board_width + 80, 40,
                           text='Previous cell: None')
    else:
        canvas.create_text(board_width + 80, 40,
                           text='Previous cell: ' + str((current_cell.previous_cell.x, current_cell.previous_cell.y)))

    root.update()


root = Tk()
root.title('A* Algorithm')

canvas_width = 1820
canvas_height = 1000
board_width = 1650
board_height = 1000

canvas = Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

board, initial_state_coordinates, goal_state_coordinates = load_board('board-2-4.txt')
board = initialize_board(board, goal_state_coordinates)

cell_height = board_height / len(board)
cell_width = board_width / len(board[0])

start_a_star(0)

root.mainloop()
