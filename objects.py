from classes.btn_class import Button
from classes.sprite_class import Sprite


def setup_objects(window, window_center, global_volume):

    objs = {}

    # мейн лобби
    objs["main_game_logo"] = Sprite(window, "Scuffle", (window_center[0], window_center[1] - 215), 170, 60,320, (0,0,0), (255,255,255))

    objs["play"] = Button(window, "play", window_center, 170, 60)
    objs["profile"] = Button(window, "profile", (window_center[0], window_center[1] + 80), 170, 60)
    objs["settings"] = Button(window, "settings", (window_center[0], window_center[1] + 160), 170, 60)
    objs["exit"] = Button(window, "exit", (window_center[0], window_center[1] + 240), 170, 60)

    # плей меню
    objs["play_text"] = Sprite(window, "Play", (window_center[0], window_center[1] - 215), 170, 60,150, (0,0,0), (255,255,255))

    objs["host"] = Button(window, "host", (window_center[0], window_center[1] + 80), 170, 60)
    objs["play_test"] = Button(window, "test", (window_center[0], window_center[1] + 160), 170, 60)
    objs["connect"] = Button(window, "connect", (window_center[0], window_center[1]), 170, 60)


    # настройки
    objs["setts_text"] = Sprite(window, "Settings", (window_center[0], window_center[1] - 215), 170, 60,150, (0,0,0), (255,255,255))

    objs["vol_num_spr"] = Sprite(window, str(int(global_volume)), (window_center[0], window_center[1] + 80), 50, 60)
    objs["vol_text_spr"] = Sprite(window, "volume:", (window_center[0], window_center[1]), 170, 60)

    objs["vol_down"] = Button(window, "<", (window_center[0] - 60, window_center[1] + 80), 50, 60)
    objs["vol_up"] = Button(window, ">", (window_center[0] + 60, window_center[1] + 80), 50, 60)

    # профиле

    objs["profile_text"] = Sprite(window, "Profile", (window_center[0], window_center[1] - 215), 170, 60,150, (0,0,0), (255,255,255))


    # нозады
    objs["profile_back"] = Button(window, "back", (window_center[0], window_center[1]), 170, 60)
    objs["connect_back"] = Button(window, "back", (window_center[0], window_center[1]), 170, 60)
    objs["host_back"] = Button(window, "back", (window_center[0], window_center[1]), 170, 60)
    objs["play_back"] = Button(window, "back", (window_center[0], window_center[1] + 240), 170, 60)
    objs["settings_back"] = Button(window, "back", (window_center[0], window_center[1] + 160), 170, 60)

    objs["game_back"] = Button(window, "X", (50, 50), 90, 90)



    return objs
