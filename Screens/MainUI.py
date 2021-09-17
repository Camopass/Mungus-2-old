import pygame

from Engine.Entity import Player
from Engine.Screen import Screen
from Engine.Window import Window


class MainUI(Screen):
    def __init__(self, window: Window, x: float, y: float, width: float, height: float, player: Player):
        super().__init__(window, x, y, width, height)
        self.player = player
        self.main_image = pygame.transform.scale2x(pygame.image.load('assets/HealthBar.png').convert_alpha())
        self.mask = pygame.transform.scale2x(pygame.image.load('assets/HealthBarMask.png').convert_alpha())

    def render(self):
        self.window.screen.blit(self.main_image, (self.x, self.y))
        width = int(self.mask.get_width() * (self.player.health / self.player.max_health))
        print(width)
        self.window.screen.blit(self.mask, (self.x, self.y), (0, 0, width, self.mask.get_height()))
