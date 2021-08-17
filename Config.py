import pygame
import json


class Controls:
    def __init__(self, json):
        self.gamepad = json['Enable GamePad?']


class VideoSettings:
    def __init__(self, json):
        self.particles = json['Enable Particles?']
        self.show_fps = json['Show FPS?']


class Config:
    def __init__(self):
        with open('config.json', 'r+') as fr:
            f = fr.read()
            if len(f) == 0:
                fr.write('{"controls": {"Enable GamePad?": 0}, {"Video Settings": {"Enable Particles?": 1, "Show FPS '
                         'counter?": 0}}}')
            jsn = json.loads(fr.read())
            self.controls = Controls(jsn['controls'])
            self.VideoSettings = VideoSettings(jsn['Video Settings'])
