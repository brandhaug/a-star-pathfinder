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


def draw_path(path, open_set, closed_set):
    for cell in path:
        canvas.create_text(cell_width * cell.x + (cell_width / 2),
                           cell_height * cell.y + (cell_height / 2),
                           font=("Helvetica", 18),
                           text="⬤")

    canvas.create_text(board_width + 80, 80,
                       text='Total f score: ' + str(path[0].f_score))
    canvas.create_text(board_width + 80, 100,
                       text='Path length: ' + str(len(path)))

    canvas.create_text(board_width + 80, 140,
                       text='Open set length: ' + str(len(open_set)))

    canvas.create_text(board_width + 80, 160,
                       text='Closed set length: ' + str(len(closed_set)))


def reconstruct_path(current_cell, open_set, closed_set):
    cell = current_cell
    path = []

    while cell:
        path.append(cell)
        cell = cell.previous_cell

    draw_path(path, open_set, closed_set)
    return path


def start_a_star(sleeping_time):
    current_cell = board[initial_state_coordinates[1]][initial_state_coordinates[0]]
    current_cell.initialize(board, goal_state_coordinates, current_cell.g_score)

    open_set = [current_cell]  # Open set contains floors not yet visited
    heapq.heapify(open_set)  # Making open set a heap prioritized by f_score (see __lt__ method in Cell)

    closed_set = []  # Closed set contains floors already visited

    while open_set:
        print('========= Open set exists - Looping =========')
        print('Current cell: ' + str((current_cell.x, current_cell.y)))

        print('Removing current cell from open set')
        heapq.heappop(open_set)

        print('Adding current cell to closed set')
        closed_set.append(current_cell)

        time.sleep(sleeping_time)
        render(board, current_cell, open_set, closed_set)

        if current_cell.type is CellType.goal_state.value:
            print('Optimal solution found!')
            return reconstruct_path(current_cell, open_set, closed_set)

        print('Looping through current cell\'s neighbors')
        for neighbor in current_cell.neighbors:
            print('Checking neighbor: ' + str((neighbor.x, neighbor.y)))
            if neighbor in closed_set:
                print('Neighbor already evaluated')
                continue
            elif neighbor in open_set:
                print('Neighbor already in open set')
                continue

            neighbor.initialize(board, goal_state_coordinates, current_cell.g_score)
            neighbor.previous_cell = current_cell
            heapq.heappush(open_set, neighbor)

        if open_set:
            print('Switching current cell to the one with lowest f_score')
            current_cell = open_set[0]
        else:
            print('No solutions')


def start_breadth_first(sleeping_time):
    current_cell = board[initial_state_coordinates[1]][initial_state_coordinates[0]]
    current_cell.initialize(board, goal_state_coordinates, current_cell.g_score)

    open_set = [current_cell]  # Open set contains floors not yet visited

    closed_set = []  # Closed set contains floors already visited

    while open_set:
        print('========= Open set exists - Looping =========')
        print('Current cell: ' + str((current_cell.x, current_cell.y)))

        print('Removing current cell from open set')
        open_set.remove(current_cell)

        print('Adding current cell to closed set')
        closed_set.append(current_cell)

        time.sleep(sleeping_time)
        render(board, current_cell, open_set, closed_set)

        if current_cell.type is CellType.goal_state.value:
            print('Solution found!')
            return reconstruct_path(current_cell, open_set, closed_set)

        print('Looping through current cell\'s neighbors')
        for neighbor in current_cell.neighbors:
            print('Checking neighbor: ' + str((neighbor.x, neighbor.y)))
            if neighbor in closed_set:
                print('Neighbor already evaluated')
                continue
            elif neighbor in open_set:
                print('Neighbor already in open set')
                continue

            neighbor.initialize(board, goal_state_coordinates, current_cell.g_score)
            neighbor.previous_cell = current_cell
            open_set.append(neighbor)

        if open_set:
            print('Switching current cell to the one with lowest f_score')
            current_cell = open_set[0]
        else:
            print('No solutions')


def render(board, current_cell, open_set, closed_set):
    canvas.delete("all")

    for y, row in enumerate(board):
        for x, element in enumerate(row):
            canvas.create_rectangle(cell_width * x, cell_height * y, (cell_width * x) + cell_width,
                                    (cell_height * y) + cell_height,
                                    fill=element.color, outline=element.outline)
            # if element.f_score > 0:
            #     canvas.create_text(cell_width * x + 20, cell_height * y + 20, text='g: ' + str(element.g_score))
            #     canvas.create_text(cell_width * x + 20, cell_height * y + 40, text='h: ' + str(element.h_score))
            #     canvas.create_text(cell_width * x + 20, cell_height * y + 60, text='f: ' + str(element.f_score))
            #     canvas.create_text(cell_width * x + 20, cell_height * y + 80, text=str((x, y)))

    # Closed set (light red)
    for cell in closed_set:
        canvas.create_text(cell_width * cell.x + (cell_width / 2),
                           cell_height * cell.y + (cell_height / 2),
                           font=("Helvetica", 16),
                           text="✕")

    for cell in open_set:
        canvas.create_text(cell_width * cell.x + (cell_width / 2),
                           cell_height * cell.y + (cell_height / 2),
                           font=("Helvetica", 16),
                           text="★")
    # Current cell
    canvas.create_text(cell_width * current_cell.x + (cell_width / 2),
                       cell_height * current_cell.y + (cell_height / 2),
                       font=("Helvetica", 18),
                       text="⬤")

    canvas.create_rectangle(board_width, 0, canvas_width, canvas_height, fill="#DDDDDD")
    canvas.create_text(board_width + 80, 20, text='Current cell: ' + str((current_cell.x, current_cell.y)))

    if not current_cell.previous_cell:
        canvas.create_text(board_width + 80, 40,
                           text='Previous cell: None')
    else:
        canvas.create_text(board_width + 80, 40,
                           text='Previous cell: ' + str(
                               (current_cell.previous_cell.x, current_cell.previous_cell.y)))

    root.update()


board, initial_state_coordinates, goal_state_coordinates = load_board('board-2-4.txt')

root = Tk()
root.title('A* Algorithm')

canvas_width = 1820
board_width = canvas_width - 170
board_height = 1000

cell_height = board_height / len(board)
cell_width = board_width / len(board[0])

if cell_height > cell_width:
    cell_height = cell_width
else:
    cell_width = cell_height

canvas_height = cell_height * len(board)

canvas = Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

start_a_star(0)
# start_breadth_first(0)

root.mainloop()
