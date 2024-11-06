# file for ui entry point, kind of like App.jsx in React.js
from modules.hooks.use_navigation import use_navigation
from modules.ui.ui_game import ui_game
from modules.ui.ui_menu_start import ui_menu_start
from modules.ui.ui_navigate import ui_navigate
from modules.assets import about_text
from modules.assets import help_text
from modules.helpers import prompt


def ui_app():
    """ui entrypoint of the app"""
    navigator = use_navigation("start")

    # basically a router
    match navigator["get_path"]():
        case "start":
            ui_menu_start(navigator)
        case "start/main_menu":
            ui_navigate(
                navigator,
                "select an alternative: ",
                (
                    ("play local", "play_local"),
                    ("play online (coming soon)", "play_online"),
                    ("about", "about"),
                    ("help", "help"),
                ),
            )
        case "start/main_menu/about":
            print(about_text)
            prompt("press enter to go back")
            navigator["go_back"]()
        case "start/main_menu/help":
            print(help_text)
            prompt("press enter to go back")
            navigator["go_back"]()
        case "start/main_menu/play_local":
            ui_game(navigator)
