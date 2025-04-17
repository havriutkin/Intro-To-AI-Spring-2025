# Maze Generation & Solving Report

This report summarizes a Python program that **generates** a perfect maze, **solves** it via the shortest path, and **animates** both processes using Pygame.

---

## 1. Maze Generation (Recursive Backtracker)

- **Algorithm**: Depth‑First Search (DFS) with an explicit stack  
- **Data structures**:  
    - `walls[(x,y)]`: a 4‑entry list `[top, right, bottom, left]`  
    - `visited`: a set of carved cells  
- **Steps**:  
    1. Push the **entrance** cell onto `stack` and mark visited  
    2. While `stack` not empty:  
        - Look at the top cell `(cx,cy)`  
        - Randomly shuffle its four neighbors `(dx,dy)`  
        - For the first unvisited neighbor `(nx,ny)`:  
            - Knock down the current’s wall `w` and neighbor’s opposite wall `ow`  
            - Mark `(nx,ny)` visited, push it on `stack`, and **yield** one frame  
            - **break** to continue carving from `(nx,ny)` (true DFS)  
        - If none unvisited, pop `stack` (backtrack) and **yield** one frame  
    3. After all cells are carved, remove the outer walls at entrance (green) and exit (red)

---

## 2. Maze Solving (Breadth‑First Search)

- **Algorithm**: BFS for the shortest path in an unweighted grid  
- **Data structures**:  
    - `queue`: FIFO of cells to explore  
    - `came_from`: map each cell to its parent for path reconstruction  
- **Steps**:  
    1. Enqueue the **entrance**, mark `came_from[start] = None`  
    2. Dequeue `current`, **yield** `('visit', current)` to animate exploration  
    3. For each accessible neighbor (no wall), if unseen:  
        - Record `came_from[neighbor] = current`, enqueue it  
    4. Stop when `current == exit`; reconstruct path by backtracking through `came_from`  
    5. **Yield** `('path', cell)` for each cell in the final shortest path

---

## 3. Animation Implementation

- **Generators & `yield`**:  
    - `generate_gen()` and `solve_gen()` each pause after every carve, backtrack, visit, or path step  
- **Pygame loop**:  
    1. Drive the active generator with `next()`  
    2. Draw the current state:  
        - Walls via `pygame.draw.line`  
        - Generation‑visited cells (light blue)  
        - Solver‑visited cells (light pink)  
        - Solution path (red squares)  
        - Entrance (green) & exit (red) fills  
    3. `pygame.display.flip()` + `clock.tick(FPS)` regulate the frame rate

---

## 4. Animation
![Maze Animation](./Generation_And_Solving_Animation.gif)


## 5. How to Run

1. **Clone** this repository  
   ```bash
   git clone https://github.com/yourusername/maze-animator.git
   cd maze-animator
2. Install **dependencies**
   ```bash
   python3 -m venv venv
   source venv/bin/activate       # macOS/Linux
   .\venv\Scripts\activate        # Windows
   pip install pygame
3. **Run** the program
   ```bash
   python main.py

