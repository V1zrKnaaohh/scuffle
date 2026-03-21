from pygame import *
from objects import setup_objects
from save_manager import save_data, load_data
from random import randint

from classes.orb_class import Orb
from classes.block_class import Block, get_room
from classes.bullet_class import Bullet

import math

# init
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
my_nickname = saved_settings.get("nickname", "Player")

gunshotsound = mixer.Sound('assets/gun_shot_sound.wav')
gunreloadsound = mixer.Sound('assets/gun_reload_sound.wav')
gunemptysound = mixer.Sound('assets/gun_empty_sound.wav')




current_music = None

objs = setup_objects(window, window_center, global_volume, my_nickname)

player_skin = (185, 0, 255)
player_orb = Orb(window, 500, 400, 35, player_skin)

gun_surf = Surface((30, 10), SRCALPHA)
gun_surf.fill((200, 200, 200))

bullets = []
active_walls = []

# главный цикл
while running:
    dt = clock.tick(120) / 1000.0
    events = event.get()

    for e in events:
        if e.type == QUIT:
            running = False


    if state == "main_lobby" and current_music != "menu":
        mixer.music.load('assets/menu_music.wav')
        mixer.music.set_volume(global_volume / 10)
        mixer.music.play(-1)
        current_music = "menu"

    elif state == "game" and current_music != "game":
        mixer.music.load('assets/game_music.wav')
        mixer.music.set_volume(global_volume / 10)
        mixer.music.play(-1)
        current_music = "game"


    window.fill("black")


    # мейн лобби

    if state == "main_lobby":
        objs["main_game_logo"].draw()
        objs["play"].draw(global_volume)
        objs["settings"].draw(global_volume)
        objs["profile"].draw(global_volume)
        objs["exit"].draw(global_volume)
        objs["version_num"].draw()

        if objs["play"].is_pressed(events):
            state = "play_menu"

        elif objs["settings"].is_pressed(events):
            state = "settings_menu"

        elif objs["profile"].is_pressed(events):
            state = "profile_menu"

        elif objs["exit"].is_pressed(events):
            running = False


    # плей меню

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
            bullets.clear()
            state = "game"

    # настрйоки

    elif state == "settings_menu":
        objs["setts_text"].draw()
        objs["vol_up"].draw(global_volume)
        objs["vol_down"].draw(global_volume)
        objs["vol_num_spr"].draw()
        objs["vol_text_spr"].draw()
        objs["settings_back"].draw(global_volume)

        if objs["vol_up"].is_pressed(events):
            global_volume = min(10, global_volume + 1)

        elif objs["vol_down"].is_pressed(events):
            global_volume = max(0, global_volume - 1)

        objs["vol_num_spr"].set_text(global_volume)

        current_data = load_data()
        current_data["volume"] = global_volume
        save_data(current_data)

        mixer.music.set_volume(global_volume / 10)
        gunshotsound.set_volume(global_volume / 10)

        if objs["settings_back"].is_pressed(events):
            state = "main_lobby"

    # профиле

    elif state == "profile_menu":
        objs["profile_text"].draw()
        objs["name_input"].draw()
        objs["profile_back"].draw(global_volume)

        for e in events:
            objs["name_input"].handle_event(e)

        if objs["profile_back"].is_pressed(events):
            new_nick = objs["name_input"].text.strip() or "Player"

            current_data = load_data()
            current_data["nickname"] = new_nick
            save_data(current_data)

            state = "main_lobby"


    # игра

    elif state == "game":

        player_orb.shoot(events, dt, bullets, Bullet, global_volume, gunshotsound, gunreloadsound, gunemptysound)
        player_orb.update(active_walls, dt)
        bullets = [b for b in bullets if b.update(active_walls, dt)]

        for wall in active_walls:
            wall.draw()
        for bullet in bullets:
            bullet.draw(window)

        player_orb.draw()

        gx, gy, angle = player_orb.get_gun_pos()

        rotated_gun = transform.rotate(gun_surf, math.degrees(-angle))

        window.blit(rotated_gun, rotated_gun.get_rect(center=(gx, gy)))

        objs["game_back"].draw(global_volume)

        if objs["game_back"].is_pressed(events):
            state = "main_lobby"

            bullets.clear()


    # хост / конект

    elif state == "host_menu":
        objs["host_back"].draw(global_volume)

        if objs["host_back"].is_pressed(events):
            state = "play_menu"

    elif state == "connect_menu":
        objs["connect_back"].draw(global_volume)

        if objs["connect_back"].is_pressed(events):
            state = "play_menu"

    display.update()

quit()