import pygame
import random
from constants import *
from tile import Tile

tot_width = GRID_COLUMNS * TILE_SIZE + (GRID_COLUMNS - 1) * TILE_PADDING
tot_height = GRID_ROWS * TILE_SIZE + (GRID_ROWS - 1) * TILE_PADDING

class Game:
    def __init__(self):
        self.tiles = []
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.pattern = []
        self.state = "idle"
        self.current_round = 1
        self.show_index = 0
        self.show_timer = 0
        self.plyr_progress = 0
        self.create_tiles()
        self.create_button()
    
    def reset_tiles(self):
        for tile in self.tiles:
            tile.color = WHITE

    def flash_current(self):
        tile_index = self.pattern[self.show_index] - 1
        self.tiles[tile_index].color = self.tiles[tile_index].active_color
        self.show_timer = pygame.time.get_ticks()

    def start_game(self):
        self.pattern = random.choices(range(1, 5), k = 50)
        self.current_round = 1
        self.show_index = 0
        self.plyr_progress = 0
        self.reset_tiles()
        self.state = "showing"
        self.flash_current()

    def update(self):
        if self.state != "showing":
            return
        
        elapsed = pygame.time.get_ticks() - self.show_timer

        if elapsed < FLASH_ON:
            pass
        elif elapsed < FLASH_ON + FLASH_OFF:
            self.reset_tiles()
        else:
            self.show_index += 1
            if self.show_index >= self.current_round:
                self.state = "waiting"
                self.plyr_progress = 0
            else:
                self.flash_current()

    def create_tiles(self):
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
        pygame.draw.rect(screen, BUTTON_COLOR, self.button_rect)
        label = self.font.render("START", True, BUTTON_TEXT_COLOR)
        screen.blit(label, label.get_rect(center=self.button_rect.center))

    def handle_click(self, mouse_pos):
        if self.button_rect.collidepoint(mouse_pos):
            if self.state == "idle":
                self.start_game()
            return

        if self.state != "waiting":
            return

        for i, tile in enumerate(self.tiles):
            if tile.is_clicked(mouse_pos):
                expected = self.pattern[self.plyr_progress] - 1
                if i == expected:
                    self.plyr_progress += 1
                    if self.plyr_progress >= self.current_round:
                        self.current_round += 1
                        if self.current_round > 50:
                            self.state = "idle"
                        else:
                            self.show_index = 0
                            self.reset_tiles()
                            self.state = "showing"
                            self.flash_current()
                else:
                    self.reset_tiles()
                    self.state = "idle"
                break

    def create_button(self):
        btn_x = (SCREEN_WIDTH - BUTTON_WIDTH) // 2
        grid_top = (SCREEN_HEIGHT - tot_height) // 2
        btn_y = grid_top - BUTTON_HEIGHT - 20
        self.button_rect = pygame.Rect(btn_x, btn_y, BUTTON_WIDTH, BUTTON_HEIGHT)