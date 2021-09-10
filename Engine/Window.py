import pygame

from math import ceil
from Engine.Maths import map_range


class Window:
    def __init__(self, width, height, caption: str = "PyGame Engine", icon=None):
        self.window_surface = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.screen = pygame.surface.Surface((width, height))
        self.target_width, self.target_height = width, height
        self.resized_rect = self.screen.get_rect()
        self.center_position = [0, 0]
        self.entity_manager = None
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

        self.resized_rect = pygame.rect.Rect(*center_position, target_width, target_height)

        self.center_position = center_position

    def get_mouse_pos(self):
        x, y = pygame.mouse.get_pos()
        return self.get_transforms(x, y)

    # Transform a Pos from the window surface to the screen surface
    def get_transforms(self, x, y):
        if not self.resized_rect.collidepoint(x, y):
            return 0, 0
        window = self.window_surface.get_rect()
        m_x, m_y = map_range(x, self.center_position[0], window.width - self.center_position[0], 0, self.resized_rect.width), map_range(y, self.center_position[1], window.height - self.center_position[1], 0, self.resized_rect.height)
        m_x, m_y = map_range(m_x, 0, self.resized_rect.width, 0, 1200), map_range(m_y, 0, self.resized_rect.height, 0, 800)

        return m_x, m_y

    def render(self):
        self.window_surface.fill((0, 0, 0))
        resized_screen = pygame.transform.smoothscale(self.screen, (ceil(self.target_width), ceil(self.target_height)))
        self.window_surface.blit(resized_screen, self.center_position)

    def mouse_up(self, button):
        if self.entity_manager is not None:
            for entity in self.entity_manager.entities:
                if entity.rect.collidepoint(self.get_transforms(*pygame.mouse.get_pos())):
                    entity.on_pressed(button)

    def mouse_down(self, button):
        if self.entity_manager is not None:
            for entity in self.entity_manager.entities:
                if entity.rect.collidepoint(self.get_transforms(*pygame.mouse.get_pos())):
                    entity.on_released(button)
