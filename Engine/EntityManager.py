import pygame


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
