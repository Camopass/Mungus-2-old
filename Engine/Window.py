import pygame


class Window:
    def __init__(self, width, height, caption: str = "PyGame Engine", icon=None):
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
        if icon is not None:
            pygame.display.set_icon(icon)
