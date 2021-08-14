import ctypes
import sys as sus
import pygame

from Engine.Entity.Player import Player
from Engine.EntityManager import EntityManager
from Engine.Window import Window

pygame.init()

icon = pygame.image.load('assets/sprites/player/000.png')

window = Window(1200, 800, "Mungus, the Sequel", icon)

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(u'camopass.mungustwo.prealpha')

player = Player((255, 0, 0), is_main_player=True)

player2 = Player((0, 255, 0))
player2.xvel = 10

player3 = Player((0, 0, 255))
player3.yvel = -10

entityManager = EntityManager(window.screen, player, player3, player2)

clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 10)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sus.exit()

    window.screen.fill((10, 25, 60))

    if pygame.mouse.get_focused():

        # Controls System; TODO: Move this to an entity method ya dum dum
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            player.xvel -= 1
        if key[pygame.K_d]:
            player.xvel += 1
        if key[pygame.K_w]:
            player.yvel -= 1
        if key[pygame.K_s]:
            player.yvel += 1

        player3.set_rainbow()

        background = pygame.image.load('assets/sprites/background/Development/Testing-1.png').convert()
        background = pygame.transform.scale(background, (1200, 800))
        window.screen.blit(background, (0, 0))

        window.screen.blit(font.render(str(clock.get_fps()), False, [255, 255, 255]), (10, 10))

        entityManager.render()
        pygame.display.flip()
        pygame.display.update()

        clock.tick(60)
