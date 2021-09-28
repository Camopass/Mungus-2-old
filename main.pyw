import sys as sus
import pygame
import os

from Engine.Button import Button
from Engine.Entity import Player, Object
from Engine.EntityManager import EntityManager
from Engine.ObjectManager import ObjectManager
from Engine.Window import Window
from Screens.DebugScreen import DebugScreen
from Screens.MainUI import MainUI
from Screens.SettingsScreen import SettingsScreen


# Change CWD to Mungus2/ instead of SYS32
with open("%s/Mungus2 Launch Info [DO NOT DELETE RENAME OR MOVE].txt" % os.path.join(os.environ["USERPROFILE"], "Desktop"), 'r') as f:
    f.seek(0)
    data = f.read()
    if not os.getcwd() == r"E:\PyOpenGLTest":  # We do a little testing
        os.chdir(data)

# TODO: Move Mungus2 Launch Info to Program Files not desktop you moron

pygame.init()  # CRINGE

pygame.joystick.init()  # MORE CRINGE

# TODO: Make this less cringe

icon = pygame.image.load('Mungus.ico')
window = Window(1600, 960, "Mungus, the Sequel", icon)

# player
player = Player((255, 0, 0), is_main_player=True)
player2 = Player((0, 255, 0))
player2.xvel = 10
player3 = Player((0, 0, 255))
player3.yvel = 10

entity_manager = EntityManager(window.screen, player, player3, player2)
window.entity_manager = entity_manager

# Make a lamp (it glows)
lamp_image = pygame.image.load('assets/floor_light_1.png').convert_alpha()
lamp_bloom = pygame.image.load('assets/floor_light_1_emission.png').convert_alpha()
light = Object('Floor Lamp', 'floor_lamp_1', lamp_image, enable_bloom=True, bloom_image=lamp_bloom, z_override=-1)
light.x = 600
light.y = 400
light.yvel, light.yvel = (0, 0)

# We gotta do a little managing
object_manager = ObjectManager(window.screen, light)

clock = pygame.time.Clock()

font = pygame.font.SysFont("Ursus.ttf", 20)  # Get it? Sus?

background = pygame.image.load('assets/TileSlate_01.png').convert()  # CRINGE!!!!!!111 HARD CODED BACKGROUND? MORE LIKE BAD!

settins_screen = SettingsScreen(window)

# SETTINGS BUTTON for STUPID PEOPLE who can't press ESCAPE except I have not implemented that yet # TODO: Fix this issue
settings_icon = pygame.image.load('assets/Settings.png').convert_alpha()
settings_icon = pygame.transform.scale2x(settings_icon)
settings = Button(1150, 2, 'settings', settings_icon, label='Settings', func=settins_screen.toggle_open)

main_ui = MainUI(window, 5, 674, 256, 128, player)

global use_gamepad  # Global Variables? CRINGE!
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
use_gamepad = True if len(joysticks) > 0 else False  # TODO: Make this stupid script better

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


# TODO: Barf Emoji
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
                sus.exit()  # Get it? Sus?
            if event.type == pygame.VIDEORESIZE:  # We do a little resizing
                window.window_surface = pygame.display.set_mode(size=(event.w, event.h), flags=pygame.RESIZABLE)
                window.update_resize()  # Set the scaling of the window screen
            if event.type == pygame.MOUSEBUTTONDOWN:  # Mouse moment
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
            if event.type == pygame.KEYDOWN:  # Fullscreen by pressing F11
                if event.key == pygame.K_F11:
                    window.windowed() if window.is_fullscreen else window.fullscreen()

        if pygame.mouse.get_focused():
            window.screen.fill((0, 0, 0))

            # Do the rainbow calculation for the rainbow player.
            player3.set_rainbow()

            window.screen.blit(background, (0, 0))  # Draw the stupid background you dumbass computer

            fps = round(clock.get_fps())

            do_input(player)  # Barf emoji

            # We do a little rendering
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
