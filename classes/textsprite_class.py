from pygame import *


class TextSprite():
    def __init__(self, window, text, center, width, height, font_size=40, color=(255,255,255), text_color=(0,0,0)):
        self.window = window
        self.text = text
        self.width = width
        self.height = height
        self.color = color
        self.text_color = text_color

        self.rect = Rect(center[0] - width//2, center[1] - height//2, width, height)

        self.font = font.Font("assets/my_font.otf", font_size)
        self.text_surf = self.font.render(text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self):
        draw.rect(self.window, self.color, self.rect)
        self.window.blit(self.text_surf, self.text_rect)

    def set_text(self, new_text):
        self.text = str(new_text)
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
