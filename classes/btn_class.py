from pygame import *

class Button:
    def __init__(self, window, text, center, width, height, font_size=40):
        self.window = window
        self.rect = Rect(center[0] - width//2, center[1] - height//2, width, height)
        self.hover_sound = mixer.Sound('assets/btn_collide_sound.wav')
        self.font = font.Font("assets/my_font.otf", font_size)
        self.text_surf = self.font.render(text, True, (0,0,0))
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        self.hovered = False

    def draw(self, vol):
        if self.rect.collidepoint(mouse.get_pos()):
            if not self.hovered:
                self.hover_sound.set_volume(vol / 10)
                self.hover_sound.play()
                self.hovered = True
            color = (200,200,200)
        else:
            self.hovered = False
            color = (255,255,255)
        draw.rect(self.window, color, self.rect)
        self.window.blit(self.text_surf, self.text_rect)

    def is_pressed(self, event_list):
        for e in event_list:
            if e.type == MOUSEBUTTONDOWN and self.rect.collidepoint(e.pos):
                return True
        return False