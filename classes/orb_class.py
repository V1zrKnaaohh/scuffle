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
        self.FRICTION = 0.87
        self.MAX_SPEED = 6

    def update(self, walls, dt):
        keys = key.get_pressed()
        move_x = 0
        move_y = 0
        move_dt = dt * 120

        if keys[K_w]: move_y -= 1
        if keys[K_s]: move_y += 1
        if keys[K_a]: move_x -= 1
        if keys[K_d]: move_x += 1

        self.sx += move_x * self.ACC * move_dt
        self.sy += move_y * self.ACC * move_dt

        if keys[K_LSHIFT]:
            self.sx *= 0.6
            self.sy *= 0.6

        speed = (self.sx ** 2 + self.sy ** 2) ** 0.5
        if speed > self.MAX_SPEED:
            self.sx = (self.sx / speed) * self.MAX_SPEED
            self.sy = (self.sy / speed) * self.MAX_SPEED

        self.sx *= self.FRICTION
        self.sy *= self.FRICTION
        self.x += self.sx * move_dt

        player_rect = Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        for wall in walls:
            if player_rect.colliderect(wall.rect):
                if self.sx > 0:
                    self.x = wall.rect.left - self.radius
                elif self.sx < 0:
                    self.x = wall.rect.right + self.radius
                self.sx = 0

        self.y += self.sy * move_dt

        player_rect = Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        for wall in walls:
            if player_rect.colliderect(wall.rect):
                if self.sy > 0:
                    self.y = wall.rect.top - self.radius
                elif self.sy < 0:
                    self.y = wall.rect.bottom + self.radius
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
