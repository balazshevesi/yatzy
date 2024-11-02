from modules.helpers import prompt
from modules import file_operations as f_op
from modules.assets import yatzy_banner
import time


def ui_menu_start(navigator):
    """the start screen"""

    f_op.sort_high_scores()
    high_score_data = f_op.get_high_score()

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
