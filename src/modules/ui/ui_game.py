from modules.prompt import prompt
from modules import renderer as r
from modules.assets import yatzy_banner
from datetime import datetime

import time


def ui_game(navigator):
    date_time, set_date_time = r.use_state()
    r.use_effect(lambda: set_date_time(datetime.now().strftime("%d-%m-%Y_%H:%M:%S")))
    game_is_running, set_game_is_running = r.use_state(False)
    game_difficulty, set_game_difficulty = r.use_state()
    err_msg, set_err_msg = r.use_state("")

    if not bool(game_difficulty()):
        print("select difficulty: ")
        print()
        print("0 - easy")
        print("1 - normal")
        print("2 - hard")
        print()
        if err_msg():
            print(err_msg())
        usr_input = prompt("enter your choice: ")
        try:
            usr_input = int(usr_input)
            if usr_input >= 2 or usr_input <= 0:
                set_err_msg("please pick a valid number")
                navigator["reload"]()
            else:
                set_err_msg("")
                set_game_difficulty(usr_input)
        except:
            set_err_msg("please pick a valid number")
            pass

    with open(f"game-{date_time()}.json", "w") as file:
        pass
