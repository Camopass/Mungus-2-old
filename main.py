import sys as sus
import pygame
import ctypes
import itertools

from Engine.Entity.Entity import Entity
from Engine.Entity.Player import Player
from Engine.Window import Window
from Engine.EntityManager import EntityManager
from math import sin, pi
from Engine.Maths.color import hsv_to_rgb


pygame.init()

icon = pygame.image.load('assets/sprites/player/player.png')

window = Window(800, 800, "Mungus, the Sequel", icon)

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(u'camopass.mungustwo.prealpha')

player = Player((255, 0, 0), is_main_player=True)

player2 = Player((0, 255, 0))
player2.xvel = 10

player3 = Player((0, 0, 255))
player3.yvel = -10

entityManager = EntityManager(window.screen, player, player3, player2)

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sus.exit()

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

    window.screen.fill((10, 25, 60))
    entityManager.render()
    pygame.display.flip()
    pygame.display.update()

    clock.tick(60)
