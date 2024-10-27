from modules.helpers import *
from modules import renderer as r
from modules.assets import yatzy_banner
from datetime import datetime
from ..assets import dice
import random as rnd

import time


def get_total_p_from_scorecard(scoreboard):
    total = 0
    for k, v in scoreboard.items():
        if v is not None:
            total += v
    total += get_upper_section_bonus(scoreboard)
    return total


def scorecards_are_filled(all_scorecards):
    filled_in_score_cards = []
    for scorecard in all_scorecards:
        scorecard_is_fully_filled_in = False
        scorecard_values = []
        empty_score_card = create_scorecard()
        for k, v in empty_score_card.items():
            scorecard_values.append(scorecard[k])
        if None in scorecard_values:
            filled_in_score_cards.append(False)
        else:
            filled_in_score_cards.append(True)
    if not False in filled_in_score_cards:
        return True
    return False


def make_scorecard_pretty(checked_scorecard, scorecard):
    return_string = ""
    for k, v in checked_scorecard.items():
        if v is None:
            return_string += f"{k:{"_"}<16}{scorecard[k]:<2} LOCKED \n"
        elif not k == "upper_section_bonus":
            return_string += f"{k:{"_"}<16}{v:<5} \n"
    return_string += f"{'total':{"_"}<16}{get_total_p_from_scorecard(scorecard):<5} \n"
    return return_string


def ui_game(navigator):
    game_difficulty, set_game_difficulty = r.use_state(None)

    players, set_players = r.use_state(["balazs", "johnnyD.", "john pork"])
    p_turn_i, set_p_turn_i = r.use_state(0)
    game_is_running, set_game_is_running = r.use_state(False)

    # initiate state for dice
    d_rerolls, set_d_rerolls = r.use_state(0)
    thrown_d, set_thrown_d = r.use_state([])
    locked_d, set_locked_d = r.use_state([False, False, False, False, False])
    d_need_rolling, set_d_need_rolling = r.use_state(True)

    all_scorecards, set_all_scorecards = r.use_state([create_scorecard()])

    def init_player_scorecards():
        
        pass

    r.use_effect()

    # initiate state for datetime
    date_time, set_date_time = r.use_state()
    r.use_effect(lambda: set_date_time(datetime.now().strftime("%d-%m-%Y_%H:%M:%S")))

    err_msg, set_err_msg = r.use_state("")

    # set difficulty
    if not game_is_running():
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
            if usr_input > 2 or usr_input < 0:
                set_err_msg("please pick a valid number")
                # navigator["reload"]()
            else:
                set_err_msg("")
                set_game_difficulty(usr_input)
                set_game_is_running(True)
                return
        except:
            set_err_msg("please pick a valid number")

    # check if game is finished
    if scorecards_are_filled(all_scorecards()):
        set_game_is_running(False)
        print(all_scorecards())
        prompt("ya done")

    if game_is_running():
        if d_need_rolling():
            roll_dice(
                set_thrown_d=set_thrown_d,
                thrown_d=thrown_d(),
                locked_d=locked_d(),
                set_d_rerolls=set_d_rerolls,
                d_rerolls=d_rerolls(),
            )
        print("you got:", end="\n\n")
        print(make_dice_pretty(thrown_d(), locked_d()))

        print(f"{d_rerolls()-1}/2 rerolls used", end="\n\n")

        print("your scorecard:")
        print(
            make_scorecard_pretty(
                get_checked_scorecard(all_scorecards()[0], thrown_d()),
                all_scorecards()[0],
            )
        )

        # if bool(err_msg()):
        #     print(err_msg())
        prompt_text = (
            "press enter to re-roll, specify dice indices to lock/unlock, or "
            if d_rerolls() <= 2
            else ""
        )
        prompt_text += "type a combination name to select: "
        usr_input = prompt(prompt_text)

        # if input is combination name
        if usr_input in create_scorecard():
            set_d_need_rolling(False)
            new_scorecard_state = {}
            for k, v in all_scorecards()[0].items():
                if k == usr_input:
                    if all_scorecards()[0][k] is None:
                        new_scorecard_state[k] = get_checked_scorecard(
                            all_scorecards()[0], thrown_d()
                        )[usr_input]
                        set_d_need_rolling(True)
                        set_d_rerolls(0)
                        set_locked_d([False, False, False, False, False])
                    else:
                        new_scorecard_state[k] = v
                else:
                    new_scorecard_state[k] = v
            set_all_scorecards([new_scorecard_state])

        # if input is lock-in or unlock
        elif not usr_input == "":
            set_d_need_rolling(False)
            indexes_to_switch = []
            for c in list(usr_input):
                if c.isnumeric():
                    indexes_to_switch.append(int(c) - 1)
            new_state = []
            for i, e in enumerate(locked_d()):
                if i in indexes_to_switch:
                    new_state.append(not e)
                else:
                    new_state.append(e)
            set_locked_d(new_state)
        # if input is re-roll
        else:
            if d_rerolls() <= 2:
                set_d_need_rolling(True)
            else:
                set_d_need_rolling(False)
