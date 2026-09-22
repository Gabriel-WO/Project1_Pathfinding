_Overview_

This is a pathfinding project that uses the A* algorithm to determine the optimal path from two nodes and implements pygame to visually show the process of the computer checking neighbors and adding them to the open list and closed list. I used an 8-directional grid (north, northwest, southwest, south, etc.) where diagonal movements are worth √2 and vertical/horizontal movements are worth 1. The program allows the user to set how many columns and rows they want, where the start and end nodes are, which nodes should be obstacles, and which heuristic they'd like to test (the choices are Manhattan, Euclidean, and Diagonal). At the end, the program will show the final optimal path as determined by the A* algorithm (using the chosen heuristic) highlighted in yellow as well as the amount of nodes explored (i.e. efficiency) and the total cost of the path. 

_Files_
- main.py = main file with A* algorithm and user interface
- Node.py = node class that houses node variables (color, is_start, etc.)
- Grid.py = grid class that contains the directions and cells in the grid

_To use_
- Run main.py
- Enter the amount of rows and columns
- Left-click to select start, end, and obstacle nodes
- Click space to run and choose the heuristic
- Click C to reset the heuristic, R to reset the entire grid
- The cost of the path, which heuristic used, and the number of nodes explored will be printed below (unless no path is found, in which case no path found is displayed)
- ESC exits the entire program

_Heuristic choices_

Given that this project uses an 8-directional grid, the optimal heuristic will be the diagonal one. The Manhattan distance heuristic is not admissible because it will overestimate the distance of diagonals (i.e. it will count the legs of the triangle rather than the cost of the hypotenuse). The Euclidean heuristic, while admissible, is still not ideal because it only evaluates the "as the crow flies" distance which is not actually how the algorithm can move along the grid. 

For testing, I recommend setting up your start, end, and obstacle nodes and running different heuristic options (clicking C will ensure only the path is reset, not the obstacles and nodes you've chosen) and comparing their relative efficiency and cost. Although the Manhattan heuristic is almost always more efficient (less nodes expanded), it is not guaranteed to find the optimal path (which can be checked by choosing either of the other two, both of which are admissible and are guaranteed to find the optimal path). The diagonal heuristic will almost always be more efficient than the Euclidean heuristic because the Euclidean heuristic overestimates when it has to zigzag, while the diagonal heuristic takes into account the cost of diagonal movements.   
