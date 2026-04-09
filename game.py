import pygame
import random
from constants import *
from tile import Tile

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
        self.click_tile_index = None
        self.click_correct = False
        self.click_timer = 0
        self.delay_timer = 0
        self.start_img = pygame.image.load(START_BTN_IMG).convert_alpha()
        self.quit_img  = pygame.image.load(QUIT_BTN_IMG).convert_alpha()
        self.click_sfx = pygame.mixer.Sound(BTN_CLICK_SFX)
        self.light_sfx = pygame.mixer.Sound(LIGHT_ON_SFX)
        self.create_tiles()
        self.create_button()
    
    def reset_tiles(self):
        for tile in self.tiles:
            tile.lit = False
            tile.pressed = False

    def flash_current(self):
        tile_index = self.pattern[self.show_index] - 1
        self.tiles[tile_index].lit = True
        self.light_sfx.play()
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
        if self.state == "showing":
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

        elif self.state == "click_flash":
            elapsed = pygame.time.get_ticks() - self.click_timer
            if elapsed >= CLICK_FLASH:
                self.tiles[self.click_tile_index].lit = False
                self.tiles[self.click_tile_index].pressed = False
                if self.click_correct:
                    self.plyr_progress += 1
                    if self.plyr_progress >= self.current_round:
                        self.current_round += 1
                        if self.current_round > 50:
                            self.state = "idle"
                        else:
                            self.delay_timer = pygame.time.get_ticks()
                            self.state = "delay"
                    else:
                        self.state = "waiting"
                else:
                    self.reset_tiles()
                    self.state = "idle"

        elif self.state == "delay":
            elapsed = pygame.time.get_ticks() - self.delay_timer
            if elapsed >= ROUND_DELAY:
                self.show_index = 0
                self.reset_tiles()
                self.state = "showing"
                self.flash_current()

    def create_tiles(self):
        img_off    = pygame.image.load(TILE_OFF_IMG).convert_alpha()
        light_w, light_h = img_off.get_size()

        sample_btn = pygame.image.load(TILE_BTN_IMGS[0]).convert_alpha()
        btn_w, btn_h = sample_btn.get_size()

        col_w = max(light_w, btn_w)
        total_width  = GRID_COLUMNS * col_w + (GRID_COLUMNS - 1) * TILE_PADDING
        total_height = light_h + TILE_LIGHT_GAP + btn_h

        start_x = (SCREEN_WIDTH  - total_width)  // 2
        start_y = (SCREEN_HEIGHT - total_height) // 2


        self.grid_top    = start_y
        self.grid_bottom = start_y + total_height

        for col in range(GRID_COLUMNS):
            cx = start_x + col * (col_w + TILE_PADDING)

            light_x = cx + (col_w - light_w) // 2
            light_rect = pygame.Rect(light_x, start_y, light_w, light_h)

            btn_x  = cx + (col_w - btn_w) // 2
            btn_y  = start_y + light_h + TILE_LIGHT_GAP
            btn_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)

            img_on      = pygame.image.load(TILE_ON_IMGS[col]).convert_alpha()
            img_btn     = pygame.image.load(TILE_BTN_IMGS[col]).convert_alpha()
            img_pressed = pygame.image.load(TILE_BTN_PRESSED_IMGS[col]).convert_alpha()
            self.tiles.append(Tile(light_rect, btn_rect, img_off, img_on, img_btn, img_pressed))

    def draw(self, screen):
        for tile in self.tiles:
            tile.draw(screen)
        screen.blit(self.start_img, self.button_rect)
        screen.blit(self.quit_img, self.quit_rect)

    def handle_click(self, mouse_pos):
        if self.quit_rect.collidepoint(mouse_pos):
            self.click_sfx.play()
            pygame.quit()
            raise SystemExit

        if self.button_rect.collidepoint(mouse_pos):
            if self.state == "idle":
                self.click_sfx.play()
                self.start_game()
            return

        if self.state != "waiting":
            return

        for i, tile in enumerate(self.tiles):
            if tile.is_clicked(mouse_pos):
                self.click_sfx.play()
                expected = self.pattern[self.plyr_progress] - 1
                tile.lit = True
                tile.pressed = True
                self.click_tile_index = i
                self.click_correct = (i == expected)
                self.click_timer = pygame.time.get_ticks()
                self.state = "click_flash"
                break

    def create_button(self):
        sw, sh = self.start_img.get_size()
        start_x = (SCREEN_WIDTH - sw) // 2
        start_y = (self.grid_top - sh) // 2
        self.button_rect = pygame.Rect(start_x, start_y, sw, sh)

        qw, qh = self.quit_img.get_size()
        quit_x = (SCREEN_WIDTH - qw) // 2
        quit_y = self.grid_bottom + (SCREEN_HEIGHT - self.grid_bottom - qh) // 2
        self.quit_rect = pygame.Rect(quit_x, quit_y, qw, qh)