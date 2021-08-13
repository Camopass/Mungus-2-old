import typing
from math import sin

import pygame

from Engine.Entity.Entity import Entity


class Player(Entity):
    def __init__(self, color: typing.Tuple[int, int, int], *, is_main_player: bool = False):
        img = pygame.image.load(self.get_frame()).convert_alpha()
        image = pygame.transform.scale(img, (128, 128))
        super().__init__("Player", "player" if is_main_player else f"player-{str(color)}", image)
        self.tint_mask = None
        self.set_color(color)

    def set_color(self, color):
        tint_mask = pygame.image.load('assets/sprites/player/tint_mask.png').convert_alpha()
        tint_mask.fill(color, special_flags=pygame.BLEND_MIN)
        self.tint_mask = pygame.transform.scale(tint_mask, (128, 128))
        self.tint_mask.set_alpha(self.tint_mask.get_alpha() * 0.5)
        img = pygame.image.load(self.get_frame()).convert_alpha()
        image = pygame.transform.scale(img, (128, 128))
        image.blit(self.tint_mask, (0, 0))
        self.image = image

    def set_rainbow(self, offset=0):
        time = sin(pygame.time.get_ticks() * 0.001 + offset) / 2 + .5
        color = pygame.color.Color(0)
        c = round(time * 360)
        color.hsla = (c, 100, 50, 100)
        self.set_color((color.r, color.g, color.b))

    def get_frame(self):
        if self.xvel >= 0.2 or self.yvel >= 0.2:
            t = sin(pygame.time.get_ticks() * .001) / 2. + .5
        else:
            res = 'assets/sprites/player/player'
