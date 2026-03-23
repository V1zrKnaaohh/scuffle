from pygame import *

class Block:
    def __init__(self, window, x, y, width, height, color=(100, 100, 100)):
        self.window = window
        self.rect = Rect(x, y, width, height)
        self.color = color

    def draw(self):
        draw.rect(self.window, self.color, self.rect)


def get_room(window, room_id):
    w = window.get_width()
    h = window.get_height()
    b = 100

    border_top = Block(window, 0, 0, w, b, (50, 50, 50))
    border_bottom = Block(window, 0, h - b, w, b, (50, 50, 50))
    border_left = Block(window, 0, 0, b, h, (50, 50, 50))
    border_right = Block(window, w - b, 0, b, h, (50, 50, 50))

    base_borders = [border_top, border_bottom, border_left, border_right]

    if room_id == "trialroom1":
        return base_borders + [
            Block(window, 400, 300, 200, 50),
            Block(window, 1200, 620, 80, 360),
            Block(window, 600, 600, 240, 70),
        ]

    elif room_id == "fightroom1":
        return base_borders + [

        ]

    return base_borders