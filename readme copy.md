# Robot Navigation Search Algorithms

This project implements several tree-based search algorithms for solving the **Robot Navigation Problem** on a grid. The robot starts at a given position on the grid and must navigate to a goal position, avoiding walls. The grid, starting position, goal(s), and walls are provided in a data file.

## Algorithms Implemented

### 1. **Depth-First Search (DFS)**
DFS is an uninformed search algorithm that explores as far as possible along each branch before backtracking. It uses a **stack** (LIFO) to keep track of the nodes to be expanded next. In the context of the grid:
- **Path**: DFS may not find the shortest path.
- **Memory**: DFS has low memory usage as it stores only the current path.
- **Expansion**: DFS will explore deep before considering other options.

### 2. **Breadth-First Search (BFS)**
BFS is an uninformed search algorithm that explores all neighbors of a node before expanding deeper. It uses a **queue** (FIFO) to manage the expansion order. In the context of the grid:
- **Path**: BFS guarantees the shortest path (in terms of number of moves).
- **Memory**: BFS may use more memory compared to DFS as it stores all nodes at the current depth.
- **Expansion**: BFS expands all nodes at the current depth before going deeper.

### 3. **Greedy Best-First Search (GBFS)**
GBFS is an informed search algorithm that prioritizes nodes based on a heuristic, specifically the **Manhattan distance** from the current node to the nearest goal. It uses a **priority queue** to expand the node closest to the goal first.
- **Path**: GBFS does not guarantee the shortest path.
- **Memory**: GBFS uses less memory compared to BFS but depends on the heuristic function.
- **Expansion**: GBFS expands nodes based on how "close" they appear to be to the goal according to the heuristic.

### 4. **A* Search**
A* is an informed search algorithm that combines the cost to reach the current node (**g**) and the estimated cost to reach the goal from the current node (**h**). It guarantees the optimal solution if the heuristic is admissible. A* uses a **priority queue**.
- **Path**: A* guarantees the shortest path.
- **Memory**: A* can use more memory because it explores more nodes.
- **Expansion**: A* expands nodes based on the total estimated cost `f(n) = g(n) + h(n)`.

### 5. **Iterative Deepening Search (IDS) - CUS1**
IDS is an uninformed search algorithm that combines DFS and BFS by iterating DFS with increasing depth limits. It ensures that the search is both memory-efficient (like DFS) and finds the shortest path (like BFS).
- **Path**: IDS guarantees the shortest path (in terms of number of moves).
- **Memory**: IDS has low memory usage.
- **Expansion**: IDS expands nodes like DFS, but re-explores nodes at each new depth limit.

### 6. **Uniform Cost Search (UCS) - CUS2**
UCS is an uninformed search algorithm that expands nodes based on their path cost from the start node. It uses a **priority queue** to expand the lowest-cost node first.
- **Path**: UCS guarantees the shortest path (in terms of cumulative cost).
- **Memory**: UCS may use more memory due to storing all explored nodes.
- **Expansion**: UCS expands nodes based on their cumulative path cost `g(n)`.

## File Format

The input data file must follow this specific format:

1. **First Line**: `[N, M]`  
   - The number of rows `N` and columns `M` for the grid, enclosed in square brackets.
   - Example: `[5,11]` represents a grid with 5 rows and 11 columns.

2. **Second Line**: `(x1, y1)`  
   - The starting coordinate of the robot (agent), enclosed in parentheses.
   - Example: `(0,1)` means the robot starts at row `0` and column `1` of the grid.

3. **Third Line**: `(xG1, yG1) | (xG2, yG2)`  
   - The goal positions separated by `|`. The robot must reach one of the goal states.
   - Example: `(7,0) | (10,3)` means the robot has two possible goal states at these coordinates.

4. **Subsequent Lines**: `(x,y,w,h)`  
   - These describe the walls. Each wall is represented by its top-left corner coordinates `(x,y)`, its width `w`, and height `h`.
   - Example: `(2,0,2,2)` describes a wall starting at position `(2,0)` that is 2 cells wide and 2 cells high.

## How to Run

The program can be run from the command line with the following syntax:

```bash
python sol.py <algorithm> <datafile>
