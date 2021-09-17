import sys as sus
import pygame

from Engine import resource_path
from Engine.Button import Button
from Engine.Entity import Player, Object
from Engine.EntityManager import EntityManager
from Engine.ObjectManager import ObjectManager
from Engine.Window import Window
from Screens.DebugScreen import DebugScreen
from Screens.MainUI import MainUI
from Screens.SettingsScreen import SettingsScreen

pygame.init()

icon = pygame.image.load('Mungus.ico')
window = Window(1200, 800, "Mungus, the Sequel", icon)

player = Player((255, 0, 0), is_main_player=True)
player2 = Player((0, 255, 0))
player2.xvel = 10
player3 = Player((0, 0, 255))
player3.yvel = 10

entity_manager = EntityManager(window.screen, player, player3, player2)
window.entity_manager = entity_manager

lamp_image = pygame.image.load('assets/floor_light_1.png').convert_alpha()
lamp_bloom = pygame.image.load('assets/floor_light_1_emission.png').convert_alpha()
light = Object('Floor Lamp', 'floor_lamp_1', lamp_image, enable_bloom=True, bloom_image=lamp_bloom, z_override=-1)
light.x = 600
light.y = 400
light.yvel, light.yvel = (0, 0)

object_manager = ObjectManager(window.screen, light)

clock = pygame.time.Clock()

font = pygame.font.SysFont("Ursus.ttf", 20)

background = pygame.image.load(resource_path('assets/TileSlate_01.png')).convert()

settins_screen = SettingsScreen(window)

settings_icon = pygame.image.load(resource_path('assets/Settings.png')).convert_alpha()
settings_icon = pygame.transform.scale2x(settings_icon)
settings = Button(1150, 2, 'settings', settings_icon, label='Settings', func=settins_screen.toggle_open)

main_ui = MainUI(window, 5, 674, 256, 128, player)

global use_gamepad
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
use_gamepad = True if len(joysticks) > 0 else False

debug_screen = DebugScreen(window, 900, 10, 275, 700, 'Debug Screen', entity_manager)

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
'''


def do_input(controlled_player):
    if use_gamepad:
        x = joysticks[0].get_axis(0)
        y = joysticks[0].get_axis(1)
        if abs(x) > 0.1:
            controlled_player.xvel += x
        if abs(y) > 0.1:
            controlled_player.yvel += y
        if joysticks[0].get_button(6):
            debug_screen.toggle_open()
        if joysticks[0].get_button(7):
            settins_screen.toggle_open()
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
        if key[pygame.K_b]:
            debug_screen.toggle_open()


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sus.exit()
            if event.type == pygame.VIDEORESIZE:
                window.window_surface = pygame.display.set_mode(size=(event.w, event.h), flags=pygame.RESIZABLE)
                window.update_resize()  # Set the scaling of the window screen
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_RIGHT:
                    window.right_click = True
                if event.button == pygame.BUTTON_LEFT:
                    window.left_click = True
                window.mouse_down(event.button)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_RIGHT:
                    window.right_click = False
                if event.button == pygame.BUTTON_LEFT:
                    window.left_click = False
                window.mouse_up(event.button)

        if pygame.mouse.get_focused():
            window.screen.fill((0, 0, 0))

            # Do the rainbow calculation for the rainbow player.
            player3.set_rainbow()

            window.screen.blit(background, (0, 0))

            fps = round(clock.get_fps())

            do_input(player)

            entity_manager.update()
            object_manager.update()
            window.render_managers(entity_manager, object_manager)
            settins_screen.render()
            debug_screen.render()
            main_ui.render()
            window.screen.blit(font.render(f'FPS: {fps}', False, [255, 255, 255]), (10, 10))

            window.render()

            pygame.display.update()

            clock.tick(60)


if __name__ == '__main__':
    main()
