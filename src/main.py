from modules import renderer as r
from modules.prompt import prompt
from modules.art import yatzy_banner
from modules.hooks.use_navigation import use_navigation
from modules.ui.ui_menu_start import ui_menu_start
from modules.ui.ui_navigate import ui_navigate

import time


def ui_app():
    navigator = use_navigation("start")

    # def effect():
    #     print("effect ran!")

    # r.use_effect(effect)

    print(navigator["get_path"]())
    print()
    print()

    match navigator["get_path"]():
        case "start":
            ui_menu_start(navigator)
        case "start/main_menu":
            ui_navigate(
                navigator,
                "Select an alternative: ",
                (
                    ("play local", "play_local"),
                    ("play online", "play_online"),
                    ("credits", "credits"),
                    ("help", "help"),
                ),
            )
        case "start/main_menu/play_local":
            ui_navigate(
                navigator,
                "Select an alternative: ",
                (
                    ("play against computer", "pvc"),
                    ("play against player", "pvp"),
                ),
            )
        case "start/main_menu/play_local/pvc":
            ui_navigate(
                navigator,
                "Select an alternative: ",
                (
                    ("play against computer", "pvc"),
                    ("play against player", "pvp"),
                ),
            )


def main():
    r.render(ui_app)


if __name__ == "__main__":
    main()
