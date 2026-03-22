from pygame import *
import math
from random import randint


class Orb:
    def __init__(self, window, x, y, radius, color):
        self.window = window
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

        self.lifes = 3
        self.health = 100

        self.sx = 0
        self.sy = 0
        self.ACC = 0.8
        self.FRICTION = 0.80
        self.MAX_SPEED = 5

        self.max_ammo = 2
        self.ammo = self.max_ammo
        self.is_reloading = False
        self.reload_timer = 0
        self.reload_duration = 2.0

        self.is_firing = False
        self.angle = 0

        self.shot_sound = mixer.Sound('assets/gun_shot_sound.wav')
        self.reload_sound = mixer.Sound('assets/gun_reload_sound.wav')
        self.empty_sound = mixer.Sound('assets/gun_empty_sound.wav')

    def get_gun_pos(self):
        if self.color != (255, 50, 50):
            m_x, m_y = mouse.get_pos()
            dx = m_x - self.x
            dy = m_y - self.y
            self.angle = math.atan2(dy, dx)

        distance = self.radius + 20
        gun_x = self.x + math.cos(self.angle) * distance
        gun_y = self.y + math.sin(self.angle) * distance

        return gun_x, gun_y, self.angle

    def shoot(self, events, dt, bullets, BulletClass, global_volume):
        if self.is_reloading:
            self.reload_timer -= dt
            if self.reload_timer <= 0:
                self.ammo = self.max_ammo
                self.is_reloading = False

        for e in events:
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                self.is_firing = True
                if self.ammo > 0 and not self.is_reloading:
                    gx, gy, angle = self.get_gun_pos()
                    keys = key.get_pressed()
                    spread = 0 if keys[K_LSHIFT] else math.radians(randint(-3, 3))

                    bullets.append(BulletClass(gx, gy, angle + spread, "player"))

                    self.shot_sound.set_volume(global_volume / 10)
                    self.shot_sound.play()
                    self.ammo -= 1

                    if self.ammo <= 0:
                        self.reload_sound.set_volume(global_volume / 10)
                        self.reload_sound.play()
                        self.is_reloading = True
                        self.reload_timer = self.reload_duration
                else:
                    self.empty_sound.set_volume(global_volume / 10)
                    self.empty_sound.play()

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
        self.get_gun_pos()

    def draw(self):
        draw.circle(self.window, self.color, (int(self.x), int(self.y)), self.radius)
        if self.is_reloading:
            bar_rect = Rect(self.x - 20, self.y - self.radius - 15, 40, 5)
            draw.rect(self.window, (50, 50, 50), bar_rect)
            progress = (self.reload_duration - self.reload_timer) / self.reload_duration
            draw.rect(self.window, (0, 255, 150), (bar_rect.x, bar_rect.y, 40 * progress, 5))