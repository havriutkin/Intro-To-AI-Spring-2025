"""
    Lab 1: Game of Life
    Author: Vladyslav Havriutkin
    Date: 14-02-2025
"""

import pygame as pg
import numpy as np

class Cell:
    def __init__(self, x: int, y: int, display: pg.Surface, size=10):
        self.position = np.array([x, y])
        self.alive = False
        self.display = display
        self._size = size

    def draw(self):
        if self.alive:
            pg.draw.rect(self.display, (255, 0, 0), 
                         (self.position[0] * self._size, self.position[1] * self._size, 
                          self._size, self._size))
    
class GameOfLife:
    def __init__(self, width: int, height: int, size=10, config: list[Cell] = None):
        self.width = width
        self.height = height
        self.size = size
        self.display = pg.display.set_mode((width * size, height * size))
        self.font = pg.font.Font(None, 36)
        self._paused = True
        
        self.grid: list[list[Cell]] = []
        if config is None:
            self.grid = [[Cell(x, y, self.display) for x in range(width)] for y in range(height)]
        else:
            if len(config) != height or len(config[0]) != width:
                raise ValueError("Invalid starting configuration.")
            
            self.grid = config

    def set_config(self, config: list[Cell]):
        if len(config) != self.height or len(config[0]) != self.width:
            raise ValueError("Invalid starting configuration.")
        self.grid = config

    def update(self):
        # If paused, do not update the grid
        if self._paused:
            return

        new_states = [[False for _ in range(self.width)] for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                neighbors = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i == 0 and j == 0:
                            continue
                        if 0 <= y + i < self.height and 0 <= x + j < self.width:
                            neighbors += self.grid[y + i][x + j].alive

                if self.grid[y][x].alive:
                    new_states[y][x] = not (neighbors < 2 or neighbors > 3)
                else:
                    new_states[y][x] = (neighbors == 3)

        # Update the grid with the new states
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x].alive = new_states[y][x]

    def draw(self):
        # Draw grid
        for i in range(self.width):
            pg.draw.line(self.display, 
                         (0, 0, 0), 
                         (i * self.size, 0), 
                         (i * self.size, self.height * self.size))
        for i in range(self.height):
            pg.draw.line(self.display, 
                         (0, 0, 0), 
                         (0, i * self.size), 
                         (self.width * self.size, i * self.size))
            
        # Draw cells
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x].draw()

        # Display paused/running text
        if self._paused:
            text = self.font.render("Paused", True, (255, 0, 0))
        else:
            text = self.font.render("Running", True, (0, 255, 0))
        pg.draw.rect(self.display, (255, 255, 255), (0, 0, 100, 30))
        self.display.blit(text, (0, 0))

    def run(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                if event.type == pg.KEYDOWN:
                    # Pause simulation on space press
                    if event.key == pg.K_SPACE:
                        self._paused = not self._paused

                    # Clear grid on 'c' press
                    if event.key == pg.K_c:
                        for row in self.grid:
                            for cell in row:
                                cell.alive = False
                
                # On mouse click, toggle cell state if paused
                if event.type == pg.MOUSEBUTTONDOWN and self._paused:
                    x, y = pg.mouse.get_pos()
                    x, y = x // self.size, y // self.size
                    self.grid[y][x].alive = not self.grid[y][x].alive   # Toggle cell state

            self.display.fill((255, 255, 255))
            self.update()
            self.draw()
            pg.display.update()
            pg.time.delay(100)

class Configurations:
    def __init__(self, width, height, display: pg.Surface):
        self._width = width
        self._height = height
        self.display = display

    def get_block(self):
        block = [[Cell(x, y, self.display) for x in range(self._width)] for y in range(self._height)]

        block[self._height//2][self._width//2].alive = True 
        block[self._height//2][self._width//2 + 1].alive = True
        block[self._height//2 + 1][self._width//2].alive = True
        block[self._height//2 + 1][self._width//2 + 1].alive = True
        
        return block
    
    def get_blinker(self):
        blinker = [[Cell(x, y, self.display) for x in range(self._width)] for y in range(self._height)]
        blinker[self._height//2][self._width//2].alive = True
        blinker[self._height//2][self._width//2 + 1].alive = True

        return blinker

if __name__ == "__main__":
    pg.init()
    game = GameOfLife(50, 50)
    configurations = Configurations(width=50, height=50, display=game.display)

    game.run()