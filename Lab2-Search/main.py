"""
    Lab 2: Search 
    Author: Vladyslav Havriutkin
    Date: 17-03-2025
"""

import random
import pygame
import sys
from collections import deque

CELL_SIZE            = 20
WALL_COLOR           = (30, 30, 30)
BG_COLOR             = (240, 240, 240)
GEN_VISITED_COLOR    = (180, 220, 255)
SOL_VISITED_COLOR    = (255, 180, 180)
PATH_COLOR           = (200, 30, 30)
ENTRANCE_COLOR       = (  0, 200,   0)
EXIT_COLOR           = (200,   0,   0)
FPS                  = 60


class Maze:
    """ This class stores information about maze and generates  maze step by step using DFS """
    def __init__(self, width: int, height: int, entrance: tuple[int,int], exit: tuple[int,int]):
        self.width    = width
        self.height   = height
        self.entrance = entrance
        self.exit     = exit
        self.visited = set() # keep track of visited cells

        # walls[(x,y)] = [top, right, bottom, left] - keeps track of whether wall is present
        self.walls = {
            (x, y): [True, True, True, True]
            for y in range(height) for x in range(width)
        }
        

    def generate_gen(self):
        """ Uses DFS to generate maze. It is a generator function, yields each step. """
        # DFS
        stack = [self.entrance]
        self.visited = {self.entrance}

        while stack:
            cx, cy = stack[-1]

            # Each neighbor consists of: 
            #   dx - shift by x from the current cell to the neighbor
            #   dy - shift by y from the current cell to the neighbor
            #   w  - the index of the wall on the CURRENT cell adjacent to the neighbor cell
            #   ow - the index of the wall on the NEIGHBOR cell adjacent to teh current cell 
            neighbors = [
                (0, -1, 0, 2),
                (1,  0, 1, 3),
                (0,  1, 2, 0),
                (-1, 0, 3, 1),
            ]
            random.shuffle(neighbors) # randomly pick a neighbor

            carved = False
            for dx, dy, w, ow in neighbors:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in self.visited:
                    # if in bounds and have not visited this cell yet - knock the wall down!
                    self.walls[(cx, cy)][w] = False
                    self.walls[(nx, ny)][ow] = False
                    self.visited.add((nx, ny))
                    stack.append((nx, ny))
                    carved = True
                    yield  # one step of carving
                    break  # update the current cell

            if not carved:
                # Means all cells around have been visited, or out of bounce => go back 
                stack.pop()
                yield  # backtracking step

        yield

class MazeSolver:
    """ Solves a maze using BFS step by step """
    def __init__(self, maze: Maze):
        self.maze   = maze
        self.width  = maze.width
        self.height = maze.height

    def solve_gen(self):
        start = self.maze.entrance
        goal  = self.maze.exit
        queue = deque([start])
        came_from = {start: None} # to keep the path for visual

        # BFS
        while queue:
            current = queue.popleft()

            # yield a “visit” event so the visualizer can color it
            yield ('visit', current)

            # Stop if reached the exit
            if current == goal:
                break

            cx, cy = current
            for dx, dy, w_idx in [(0,-1,0),(1,0,1),(0,1,2),(-1,0,3)]:
                # Visit each neighbor 
                if not self.maze.walls[(cx, cy)][w_idx]:
                    # If can get to this neighbor (i.e. there is no wall)
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height and (nx,ny) not in came_from:
                        came_from[(nx,ny)] = current
                        queue.append((nx,ny))

        # reconstruct path
        path = []
        node = goal
        while node is not None:
            path.append(node)
            node = came_from[node]
        path.reverse()

        for cell in path:
            # yield "coloring path" event
            yield ('path', cell)

def visualize(maze: Maze, solve_gen):
    """ Visualize generation and solving in pygame """
    pygame.init()
    screen = pygame.display.set_mode((maze.width * CELL_SIZE, maze.height * CELL_SIZE))
    clock  = pygame.time.Clock()

    gen_phase = True
    solver_phase = False
    solver_visited = set()
    solution_path  = []

    gen_steps = maze.generate_gen()
    sol_steps = solve_gen

    def draw():
        screen.fill(BG_COLOR)
        # fill generated-visited cells
        for x, y in maze.visited:
            rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GEN_VISITED_COLOR, rect)

        # fill solver-visited cells
        for x, y in solver_visited:
            rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, SOL_VISITED_COLOR, rect)

        # fill solution path
        for x, y in solution_path:
            rect = pygame.Rect(
                x*CELL_SIZE + CELL_SIZE//4,
                y*CELL_SIZE + CELL_SIZE//4,
                CELL_SIZE//2,
                CELL_SIZE//2
            )
            pygame.draw.rect(screen, PATH_COLOR, rect)

        # draw walls
        for (x, y), walls in maze.walls.items():
            sx, sy = x * CELL_SIZE, y * CELL_SIZE
            if walls[0]:
                pygame.draw.line(screen, WALL_COLOR, (sx, sy), (sx+CELL_SIZE, sy))
            if walls[1]:
                pygame.draw.line(screen, WALL_COLOR, (sx+CELL_SIZE, sy), (sx+CELL_SIZE, sy+CELL_SIZE))
            if walls[2]:
                pygame.draw.line(screen, WALL_COLOR, (sx, sy+CELL_SIZE), (sx+CELL_SIZE, sy+CELL_SIZE))
            if walls[3]:
                pygame.draw.line(screen, WALL_COLOR, (sx, sy), (sx, sy+CELL_SIZE))

        # highlight entrance & exit
        ex, ey = maze.entrance
        rect = pygame.Rect(ex*CELL_SIZE, ey*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, ENTRANCE_COLOR, rect)
        tx, ty = maze.exit
        rect = pygame.Rect(tx*CELL_SIZE, ty*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, EXIT_COLOR, rect)

        pygame.display.flip()

    # Game loop
    running = True
    while running:
        clock.tick(FPS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        if gen_phase:
            try:
                next(gen_steps)
            except StopIteration:
                gen_phase    = False
                solver_phase = True
            draw()
            continue

        if solver_phase:
            try:
                tag, cell = next(sol_steps)
                if tag == 'visit':
                    solver_visited.add(cell)
                else:  # 'path'
                    solution_path.append(cell)
            except StopIteration:
                solver_phase = False
            draw()
            continue

        # after both phases are done, just display
        draw()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    W, H = 50, 30
    entrance = (0, random.randrange(H))
    exit     = (W-1, random.randrange(H))

    maze   = Maze(W, H, entrance, exit)
    solver = MazeSolver(maze)

    visualize(maze, solver.solve_gen())
