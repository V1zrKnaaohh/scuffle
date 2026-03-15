from pygame import *

class Block:
    def __init__(self, window, x, y, width, height, color=(100, 100, 100)):
        self.window = window
        self.rect = Rect(x, y, width, height)
        self.color = color

    def draw(self):
        draw.rect(self.window, self.color, self.rect)

def get_room(window, room_id):
    walls = []
    if room_id == "trialroom1":
        walls = [

        ]

    elif room_id == "fightroom1":

        walls = [

        ]

    elif room_id == "fightroom1":

        walls = [

        ]

    return walls