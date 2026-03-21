from pygame import *


class InputBox:
    def __init__(self, window, center, width, height, text='', font_size=32, max_chars=11):
        self.window = window
        self.rect = Rect(center[0] - width//2, center[1] - height//2, width, height)
        self.color_inactive = (100, 100, 100)
        self.color_active = (255, 255, 255)
        self.color = self.color_inactive
        self.max_chars = max_chars

        self.text = text
        self.font = font.SysFont("Arial", font_size)
        self.active = False

        self.cursor_visible = True
        self.last_cursor_switch = time.get_ticks()

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = self.color_active
            else:
                self.active = False
                self.color = self.color_inactive

        if self.active:
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == K_RETURN:
                    self.active = False
                    self.color = self.color_inactive

            elif event.type == TEXTINPUT:
                if len(self.text) < self.max_chars:
                    self.text += event.text

    def draw(self):
        draw.rect(self.window, self.color, self.rect, 2, border_radius=5)

        txt_surface = self.font.render(self.text, True, (255, 255, 255))
        self.window.blit(txt_surface, (self.rect.x + 10, self.rect.y + (self.rect.h - txt_surface.get_height()) // 2))

        if self.active:
            current_time = time.get_ticks()
            if current_time - self.last_cursor_switch > 500:  # Каждые 500мс
                self.cursor_visible = not self.cursor_visible
                self.last_cursor_switch = current_time

            if self.cursor_visible:
                cursor_x = self.rect.x + 10 + txt_surface.get_width() + 2
                draw.line(self.window, (255, 255, 255),
                          (cursor_x, self.rect.y + 10),
                          (cursor_x, self.rect.y + self.rect.h - 10), 2)