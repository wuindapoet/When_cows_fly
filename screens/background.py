from kivy.config import Config
Config.set('input', 'wm_touch', 'mouse,disable')
Config.set('input', 'wm_pen', 'mouse,disable')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Rectangle, InstructionGroup
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from kivy.graphics.texture import Texture
from screens.animated_sprites import get_scaled_value
from kivy.resources import resource_find

import math

Window.size = (800, 600)

def get_objects_background_speed():
    return get_scaled_value(0.45)

GROUND_PATH = "assets/images/backgrounds/background_1/ground.png"
BASE_PATHS = [f"assets/images/backgrounds/background_{i}" for i in range(1, 7)]

class ParallaxLayer:
    def __init__(self, sources, speed):
        self.sources = sources
        self.speed = speed
        self.offset = 0
        self.rects = []
        self.total_width = 1
        self.group = InstructionGroup()

        textures = []
        for src in self.sources:
            path = resource_find(src)
            if not path:
                raise FileNotFoundError(f"Image not found: {src}")
            textures.append(CoreImage(path).texture)

        textures.append(textures[2])
        self.texture = self.concat_textures(textures)
        self.img_width = self.texture.width
        self.img_height = self.texture.height

    def resize(self):
        scale = Window.height / self.img_height
        self.scaled_width = self.img_width * scale
        self.scaled_height = Window.height
        self.total_width = self.texture.width * scale

        if not self.rects:
            return
        for i, rect in enumerate(self.rects):
            rect.size = (self.scaled_width, self.scaled_height)
            rect.pos = (i * self.scaled_width, 0)

    def concat_textures(self, textures):
        total_width = sum(t.width for t in textures)
        max_height = max(t.height for t in textures)
        result = Texture.create(size=(total_width, max_height))

        x_offset = 0
        for tex in textures:
            result.blit_buffer(tex.pixels, colorfmt='rgba', bufferfmt='ubyte',
                               size=(tex.width, tex.height), pos=(x_offset, 0))
            x_offset += tex.width

        result.flip_vertical()
        return result

    def init_graphics(self, canvas, y=0, height=Window.height):
        from kivy.graphics import Color, Rectangle
        self.group.clear()
        self.rects = []

        scale = Window.height / self.img_height
        scaled_width = self.img_width * scale
        scaled_height = Window.height
        self.scaled_width = scaled_width

        self.group.add(Color(1, 1, 1, 1))
        num_tiles = math.ceil(Window.width / scaled_width) + 3
        for i in range(num_tiles):
            rect = Rectangle(texture=self.texture, pos=(i * scaled_width, y),
                             size=(scaled_width, scaled_height))
            self.rects.append(rect)
            self.group.add(rect)

        if self.group in canvas.children:
            canvas.remove(self.group)
        canvas.add(self.group)

        self.total_width = self.scaled_width * len(self.rects)

    def move(self, scroll):
        scroll_offset = (scroll * self.speed) % self.total_width
        start_x = -scroll_offset
        for i, rect in enumerate(self.rects):
            x_pos = start_x + i * self.scaled_width
            rect.pos = (x_pos, rect.pos[1])


class GroundLayer:
    def __init__(self, source, scroll_speed):
        self.source = source
        self.scroll_speed = scroll_speed
        self.offset = 0
        self.rects = []
        self.group = InstructionGroup()
        self.speed_multiplier = 1.0

        path = resource_find(self.source)
        if not path:
            raise FileNotFoundError(f"Ground image not found: {self.source}")
        self.texture = CoreImage(path).texture

        self.ground_width = self.texture.width
        self.ground_height = self.texture.height

    def set_speed_multiplier(self, multiplier):
        self.speed_multiplier = multiplier

    def resize(self):
        scale = Window.height / self.ground_height
        self.scaled_width = self.ground_width * scale
        self.scaled_height = Window.height

        if not self.rects:
            return
        for i, rect in enumerate(self.rects):
            rect.size = (self.scaled_width, self.scaled_height)
            rect.pos = (i * self.scaled_width, 0)

    def init_graphics(self, canvas, y):
        from kivy.graphics import Color, Rectangle
        self.group.clear()
        self.rects = []

        self.group.add(Color(1, 1, 1, 1))
        scale = Window.height / self.ground_height
        scaled_width = self.ground_width * scale
        scaled_height = Window.height
        self.scaled_width = scaled_width

        num_tiles = math.ceil(Window.width / scaled_width) + 3
        for i in range(num_tiles):
            rect = Rectangle(texture=self.texture, pos=(i * scaled_width, y),
                             size=(scaled_width, scaled_height))
            self.rects.append(rect)
            self.group.add(rect)

        if self.group in canvas.children:
            canvas.remove(self.group)
        canvas.add(self.group)

    def move(self, scroll):
        scroll_offset = scroll
        total_width = self.scaled_width * len(self.rects)
        for i, rect in enumerate(self.rects):
            x_pos = (i * self.scaled_width) - (scroll_offset % total_width)
            if x_pos + self.scaled_width < 0:
                x_pos += total_width
            rect.pos = (x_pos, rect.pos[1])


class OverlayLayer:
    def __init__(self, color=(0, 0, 0), opacity=0.3, speed=1.0):
        self.color = color
        self.opacity = opacity
        self.speed = speed
        self.rects = []
        self.group = InstructionGroup()
        self.scaled_width = 0

    def init_graphics(self, canvas):
        from kivy.graphics import Color, Rectangle
        self.group.clear()
        self.rects = []

        self.scaled_width = Window.width
        num_tiles = math.ceil(Window.width / self.scaled_width) + 3

        self.group.add(Color(*self.color, self.opacity))
        for i in range(num_tiles):
            rect = Rectangle(pos=(i * self.scaled_width, 0), size=Window.size)
            self.rects.append(rect)
            self.group.add(rect)

        if self.group in canvas.children:
            canvas.remove(self.group)
        canvas.add(self.group)

    def move(self, scroll):
        scroll_offset = (scroll * self.speed) % self.scaled_width
        start_x = -scroll_offset
        for i, rect in enumerate(self.rects):
            x_pos = start_x + i * self.scaled_width
            rect.pos = (x_pos, 0)

    def resize(self):
        self.scaled_width = Window.width
        for i, rect in enumerate(self.rects):
            rect.size = Window.size
            rect.pos = (i * self.scaled_width, 0)


class ParallaxWidget(Widget):
    def __init__(self, cow=None, **kwargs):
        super().__init__(**kwargs)
        self.scroll = 0
        self.scroll_max = 10000
        self.cow = cow
        self.layers = []
        self.ground = None

        self.build_background()

        Window.bind(on_resize=self.on_resize)
        Clock.schedule_interval(self.update, 1 / 60)

    def build_background(self):
        speed = 0.5
        for layer_num in range(1, 6):
            sources = [f"{base}/layer_{layer_num}.png" for base in BASE_PATHS]
            layer = ParallaxLayer(sources, speed)
            layer.init_graphics(self.canvas)
            self.layers.append(layer)
            if layer_num == 5:
                self.layer5_width = layer.scaled_width
            speed += 0.25


        self.ground_overlay = OverlayLayer(color=(1, 1, 1), opacity=0.4)
        self.ground_overlay.init_graphics(self.canvas)

        self.ground = GroundLayer(GROUND_PATH, get_objects_background_speed())
        self.ground.init_graphics(self.canvas, y=0)

    def on_resize(self, *args):
        for layer in self.layers:
            layer.resize()
        self.ground.resize()
        self.ground_overlay.resize()

    def update(self, dt):
        self.scroll = (self.scroll + self.ground.scroll_speed * self.ground.speed_multiplier * dt) % self.scroll_max
        for layer in self.layers:
            layer.move(self.scroll)
        self.ground.move(self.scroll)


class ParallaxApp(App):
    def build(self):
        return ParallaxWidget()

if __name__ == '__main__':
    ParallaxApp().run()