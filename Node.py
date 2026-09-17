# Node class file
__author__ = "Gabriel Whangbo-Olvera"
__date__ = "09.17.2026"

# Import statements
import pygame

# Colors
WHITE = (255, 255, 255)      # default/unvisited
BLACK = (0, 0, 0)            # obstacle
GREY = (200, 200, 200)       # grid lines
GREEN = (0, 200, 0)          # open set
RED = (220, 60, 60)          # closed set
ORANGE = (255, 165, 0)       # start
TURQUOISE = (64, 224, 208)   # end
YELLOW = (255, 215, 0)       # final path

# Node class - contains the size of the node, whether it's an obstacle,
# neighbors, start vs end distinction, and color depending on its status
class Node:
    # Initialize
    def __init__(self, row, col, cell_size):
        self.row = row
        self.col = col
        self.cell_size = cell_size
        self.x = col * cell_size
        self.y = row * cell_size
        self.color = WHITE
        self.is_obstacle = False
        self.is_start = False
        self.is_end = False
        self.neighbors = []

    # Populate neighbors
    def add_neighbors(self, grid):
        self.neighbors = []
        for dr, dc in grid.directions:
            new_row = self.row + dr
            new_col = self.col + dc
            if 0 <= new_row < grid.rows and 0 <= new_col < grid.cols:
                if not grid.cells[new_row][new_col].is_obstacle:
                    self.neighbors.append(grid.cells[new_row][new_col])

    # Resets the node
    def reset(self):
        self.color = WHITE
        self.is_obstacle = False
        self.is_start = False
        self.is_end = False

    # Sets the status to obstacle
    def make_obstacle(self):
        self.is_obstacle = True
        self.color = BLACK

    # Sets the status to start node
    def make_start(self):
        self.is_start = True
        self.color = ORANGE

    # Sets the status to end node
    def make_end(self):
        self.is_end = True
        self.color = TURQUOISE

    # Set the status to in the open list
    def make_open(self):
        if not self.is_start and not self.is_end:
            self.color = GREEN

    # Set the status to in the closed list
    def make_closed(self):
        if not self.is_start and not self.is_end:
            self.color = RED

    # Change the color (called if it's in the reconstructed final path)
    def make_path(self):
        if not self.is_start and not self.is_end:
            self.color = YELLOW

    # Draws the node
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.cell_size, self.cell_size))
