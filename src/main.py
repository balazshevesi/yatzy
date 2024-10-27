from modules import renderer as r
from modules.helpers import prompt
from modules.assets import yatzy_banner
from modules.hooks.use_navigation import use_navigation
from modules.ui.ui_game import ui_game
from modules.ui.ui_menu_start import ui_menu_start
from modules.ui.ui_navigate import ui_navigate
import time

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from modules.helpers import prompt  # Your normal imports here


def ui_app():
    # navigator = use_navigation("start")
    navigator = use_navigation("start/main_menu/play_local/pvc")

    print(navigator["get_path"]())
    print()
    print()

    match navigator["get_path"]():
        case "start":
            ui_menu_start(navigator)
        case "start/main_menu":
            ui_navigate(
                navigator,
                "select an alternative: ",
                (
                    ("play local", "play_local"),
                    ("play online (not working yet)", "play_online"),
                    ("credits", "credits"),
                    ("help", "help"),
                ),
            )
        case "start/main_menu/play_local":
            ui_navigate(
                navigator,
                "select an alternative: ",
                (("play against computer", "pvc"), ("play against player", "pvp")),
            )
        case "start/main_menu/play_local/pvc":
            # print("bruh")
            ui_game(navigator)


def main():
    r.render(ui_app)


if __name__ == "__main__":
    main()
