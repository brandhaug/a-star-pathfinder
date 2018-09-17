from enum import Enum


class CellType(Enum):
    floor = '.'
    obstacle = '#'
    initial_state = 'A'
    goal_state = 'B'
    water = 'w'
    mountain = 'm'
    forest = 'f'
    grass = 'g'
    road = 'r'
