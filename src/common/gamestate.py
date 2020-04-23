from enum import Enum, auto
import numpy as np
from .cell import Cell


class Direction(Enum):
    UP_LEFT = auto()
    UP = auto()
    UP_RIGHT = auto()
    LEFT = auto()
    RIGHT = auto()
    DOWN_LEFT = auto
    DOWN = auto()
    DOWN_RIGHT = auto()

UP_DIRS = [Direction.UP, Direction.UP_LEFT, Direction.UP_RIGHT]
DOWN_DIRS = [Direction.DOWN, Direction.DOWN_LEFT, Direction.DOWN_RIGHT]
LEFT_DIRS = [Direction.LEFT, Direction.DOWN_LEFT, Direction.UP_LEFT]
RIGHT_DIRS = [Direction.RIGHT, Direction.DOWN_RIGHT, Direction.UP_RIGHT]


class GameState:
    def __init__(self, size_y, size_x, rules=([3], [2, 3])):
        self.x = size_x
        self.y = size_y
        self.rules = rules  # defaults to conway's rules, Born3Survive23.

        self.grid = []
        for ii in range(0, self.y):
            self.grid.append([None]*self.x)

    def get_cell_neighbor(self, y, x, direction):
        if direction in UP_DIRS:
            y = (y-1) % self.y
        elif direction in DOWN_DIRS:
            y = (y+1) % self.y

        if direction in RIGHT_DIRS:
            x = (x+1) % self.x
        elif direction in LEFT_DIRS:
            x = (x-1) % self.x

        return self.grid[y][x]

    def get_cell_neighbors(self, y, x):
        return tuple(
            self.get_cell_neighbor(y, x, dir) for dir in Direction
        )

    def get_live_neighbor_count(self, y, x):
        neighbors = self.get_cell_neighbors(y, x)
        return len([x for x in neighbors if x is not None])

    def __getitem__(self, yx_tuple):
        y, x = yx_tuple
        return self.grid[y][x]

    def __setitem__(self, yx_tuple, value):
        y, x = yx_tuple
        self.grid[y][x] = value

    def step(self):
        """Run a step in conways game of life"""
        new_state = GameState(self.y, self.x)

        for y in range(0, self.y):
            for x in range(0, self.x):
                count = self.get_live_neighbor_count(y, x)

                if count in self.rules[0] and self[y, x] is None:
                    # New cell is born
                    new_state[y, x] = Cell.birth_from_parents([cell for cell in self.get_cell_neighbors(y, x)
                                                               if cell is not None])
                elif count in self.rules[1]:
                    # Cell survives
                    new_state[y, x] = self[y, x]
                else:
                    # Cell dies
                    new_state[y, x] = None

        return new_state

    def apply_subboard(self, y, x, subboard):
        new_state = GameState.copy_gamestate(self)

        for ii in range(0, subboard.y):
            for jj in range(0, subboard.x):
                new_state[y+ii, x+jj] = subboard[ii,jj]

        return  new_state

    def get_numpy_array(self):
        new_array = []
        for ii in range(0, self.y):
            new_array.append([-1]*self.x)
            for jj in range(0, self.x):
                if self[ii, jj] is not None:
                    new_array[ii][jj] = self[ii, jj].team_id
                else:
                    new_array[ii][jj] = 0
        np_array = np.array(new_array)
        return np_array

    @staticmethod
    def gamestate_from_numpy_array(array):
        y = array.shape[0]
        x = array.shape[1]
        state = GameState(y, x)

        for ii in range(0, y):
            for jj in range(0, x):
                if array[ii, jj] != 0:
                    state[ii, jj] = Cell(team_id=array[ii, jj])

    @staticmethod
    def copy_gamestate(gamestate: 'GameState'):
        new_state = GameState(gamestate.y, gamestate.x)
        for ii in range(0, gamestate.y):
            for jj in range(0, gamestate.x):
                new_state[ii, jj] = gamestate[ii,jj]

        return new_state