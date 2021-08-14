import typing
import pygame

from math import sin
from Engine.Entity.Entity import Entity


class Player(Entity):
    def __init__(self, color: typing.Tuple[int, int, int], *, is_main_player: bool = False):
        super().__init__("Player", "player" if is_main_player else f"player-{str(color)}")
        img = self.get_image(self.get_frame())
        image = pygame.transform.scale(img, (128, 128))
        self.image = image
        self.rect = image.get_rect()
        self.tint_mask = None
        self.color = color
        self.set_color(color)

    def set_color(self, color):
        frame = self.get_frame()
        tint_mask = self.get_tint_mask(frame)
        tint_mask.fill(color, special_flags=pygame.BLEND_MIN)
        self.tint_mask = pygame.transform.scale(tint_mask, (128, 128))
        self.tint_mask.set_alpha(self.tint_mask.get_alpha() * 0.5)
        img = self.get_image(frame)
        image = pygame.transform.scale(img, (128, 128))
        image.blit(self.tint_mask, (0, 0))
        if self.xvel < 0:
            image = pygame.transform.flip(image, True, False)
        self.image = image
        self.color = color
        return image

    def set_rainbow(self, offset=0):
        time = sin(pygame.time.get_ticks() * (0.001) + offset) / 2 + .5
        color = pygame.color.Color(0)
        c = round(time * 360)
        color.hsla = (c, 100, 50, 100)
        self.set_color((color.r, color.g, color.b))

    def get_frame(self):
        """
        Animation Format:
        000
        1 - Animation Set
        2 - Animation Frame
        3 - Frame is tint mask or not

        Animations:
        0 - Idle
        1 - Running
        """
        # Runnning Animation
        if abs(self.xvel) >= 0.1 or abs(self.yvel) >= 0.1:
            # round( sin(x / (10 - v) * 0.03) + 1)
            x = pygame.time.get_ticks()
            r = sin(x * .01) + 1
            self.y_offset = (r - 1) * 3
            frame_count = round(r)
            return f'1{int(frame_count)}'
        else:
            self.y_offset = 0
            return '00'

    def get_image(self, frame):
        image = f'assets/sprites/player/{frame}0.png'
        return pygame.image.load(image).convert_alpha()

    def get_tint_mask(self, frame):
        tint_mask = f'assets/sprites/player/{frame}1.png'
        return pygame.image.load(tint_mask).convert_alpha()

    def update(self):
        if self.xvel != 0:
            self.xvel *= 0.9
        if self.yvel != 0:
            self.yvel *= 0.9
        self.rect.x += round(self.xvel)
        self.rect.y += round(self.yvel)
        self.x, self.y = self.rect.center
        self.rect.center = (self.x, self.y)
        self.set_color(self.color)
