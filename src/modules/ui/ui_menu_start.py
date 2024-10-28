from modules.helpers import prompt
from modules import renderer as r
from modules.assets import yatzy_banner
import json
import time


def sort_high_scores():
    with open("high_scores.json", "r+") as file:
        json_data = json.load(file)
        json_data["high_scores"].sort(key=lambda x: x[1], reverse=True)
        file.seek(0)
        json.dump(json_data, file, indent=4)
        file.truncate()


def get_high_score():
    with open("high_scores.json", "r") as file:
        data = json.load(file)
    return data


def ui_menu_start(navigator):
    sort_high_scores()
    high_score_data = get_high_score()

    art = yatzy_banner
    art_lines = art.split("\n")
    for line in art_lines:
        print(line)
        time.sleep(0.05)

    print(f"{' h i g h   s c o r e s '.upper():^60}")
    print()
    for scores in high_score_data["high_scores"][:5]:
        print(f"{scores[0] + " (" + scores[2][:10] + ") - " +str(scores[1]):^60}")
    print()
    prompt(f"{'p r e s s   e n t e r   t o   s t a r t '.upper():^60}")
    navigator["go_forward"]("main_menu")
