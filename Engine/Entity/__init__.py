import typing
import pygame

from PIL import Image, ImageFilter, ImageMath
from math import sin
from io import BytesIO

from Engine import resource_path

from Engine.Maths import Vec2


def pil_to_pygame(image: Image.Image):
    data = image.tobytes()
    return pygame.image.fromstring(data, image.size, image.mode)


class Entity:
    def __init__(self, name: str, id: str, image: pygame.image = None):
        self.name = name
        self.id = id
        self.original_image = image
        self.image = image
        self.xvel = 0
        self.yvel = 0
        self.x = 0
        self.y = 0
        self.y_offset = 0
        self.x_offset = 0
        if image is not None:
            self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
            self.rect.center = (self.x + self.image.get_width() / 2, self.y + self.image.get_height() / 2)
        else:
            self.rect = pygame.Rect(self.x, self.y, 1, 1)

    def update(self):
        if self.xvel != 0:
            self.xvel *= 0.9
        if self.yvel != 0:
            self.yvel *= 0.9
        self.rect.x += self.xvel
        self.rect.y += self.yvel
        self.x, self.y = self.rect.center
        self.rect.center = (self.x + self.image.get_width() / 2, self.y + self.image.get_height() / 2)

    def on_pressed(self, button):
        print("Entity pressed")

    def on_released(self, button):
        pass

    def render(self, screen):
        screen.blit(self.image, (self.x + self.x_offset - 64, self.y + self.y_offset - 64))


class Player(Entity):
    def __init__(self, color: typing.Tuple[int, int, int], *, is_main_player: bool = False):
        super().__init__("Player", "player" if is_main_player else f"player-{str(color)}")
        img = self.get_image(self.get_frame())
        image = pygame.transform.scale(img, (128, 128))
        self.image = image
        self.tint_mask = None
        self.color = color
        self.interactable_objects = []
        self.set_color(color)

    def set_color(self, color):
        frame = self.get_frame()
        tint_mask = self.get_tint_mask(frame)
        tint_mask.fill(color, special_flags=pygame.BLEND_MIN)
        self.tint_mask = pygame.transform.scale(tint_mask, (128, 128))
        self.tint_mask.set_alpha(self.tint_mask.get_alpha() * 0.5)
        img = self.get_image(frame)
        image = pygame.transform.scale(img, (128, 128))
        image.blit(self.tint_mask, (0, 0))
        if self.xvel < 0:
            image = pygame.transform.flip(image, True, False)
        self.image = image
        self.color = color
        return image

    def set_rainbow(self, offset=0):
        time = sin(pygame.time.get_ticks() * 0.001 + offset) / 2 + .5
        color = pygame.color.Color(0)
        c = round(time * 360)
        color.hsla = (c, 100, 50, 100)
        self.set_color((color.r, color.g, color.b))

    def get_frame(self):
        """
        Animation Format:
        0000
        0 - Direction; 0: l-r, 1: d, 2: u
        1 - Animation Set
        2 - Animation Frame
        3 - Frame is tint mask or not

        Animations:
        0 - Idle
        1 - Running
        """
        # Running Animation
        dir = '1' if self.yvel > 0 else '2'
        if abs(self.xvel) >= 0.1 or abs(self.yvel) >= 0.1:
            # round( sin(x / (10 - v) * 0.03) + 1)
            x = pygame.time.get_ticks()
            r = sin(x * .01) + 1
            self.y_offset = (r - 1) * 3
            frame_count = round(r)
            return '{0}1{1}'.format('0' if abs(self.xvel) > abs(self.yvel) else dir, int(frame_count))
        else:
            self.y_offset = 0
            return '{}00'.format('0' if abs(self.xvel) > abs(self.yvel) else dir)

    def get_image(self, frame):
        image = resource_path(f'assets/{frame}0.png')
        return pygame.image.load(image).convert_alpha()

    def get_tint_mask(self, frame):
        tint_mask = resource_path(f'assets/{frame}1.png')
        return pygame.image.load(tint_mask).convert_alpha()

    def update(self):
        if self.xvel != 0:
            self.xvel *= 0.9
        if self.yvel != 0:
            self.yvel *= 0.9
        # Reduce the velocity of the player each frame
        self.rect.x += round(self.xvel)
        self.rect.y += round(self.yvel)
        self.x, self.y = self.rect.center
        # self.rect.center = (self.x, self.y)
        self.set_color(self.color)


class Object(Entity):
    def __init__(self, name: str, id: str, image, *, interactable: bool = False, range: int = None,
                 enable_bloom: bool = False, bloom_image=None, moveable=False):
        super().__init__(name, id, image)
        self.interactable = interactable
        self.activation_range = range
        self.enable_bloom = enable_bloom
        self.moveable = moveable
        if self.enable_bloom:
            self.bloom_image = self.do_bloom(bloom_image)
        else:
            self.bloom_image = None

    def interact(self, player: Player):
        pass

    '''def do_bloom(self, image):
        im = pygame.image.tostring(image, "RGBA", False)
        im = Image.frombuffer("RGBA", self.image.get_size(), im)
        im.show()
        intensity = 10
        buffers = [im]
        for i in range(1, 2):
            buffer = buffers[i - 1].resize((buffers[i - 1].size[0] // 2, buffers[i - 1].size[1] // 2))
            buffers.append(pil_to_pygame(buffer.filter(ImageFilter.GaussianBlur(radius=(intensity - i))).resize(im.size)))
        final = pil_to_pygame(buffers[0])
        for buffer in buffers[1:]:
            final.blit(buffer, (0, 0), special_flags=pygame.BLEND_ADD)
        return final'''

    def do_bloom(self, image):
        image2 = pygame.transform.smoothscale(image, (image.get_width() // 10, image.get_height() // 10))
        image.blit(pygame.transform.smoothscale(image2, (image.get_width(), image.get_height())), (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        image3 = pygame.transform.smoothscale(image, (image.get_width() // 5, image.get_height() // 5))
        image.blit(pygame.transform.smoothscale(image3, (image.get_width(), image.get_height())), (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        return image

    def render(self, screen):
        pos = Vec2(self.x + self.x_offset, self.y + self.y_offset)
        screen.blit(self.image, pos.to_tuple())
        if self.enable_bloom:
            screen.blit(self.bloom_image, pos - pos / Vec2(2, 2))
