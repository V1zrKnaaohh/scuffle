from classes.btn_class import Button
from classes.textsprite_class import TextSprite
from classes.inputbox_class import InputBox


def setup_objects(window, window_center, global_volume, nickname):
    objs = {}
    cx, cy = window_center

    # main_lobby
    objs["main_game_logo"] = TextSprite(window, "Scuffle", (cx, cy - 215), 170, 60, 320, (0, 0, 0), (255, 255, 255))
    objs["version_num"] = TextSprite(window, "0.2.1", (cx, cy - 100), 40, 15, 30, (0, 0, 0), (105, 105, 105))

    objs["play"] = Button(window, "play", (cx, cy), 170, 60)
    objs["profile"] = Button(window, "profile", (cx, cy + 80), 170, 60)
    objs["settings"] = Button(window, "settings", (cx, cy + 160), 170, 60)
    objs["exit"] = Button(window, "exit", (cx, cy + 240), 170, 60)

    # play_menu
    objs["play_text"] = TextSprite(window, "Play", (cx, cy - 215), 170, 60, 150, (0, 0, 0), (255, 255, 255))

    objs["connect"] = Button(window, "connect", (cx, cy), 170, 60)
    objs["host"] = Button(window, "host", (cx, cy + 80), 170, 60)
    objs["play_test"] = Button(window, "test", (cx, cy + 160), 170, 60)
    objs["play_back"] = Button(window, "back", (cx, cy + 240), 170, 60)

    # host_menu
    objs["host_text"] = TextSprite(window, "Host", (cx, cy - 215), 170, 60, 150, (0, 0, 0), (255, 255, 255))


    objs["host_start"] = Button(window, "start", (cx, cy), 170, 60)
    objs["host_back"] = Button(window, "back", (cx, cy + 80), 170, 60)

    # connect_menu
    objs["connect_text"] = TextSprite(window, "Connect", (cx, cy - 215), 170, 60, 150, (0, 0, 0), (255, 255, 255))

    objs["ip_input"] = InputBox(window, (cx, cy), 250, 50, "127.0.0.1", max_chars=15)
    objs["connect_start"] = Button(window, "start", (cx, cy + 80), 170, 60)
    objs["connect_back"] = Button(window, "back", (cx, cy + 160), 170, 60)

    # settings_menu
    objs["setts_text"] = TextSprite(window, "Settings", (cx, cy - 215), 170, 60, 150, (0, 0, 0), (255, 255, 255))

    objs["vol_text_spr"] = TextSprite(window, "volume:", (cx, cy), 170, 60)
    objs["vol_num_spr"] = TextSprite(window, str(int(global_volume)), (cx, cy + 80), 50, 60)

    objs["vol_down"] = Button(window, "<", (cx - 60, cy + 80), 50, 60)
    objs["vol_up"] = Button(window, ">", (cx + 60, cy + 80), 50, 60)
    objs["settings_back"] = Button(window, "back", (cx, cy + 160), 170, 60)

    # profile_menu
    objs["profile_text"] = TextSprite(window, "Profile", (cx, cy - 215), 170, 60, 150, (0, 0, 0), (255, 255, 255))
    objs["name_input"] = InputBox(window, (cx, cy), 200, 50, nickname)
    objs["profile_back"] = Button(window, "back", (cx, cy + 80), 170, 60)

    # game
    objs["game_back"] = Button(window, "X", (50, 50), 90, 90)

    return objs