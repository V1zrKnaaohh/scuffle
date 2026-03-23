from classes.orb_class import Orb
from classes.bullet_class import Bullet
from pygame import *
from random import randint

class GameSession:
    def __init__(self, window, global_volume, is_host=True, player_skin=(185, 0, 255)):
        self.window = window
        self.global_volume = global_volume
        self.is_host = is_host

        self.font_path = "assets/my_font.otf"
        self.my_font = font.Font(self.font_path, 30)

        if self.is_host:
            self.player_orb = Orb(window, 200, 500, 35, player_skin)
            self.enemy_orb = Orb(window, 1700, 500, 35, (255, 50, 50))
        else:
            self.player_orb = Orb(window, 1700, 500, 35, player_skin)
            self.enemy_orb = Orb(window, 200, 500, 35, (255, 50, 50))

        self.bullets = []
        self.active_walls = []
        self.net = None

        self.gun_surf = Surface((30, 10), SRCALPHA)
        self.gun_surf.fill((200, 200, 200))

    def update(self, dt, events):
        self.player_orb.update(self.active_walls, dt)
        self.player_orb.shoot(events, dt, self.bullets, Bullet, self.global_volume)

        if self.net:
            try:
                my_data = {
                    "x": self.player_orb.x, "y": self.player_orb.y,
                    "angle": self.player_orb.angle, "firing": self.player_orb.is_firing,
                    "health": self.player_orb.health, "lifes": self.player_orb.lifes
                }
                self.player_orb.is_firing = False
                enemy_data = self.net.send(my_data)

                if enemy_data:
                    self.enemy_orb.x = enemy_data.get("x", self.enemy_orb.x)
                    self.enemy_orb.y = enemy_data.get("y", self.enemy_orb.y)
                    self.enemy_orb.angle = enemy_data.get("angle", self.enemy_orb.angle)
                    self.enemy_orb.health = enemy_data.get("health", 100)
                    self.enemy_orb.lifes = enemy_data.get("lifes", 3)

                    if enemy_data.get("firing"):
                        ex, ey, ea = self.enemy_orb.get_gun_pos()
                        self.bullets.append(Bullet(ex, ey, ea, "enemy"))
                        self.enemy_orb.shot_sound.set_volume(self.global_volume / 10)
                        self.enemy_orb.shot_sound.play()
                else:
                    return "main_lobby"
            except:
                return "main_lobby"

        self.bullets = [b for b in self.bullets if b.update(self.active_walls, dt)]

        p_rect = Rect(self.player_orb.x - 35, self.player_orb.y - 35, 70, 70)
        e_rect = Rect(self.enemy_orb.x - 35, self.enemy_orb.y - 35, 70, 70)

        for bullet in self.bullets[:]:
            b_rect = Rect(bullet.x - 2, bullet.y - 2, 4, 4)
            if b_rect.colliderect(p_rect):
                if getattr(bullet, 'lifetime', 0) > 0.05:
                    self.player_orb.health -= 20
                    if bullet in self.bullets: self.bullets.remove(bullet)
            elif b_rect.colliderect(e_rect):
                if not self.net:
                    self.enemy_orb.health -= 20
                if bullet in self.bullets:
                    self.bullets.remove(bullet)

        if self.player_orb.health <= 0:
            if self.player_orb.lifes > 0:
                self.player_orb.x = (200 if self.is_host else 1600) + randint(-50, 50)
                self.player_orb.y = 500 + randint(-200, 200)
                self.player_orb.health = 100
                self.player_orb.lifes -= 1
            else:
                return "main_lobby"

        if self.enemy_orb.health <= 0:
            if not self.net:
                if self.enemy_orb.lifes > 0:
                    self.enemy_orb.x, self.enemy_orb.y = 1400, 800
                    self.enemy_orb.health = 100
                    self.enemy_orb.lifes -= 1
                else:
                    return "main_lobby"
            else:
                if self.enemy_orb.lifes <= 0:
                    return "main_lobby"

        return "game"

    def draw(self):
        for wall in self.active_walls:
            wall.draw()
        for bullet in self.bullets:
            bullet.draw(self.window)

        self.player_orb.draw()
        self.enemy_orb.draw()
        self.draw_hud()

        gx, gy, angle = self.player_orb.get_gun_pos()
        rotated_gun = transform.rotate(self.gun_surf, -angle * 180 / 3.14159265)
        self.window.blit(rotated_gun, rotated_gun.get_rect(center=(gx, gy)))

        egx, egy, e_angle = self.enemy_orb.get_gun_pos()
        rotated_enemy_gun = transform.rotate(self.gun_surf, -e_angle * 180 / 3.14159265)
        self.window.blit(rotated_enemy_gun, rotated_enemy_gun.get_rect(center=(egx, egy)))

    def draw_hud(self):
        hp_str = f"HP: {int(self.player_orb.health)}"
        lives_str = f"LIVES: {self.player_orb.lifes}"

        hp_surf = self.my_font.render(hp_str, True, (255, 255, 255))
        lives_surf = self.my_font.render(lives_str, True, (255, 255, 255))

        screen_h = self.window.get_height()

        self.window.blit(lives_surf, (20, screen_h - 80))
        self.window.blit(hp_surf, (20, screen_h - 45))