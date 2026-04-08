from constants import *
from tile import Tile

class Game:
    def __init__(self):
        self.tiles = []
        self.create_tiles()
    
    def create_tiles(self):
        tot_width = GRID_COLUMNS * TILE_SIZE + (GRID_COLUMNS - 1) * TILE_PADDING
        tot_height = GRID_ROWS * TILE_SIZE + (GRID_ROWS - 1) * TILE_PADDING

        start_x = (SCREEN_WIDTH - tot_width) // 2
        start_y = (SCREEN_HEIGHT - tot_height) // 2

        for row in range(GRID_ROWS):
            for col in range(GRID_COLUMNS):
                index = row * GRID_COLUMNS + col
                x = start_x + col * (TILE_SIZE + TILE_PADDING)
                y = start_y + row * (TILE_SIZE + TILE_PADDING)

                self.tiles.append(Tile(x, y, TILE_SIZE, TILE_COLORS[index]))
    
    def draw(self, screen):
        for tile in self.tiles:
            tile.draw(screen)