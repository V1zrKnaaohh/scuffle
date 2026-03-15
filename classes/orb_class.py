from pygame import *
import math

class Orb:
    def __init__(self, window, x, y, radius, color):
        self.window = window
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.sx = 0
        self.sy = 0
        self.ACC = 0.8
        self.FRICTION = 0.85
        self.MAX_SPEED = 5

    def update(self):
        # --- ТВОЙ ОРИГИНАЛЬНЫЙ КОД ---
        keys = key.get_pressed()
        move_x = 0
        move_y = 0

        if keys[K_w]: move_y -= 1
        if keys[K_s]: move_y += 1
        if keys[K_a]: move_x -= 1
        if keys[K_d]: move_x += 1

        self.sx += move_x * self.ACC
        self.sy += move_y * self.ACC

        if keys[K_LSHIFT]:
            self.sx *= 0.6
            self.sy *= 0.6

        speed = (self.sx ** 2 + self.sy ** 2) ** 0.5
        if speed > self.MAX_SPEED:
            self.sx = (self.sx / speed) * self.MAX_SPEED
            self.sy = (self.sy / speed) * self.MAX_SPEED

        self.sx *= self.FRICTION
        self.sy *= self.FRICTION

        self.x += self.sx
        self.y += self.sy

        border_size = 100

        if self.x < border_size + self.radius:
            self.x = border_size + self.radius
            self.sx = 0
        elif self.x > self.window.get_width() - border_size - self.radius:
            self.x = self.window.get_width() - border_size - self.radius
            self.sx = 0


        if self.y < border_size + self.radius:
            self.y = border_size + self.radius
            self.sy = 0
        elif self.y > self.window.get_height() - border_size - self.radius:
            self.y = self.window.get_height() - border_size - self.radius
            self.sy = 0


    def draw(self):
        draw.circle(self.window, self.color, (int(self.x), int(self.y)), self.radius)

    def check_collision(self, other_orb):
        dx = self.x - other_orb.x
        dy = self.y - other_orb.y

        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance < (self.radius + other_orb.radius):
            return True
        return False


    def get_gun_pos(self):
        m_x, m_y = mouse.get_pos()

        dx = m_x - self.x
        dy = m_y - self.y

        angle = math.atan2(dy, dx)

        distance = self.radius + 20

        gun_x = self.x + math.cos(angle) * distance
        gun_y = self.y + math.sin(angle) * distance

        return gun_x, gun_y, angle