import pygame


class EntityManager:
    def __init__(self, screen, *entities):
        self.screen = screen
        self.entities = entities

    def render(self):
        for entity in self.entities:
            entity.update()
            entity.render(self.screen)
