import pygame
from constants import *

class Tile:
    def __init__(self, light_rect, btn_rect, img_off, img_on, img_btn, img_btn_pressed):
        self.light_rect = light_rect
        self.btn_rect   = btn_rect
        self.img_off = img_off
        self.img_on  = img_on
        self.img_btn = img_btn
        self.img_btn_pressed = img_btn_pressed
        self.lit     = False
        self.pressed = False

    def draw(self, screen):
        light = self.img_on if self.lit else self.img_off
        screen.blit(light, self.light_rect)
        btn = self.img_btn_pressed if self.pressed else self.img_btn
        screen.blit(btn, self.btn_rect)

    def is_clicked(self, mouse_pos):
        return self.btn_rect.collidepoint(mouse_pos)
