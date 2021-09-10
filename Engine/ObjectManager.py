import pygame

from Engine.Maths import Vec2, pythagoras


class ObjectManager:
    def __init__(self, screen, *objects):
        self.screen = screen
        self.objects = list(objects)

    def render(self):
        self.objects.sort(key=lambda x: x.y)
        size = self.screen.get_size()

        from main import player
        player.interactable_objects = []

        for object in self.objects:
            if object.interactable:
                if pythagoras(Vec2(object.x, object.y), Vec2(player.x, player.y)) <= object.activation_range:
                    player.interactable_objects.append(object)
            if size[1] > object.y > -30 and -30 < object.x < size[0]:
                object.render(self.screen)
