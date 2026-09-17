# Grid class file
__author__ = "Gabriel Whangbo-Olvera"
__date__ = "09.17.2026"

# Import statements
import pygame
from Node import Node, GREY

# Grid class - contains cell size, # of rows and columns, and directions
class Grid:
    def __init__(self, rows, cols, cell_size):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.cells = []
        self.directions = [
            (0, -1),  # West
            (-1, -1),  # Northwest
            (-1, 0),  # North
            (-1, 1),  # Northeast
            (0, 1),  # East
            (1, 1),  # Southeast
            (1, 0),  # South
            (1, -1)  # Southwest
        ]

    # Create all the cells to the grid list
    def make_cells(self):
        self.cells = [
            [Node(r, c, self.cell_size) for c in range(self.cols)] for r in range(self.rows)
        ]

    # Add neighbors to each node
    def update_neighbors(self):
        for row in self.cells:
            for node in row:
                node.add_neighbors(self)

    # Reset each node (for playing again)
    def reset(self):
        for row in self.cells:
            for node in row:
                node.reset()

    # Draw the lines defining each cell
    def draw_lines(self, win):
        width = self.cols * self.cell_size
        height = self.rows * self.cell_size
        for i in range(self.rows + 1):
            pygame.draw.line(win, GREY, (0, i * self.cell_size), (width, i * self.cell_size))
        for j in range(self.cols + 1):
            pygame.draw.line(win, GREY, (j * self.cell_size, 0), (j * self.cell_size, height))
