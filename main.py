import sys as sus
from math import ceil

import pygame

from Engine.Entity.Player import Player
from Engine.EntityManager import EntityManager
from Engine.Window import Window

pygame.init()

icon = pygame.image.load('Mungus.ico')

window = Window(1200, 800, "Mungus, the Sequel", icon)

player = Player((255, 0, 0), is_main_player=True)

player2 = Player((0, 255, 0))
player2.xvel = 10

player3 = Player((0, 0, 255))
player3.yvel = -10

entityManager = EntityManager(window.screen, player, player3, player2)

clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 10)

background = pygame.image.load('assets/sprites/background/Development/Testing-1.png').convert()
background = pygame.transform.scale(background, (1200, 800))

use_gamepad = True

global use_gamepad
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
use_gamepad = True if len(joysticks) > 0 else False


def do_input(controlled_player):
    if use_gamepad:
        x = joysticks[0].get_axis(0)
        y = joysticks[0].get_axis(1)
        if abs(x) > 0.1:
            controlled_player.xvel += x
        if abs(y) > 0.1:
            controlled_player.yvel += y
    else:
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            controlled_player.xvel -= 1
        if key[pygame.K_d]:
            controlled_player.xvel += 1
        if key[pygame.K_w]:
            controlled_player.yvel -= 1
        if key[pygame.K_s]:
            controlled_player.yvel += 1


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sus.exit()
        if event.type == pygame.VIDEORESIZE:
            window.window_surface = pygame.display.set_mode(size=(event.w, event.h), flags=pygame.RESIZABLE)
            window.update_resize()  # Set the scaling of the window screen

        '''
        JoyButton:
            A: 0
            B: 1
            X: 2
            Y: 3
            LB: 4
            RB: 5
            SHARE: 6
            MENU: 7
            LJ: 8
            RJ: 9
        JoyAxisMotion:
            
        '''

    if pygame.mouse.get_focused():
        window.screen.fill((0, 0, 0))

        # Do the rainbow calculation for the rainbow player.
        player3.set_rainbow()

        window.screen.blit(background, (0, 0))

        fps = round(clock.get_fps())
        window.screen.blit(font.render(f'FPS: {fps}', False, [255, 255, 255]), (10, 10))

        do_input(player)
        entityManager.render()

        window.render()

        pygame.display.update()

        clock.tick(60)
