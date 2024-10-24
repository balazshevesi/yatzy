from modules import renderer as r
import time


def ui_menu_start(navigator):
    print(
        """
  ___    ___ ________  _________  ________      ___    ___ 
 |\  \  /  /|\   __  \|\___   ___|\_____  \    |\  \  /  /|
 \ \  \/  / \ \  \|\  \|___ \  \_|\|___/  /|   \ \  \/  / /
  \ \    / / \ \   __  \   \ \  \     /  / /    \ \    / / 
   \/  /  /   \ \  \ \  \   \ \  \   /  /_/__    \/  /  /  
 __/  / /      \ \__\ \__\   \ \__\ |\________\__/  / /    
|\___/ /        \|__|\|__|    \|__|  \|_______|\___/ /     
\|___|/                                       \|___|/      
"""
    )
    input(f"{'p r e s s   e n t e r   t o   s t a r t '.upper():^60}")
    navigator["go_forward"]("main_menu")


def ui_navigate(navigator, question: str, lst_of_alts: list):
    err_msg, set_err_msg = r.use_state("")

    print(question)
    print()
    print("0 - back")
    for i, e in enumerate(lst_of_alts):
        print(f"{i+1} - {e[0]}")
    print()
    print(err_msg())
    usr_input = input("enter your choice: ")
    try:
        usr_input = int(usr_input)
        lst_of_alts[usr_input - 1]
        if usr_input == 0:
            set_err_msg("")
            navigator["go_back"]()
        else:
            set_err_msg("")
            navigator["go_forward"](lst_of_alts[usr_input - 1][1])

    except:
        navigator["reload"]()
        set_err_msg("Please enter a valid number")
        pass


def use_navigation(initial_path: str):
    nav, set_nav = r.use_state(initial_path)

    def go_back():
        back_state_value = nav().split("/")
        back_state_value.pop()
        set_nav("/".join(back_state_value))

    def go_forward(path: str):
        forward_state_value = nav() + "/" + path
        set_nav(forward_state_value)

    def reload():
        set_nav(nav())

    return {
        "get_path": nav,
        "set_path": set_nav,
        "go_back": go_back,
        "go_forward": go_forward,
        "reload": reload,
    }


def ui_entry_point():
    navigator = use_navigation("start")

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
                (("play", "play"), ("credits", "credits")),
            )
        case "start/main_menu/play":
            ui_navigate(
                navigator,
                "Select an alternative: ",
                (
                    ("play against computer", "pvc"),
                    ("play against player", "pvp"),
                ),
            )


def main():
    r.render(ui_entry_point)


if __name__ == "__main__":
    main()
