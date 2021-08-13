import pygame


class Entity:
    def __init__(self, name: str, id: str, image: pygame.image):
        self.name = name
        self.id = id
        self.original_image = image
        self.image = image
        self.rect = image.get_rect()
        self.xvel = 0
        self.yvel = 0
        self.x = 0
        self.y = 0
        self.rotation = 0
        self.scale = 1

    def update(self):
        if self.xvel != 0:
            self.xvel *= 0.9
        if self.yvel != 0:
            self.yvel *= 0.9
        self.rect.x += self.xvel
        self.rect.y += self.yvel
        self.x, self.y = self.rect.center
        self.rect.center = (self.x, self.y)

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))
