import pygame

from DebugConfig import debug_config
from Engine.Button import Button


class EntityManager:
    def __init__(self, screen, *entities):
        self.screen = screen
        self.entities = list(entities)

    def render(self):
        self.entities.sort(key=lambda e: e.y)
        size = self.screen.get_size()
        for entity in self.entities:
            entity.update()

            if size[1] > entity.y > -30 and -30 < entity.x < size[0]:
                entity.render(self.screen)
                from main import settins_screen
                if settins_screen.open:
                    pygame.draw.rect(self.screen, (255, 255, 255), entity.rect, 3 if type(entity) != Button else 0)
                    pygame.draw.circle(self.screen, (255, 255, 255), (entity.x, entity.y), 3)
