# Main file for Pathfinding project
__author__ = "Gabriel Whangbo-Olvera"
__date__ = "09.17.2026"

# AI use:
# Flint:
# Claude:

# Import statements
import math
import heapq
import sys
import pygame
from Node import Node
from Grid import Grid

# GLOBAL VARIABLES
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
# Window settings
WINDOW_SIZE = 600
ANIMATION_DELAY = 20

# Pathfinding class - prompts user to select start, end, and obstacle nodes on an 8-directional grid
# and finds the optimal path using the A* algorithm with a diagonal heuristic
class Pathfinding:
    def __init__(self, grid):
        self.grid = grid
        self.open_list = []
        self.open_set = set()
        self.closed_list = set()
        self.came_from = {} # Parent node
        self.g_score = {} # Cost from start

    # Diagonal heuristic
    def diagonal_cost(self, node, end_node):
        dr = abs(end_node.row - node.row) # x-axis difference
        dc = abs(end_node.col - node.col) # y-axis difference
        D = 1 # Vertical/horizontal distance
        D2 = math.sqrt(2) # Diagonal distance
        return D * (dr + dc) + (D2 - 2 * D) * min(dr, dc)

    # Manhattan heuristic
    def manhattan_cost(self, node, end_node):
        dr = abs(end_node.row - node.row) # x-axis difference
        dc = abs(end_node.col - node.col) # y-axis difference
        D = 1 # Vertical/horizontal distance
        return D * (dr + dc)

    # Euclidean heuristic
    def euclidean_cost(self, node, end_node):
        dr = abs(end_node.row - node.row) # x-axis difference
        dc = abs(end_node.col - node.col) # y-axis difference
        D = 1
        return D * ((dr * dr) + (dc * dc))

    # Calculates the step cost
    def g_cost(self, node, neighbor):
        dr = abs(node.row - neighbor.row)
        dc = abs(node.col - neighbor.col)
        return math.sqrt(2) if dr == 1 and dc == 1 else 1

    # Reconstructs the path back to the start node
    def reconstruct_path(self, current_node):
        path = [current_node]
        while current_node in self.came_from:
            current_node = self.came_from[current_node]
            path.append(current_node)
        path.reverse()
        return path

    # A* search algorithm
    def a_star(self, grid, start_node, end_node, heuristic, draw_callback=None):
        # Initialize the open and closed lists and add start node (with g = 0 to start)
        self.open_list = []
        self.open_set = set()
        self.closed_list = set()
        self.came_from = {}
        self.g_score = {start_node: 0}
        counter = 0

        # Algorithm will change depending on what heuristic the user wants to use
        heuristics_map = {
            1: self.manhattan_cost,
            2: self.euclidean_cost,
            3: self.diagonal_cost,
        }

        start_f = heuristics_map[heuristic](start_node, end_node)

        heapq.heappush(self.open_list, (start_f, counter, start_node))
        self.open_set.add(start_node)

        # Loop until the open list is empty
        while self.open_list:
            # Allow quitting while animating
            if draw_callback:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

            # Pop node with lowest f(n) and call it current
            _, _, current = heapq.heappop(self.open_list)

            # Stale heap entry - skip it
            if current not in self.open_set:
                continue
            self.open_set.remove(current)

            # If current == goal, reconstruct path via the parent map and end the search
            if current == end_node:
                path = self.reconstruct_path(current)
                for node in path:
                    node.make_path()
                if draw_callback:
                    draw_callback()
                    pygame.time.delay(ANIMATION_DELAY)
                return path

            # Add current to closed list
            self.closed_list.add(current)
            if current is not start_node: # Update the color
                current.make_closed()

            # Checks the f(n) of neighbors
            for neighbor in current.neighbors:
                # If neighbor in closed list, skip it
                if neighbor in self.closed_list:
                    continue
                # Calculate temporary g(n) = g(current) + step cost
                temp_g = self.g_score[current] + self.g_cost(current, neighbor)
                # If temporary g(n) is less than g(neighbor), update g(n) and parent
                if temp_g < self.g_score.get(neighbor, math.inf):
                    self.came_from[neighbor] = current
                    self.g_score[neighbor] = temp_g
                    f_score = temp_g + heuristics_map[heuristic](neighbor, end_node)
                    counter += 1
                    heapq.heappush(self.open_list, (f_score, counter, neighbor))
                    # Add to the open list
                    self.open_set.add(neighbor)
                    if neighbor is not end_node: # Update the color
                        neighbor.make_open()

            if draw_callback:
                draw_callback()
                pygame.time.delay(ANIMATION_DELAY)

        # Open list didn't find end node --> no path exists
        return None

# Determines grid size based on user input
def get_grid_size():
    # Prompt user
    def ask(prompt, default):
        raw = input(f"{prompt}").strip()
        if not raw:
            return default
        try:
            value = int(raw)
            return value if 2 <= value <= 100 else default
        except ValueError:
            return default

    # Prompt for rows
    rows = ask("Enter rows: ", 20)
    # Prompt for columns
    cols = ask("Enter columns: ", 20)

    return rows, cols

# Determine which heuristic to use based on user input
def get_heuristic():
    def ask(prompt, default):
        raw = input(f"{prompt}").strip()
        if not raw:
            return default
        try:
            value = int(raw)
            return value if 1 <= value <= 3 else default
        except ValueError:
            return default

    # Prompt for heuristic
    heuristic = ask("Choose a heuristic: \n 1: Manhattan\n 2: Euclidean\n 3: Diagonal \n", 3)
    return heuristic

# Gets start node from user
def get_clicked_pos(pos, cell_size):
    x, y = pos
    col = x // cell_size
    row = y // cell_size
    return row, col

# Draws the nodes
def draw(win, grid):
    win.fill(WHITE)
    for row in grid.cells:
        for node in row:
            node.draw(win)
    grid.draw_lines(win)
    pygame.display.update()

# Main - creates the visual display, prompts the user, and runs the algorithm
def main():
    print("Set up the grid (default is 20 x 20)")
    rows, cols = get_grid_size()
    heuristic = get_heuristic()
    cell_size = WINDOW_SIZE // max(rows, cols)
    width = cols * cell_size
    height = rows * cell_size

    pygame.init()
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("A* Pathfinding")

    grid = Grid(rows, cols, cell_size)
    grid.make_cells()

    start_node = None
    end_node = None
    running = True
    algorithm_done = False

    print("Left-click: place start, then end, then obstacles.")
    print("Right-click: erase a cell.")
    print("SPACE: run the animation once start and end are set.")
    print("R: reset the grid. ESC: quit.")

    while running:
        draw(win, grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and not algorithm_done:
                row, col = get_clicked_pos(pygame.mouse.get_pos(), cell_size)
                if not (0 <= row < rows and 0 <= col < cols):
                    continue
                node = grid.cells[row][col]

                if event.button == 1:  # left click
                    if not start_node and node is not end_node:
                        start_node = node
                        node.make_start()
                    elif not end_node and node is not start_node:
                        end_node = node
                        node.make_end()
                    elif node is not start_node and node is not end_node:
                        node.make_obstacle()

                elif event.button == 3:  # right click - erase
                    if node is start_node:
                        start_node = None
                    if node is end_node:
                        end_node = None
                    node.reset()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_r:
                    grid.reset()
                    start_node = None
                    end_node = None
                    algorithm_done = False

                elif event.key == pygame.K_SPACE and not algorithm_done:
                    if start_node and end_node:
                        grid.update_neighbors()  # pick up any obstacles placed after creation
                        pathfinder = Pathfinding(grid)
                        path = pathfinder.a_star(
                            grid, start_node, end_node, heuristic,
                            draw_callback=lambda: draw(win, grid)
                        )
                        algorithm_done = True
                        if not path:
                            print("No path exists.")
                        else:
                            print(f"Path found, length {len(path)}.")

    pygame.quit()


if __name__ == "__main__":
    main()
