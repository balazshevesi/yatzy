from modules.prompt import prompt
from modules import renderer as r
from modules.assets import yatzy_banner

import time


def ui_menu_start(navigator):
    art = yatzy_banner
    art_lines = art.split("\n")
    for line in art_lines:
        print(line)
        time.sleep(0.05)

    prompt(f"{'p r e s s   e n t e r   t o   s t a r t '.upper():^60}")
    navigator["go_forward"]("main_menu")
