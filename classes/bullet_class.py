from pygame import *
import math


class Bullet:
    def __init__(self, x, y, angle, spread):
        self.x = x
        self.y = y
        self.radius = 5
        self.speed = 37

        self.vx = math.cos(angle) * self.speed
        self.vy = math.sin(angle) * self.speed

        self.rect = Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        self.bounces = 0

    def update(self, walls, dt):
        move_dt = dt * 120
        total_dx = self.vx * move_dt
        total_dy = self.vy * move_dt
        steps = 5
        dx = total_dx / steps
        dy = total_dy / steps

        for _ in range(steps):
            self.x += dx
            self.y += dy
            self.rect.center = (self.x, self.y)

            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    overlap_left = abs(self.rect.right - wall.rect.left)
                    overlap_right = abs(self.rect.left - wall.rect.right)
                    overlap_top = abs(self.rect.bottom - wall.rect.top)
                    overlap_bottom = abs(self.rect.top - wall.rect.bottom)

                    min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

                    if min_overlap == overlap_left or min_overlap == overlap_right:
                        self.vx *= -1
                        dx *= -1
                    else:
                        self.vy *= -1
                        dy *= -1

                    self.bounces += 1
                    if self.bounces > 1:
                        return False
                    return True

        if self.bounces > 2:
            return False
        return True

    def draw(self, window):
        draw.circle(window, (255, 255, 0), (int(self.x), int(self.y)), self.radius)