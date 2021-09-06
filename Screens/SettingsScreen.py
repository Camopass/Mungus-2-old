import pygame

from Engine.Screen import Screen


class SettingsScreen(Screen):
    def __init__(self, window):
        super().__init__(window, 50, 50, 150, 700)
