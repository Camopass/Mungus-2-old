import pygame

from math import ceil


class Window:
    def __init__(self, width, height, caption: str = "PyGame Engine", icon=None):
        self.window_surface = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.screen = pygame.surface.Surface((width, height))
        self.target_width, self.target_height = width, height
        self.center_position = [0, 0]
        pygame.display.set_caption(caption)
        if icon is not None:
            pygame.display.set_icon(icon)

    def update_resize(self):
        window_width, window_height = self.window_surface.get_width(), self.window_surface.get_height()
        screen_width, _ = self.screen.get_width(), self.screen.get_height()
        target_width = window_width
        if target_width * 0.666 > window_height:
            target_width = window_height * 1.5
        if target_width is not None:
            target_height = target_width * 0.66666
            resized_screen = pygame.transform.smoothscale(self.screen, (ceil(target_width), ceil(target_height)))
            self.target_width, self.target_height = target_width, target_height

        width = self.window_surface.get_width()
        height = self.window_surface.get_height()
        screen_width = resized_screen.get_width()
        screen_height = resized_screen.get_height()
        center_position = [0, 0]

        a = width - screen_width
        center_position[0] = a / 2
        b = height - screen_height
        center_position[1] = b / 2

        self.center_position = center_position

    def render(self):
        self.window_surface.fill((0, 0, 0))

        resized_screen = pygame.transform.smoothscale(self.screen, (ceil(self.target_width), ceil(self.target_height)))
        self.window_surface.blit(resized_screen, self.center_position)
