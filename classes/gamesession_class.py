from classes.orb_class import Orb
from classes.bullet_class import Bullet
from pygame import Surface, transform, SRCALPHA

class GameSession:
    def __init__(self, window, global_volume, player_skin=(185, 0, 255)):
        self.window = window
        self.global_volume = global_volume

        self.player_orb = Orb(window, 500, 400, 35, player_skin)

        self.bullets = []
        self.active_walls = []

        self.gun_surf = Surface((30, 10), SRCALPHA)
        self.gun_surf.fill((200, 200, 200))

    def update(self, dt, events):
        self.player_orb.shoot(
            events,
            dt,
            self.bullets,
            Bullet,
            self.global_volume,
            self.player_orb.shot_sound,
            self.player_orb.reload_sound,
            self.player_orb.empty_sound
        )
        self.player_orb.update(self.active_walls, dt)

        self.bullets = [b for b in self.bullets if b.update(self.active_walls, dt)]

    def draw(self):
        for wall in self.active_walls:
            wall.draw()
        for bullet in self.bullets:
            bullet.draw(self.window)
        self.player_orb.draw()

        gx, gy, angle = self.player_orb.get_gun_pos()
        rotated_gun = transform.rotate(self.gun_surf, -angle * 180 / 3.14159265)
        self.window.blit(rotated_gun, rotated_gun.get_rect(center=(gx, gy)))