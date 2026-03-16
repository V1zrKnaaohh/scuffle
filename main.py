from pygame import *
from objects import setup_objects
from save_manager import save_data, load_data

from classes.orb_class import Orb
from classes.block_class import Block,get_room
from classes.bullet_class import Bullet

import math


# окошко

init()
mixer.init()

info = display.Info()
window = display.set_mode((info.current_w, info.current_h), FULLSCREEN)
window_center = (window.get_width() // 2, window.get_height() // 2)

running = True
clock = time.Clock()
state = "main_lobby"
game_state = ""
saved_settings = load_data()
global_volume = saved_settings.get("volume", 5)

objs = setup_objects(window, window_center, global_volume)

player_skin = (185, 0, 255)
player_orb = Orb(window, 500, 400, 35, (player_skin))

gun_surf = Surface((30, 10), SRCALPHA)
gun_surf.fill((200, 200, 200))

bullets = []
active_walls = []


 # главный цикл
while running:
    dt = clock.tick(120) / 1000.0
    window.fill("black")
    events = event.get()


    for e in events:
        if e.type == QUIT:
            running = False

    if state == "main_lobby":
        objs["main_game_logo"].draw()

        objs["play"].draw(global_volume)
        objs["settings"].draw(global_volume)
        objs["profile"].draw(global_volume)
        objs["exit"].draw(global_volume)

        if objs["play"].is_pressed(events):
            state = "play_menu"

        elif objs["settings"].is_pressed(events):
            state = "settings_menu"

        elif objs["profile"].is_pressed(events):
            state = "profile_menu"

        elif objs["exit"].is_pressed(events):
            running = False

    elif state == "play_menu":
        objs["play_text"].draw()
        objs["host"].draw(global_volume)
        objs["connect"].draw(global_volume)
        objs["play_back"].draw(global_volume)
        objs["play_test"].draw(global_volume)

        if objs["connect"].is_pressed(events):
            state = "connect_menu"

        if objs["host"].is_pressed(events):
            state = "host_menu"

        if objs["play_back"].is_pressed(events):
            state = "main_lobby"

        if objs["play_test"].is_pressed(events):
            game_state = "playtest"
            active_walls = get_room(window, "trialroom1")
            state = "game"

    elif state == "settings_menu":
        objs["setts_text"].draw()
        objs["vol_up"].draw(global_volume)
        objs["vol_down"].draw(global_volume)
        objs["vol_num_spr"].draw()
        objs["vol_text_spr"].draw()
        objs["settings_back"].draw(global_volume)

        if objs["vol_up"].is_pressed(events):
            global_volume = min(10, global_volume + 1)
            objs["vol_num_spr"].set_text(global_volume)
            save_data({"volume": global_volume})

        elif objs["vol_down"].is_pressed(events):
            global_volume = max(0, global_volume - 1)
            objs["vol_num_spr"].set_text(global_volume)
            save_data({"volume": global_volume})

        elif objs["settings_back"].is_pressed(events):
            state = "main_lobby"

    elif state == "profile_menu":
        objs["profile_text"].draw()
        objs["profile_back"].draw(global_volume)

        if objs["profile_back"].is_pressed(events):
            state = "main_lobby"


    elif state == "game":

        for e in events:
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                gx, gy, g_angle = player_orb.get_gun_pos()

                bullets.append(Bullet(gx, gy, g_angle))

        player_orb.update(active_walls, dt)
        for b in bullets[:]:
            if not b.update(active_walls, dt):
                bullets.remove(b)

        window.fill("black")

        for wall in active_walls:
            wall.draw()
        for bullet in bullets:
            bullet.draw(window)
        player_orb.draw()

        gx, gy, angle = player_orb.get_gun_pos()
        deg = math.degrees(-angle)
        rotated_gun = transform.rotate(gun_surf, deg)

        gun_rect = rotated_gun.get_rect(center=(gx, gy))

        window.blit(rotated_gun, gun_rect)


        objs["game_back"].draw(global_volume)

        if objs["game_back"].is_pressed(events):
            state = "main_lobby"

            bullets.clear()


    elif state == "host_menu":
        objs["host_back"].draw(global_volume)

        if objs["host_back"].is_pressed(events):
            state = "play_menu"


    elif state == "connect_menu":
        objs["connect_back"].draw(global_volume)

        if objs["connect_back"].is_pressed(events):
            state = "play_menu"


    display.update()
    clock.tick(120)

quit()