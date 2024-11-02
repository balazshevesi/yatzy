# file for ui entry point, kind of like App.jsx in React.js
from modules.hooks.use_navigation import use_navigation
from modules.ui.ui_game import ui_game
from modules.ui.ui_menu_start import ui_menu_start
from modules.ui.ui_navigate import ui_navigate


def ui_app():
    """ui entrypoint of the app"""
    navigator = use_navigation("start")

    # basically a router
    match navigator["get_path"]():
        case "start":
            ui_menu_start(navigator)
        case "start/main_menu":
            print(navigator["get_path"]())
            ui_navigate(
                navigator,
                "select an alternative: ",
                (
                    ("play local", "play_local"),
                    ("play online (coming soon)", "play_online"),
                    ("credits", "credits"),
                    ("help", "help"),
                ),
            )
        case "start/main_menu/play_local":
            ui_game(navigator)
