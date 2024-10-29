from modules.helpers import *
from modules import renderer as r
from modules.assets import yatzy_banner
from datetime import datetime
from ..assets import dice
import random as rnd

import time
import json


def add_score_to_file(name: str, score: int):
    now = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    with open("high_scores.json", "r+") as file:
        json_data = json.load(file)
        json_data["high_scores"].append([name, score, now])
        json_data["high_scores"].sort(key=lambda x: x[1], reverse=True)
        file.seek(0)
        json.dump(json_data, file, indent=4)
        file.truncate()


def ui_game(navigator):
    players, set_players = r.use_state([""])
    p_turn_i, set_p_turn_i = r.use_state(0)
    game_is_running, set_game_is_running = r.use_state(False)

    # initiate state for dice
    d_rerolls, set_d_rerolls = r.use_state(0)
    thrown_d, set_thrown_d = r.use_state([])
    locked_d, set_locked_d = r.use_state([False, False, False, False, False])
    d_need_rolling, set_d_need_rolling = r.use_state(True)

    all_scorecards, set_all_scorecards = r.use_state([create_scorecard()])

    def init_player_scorecards():
        new_state_for_all_scorecards = []
        for i in players():
            new_state_for_all_scorecards.append(create_scorecard())
        set_all_scorecards(new_state_for_all_scorecards)

    def check_comb_on_scorecard(input_comb: str) -> str:
        set_d_need_rolling(False)
        updated_scorecard = all_scorecards()[p_turn_i()].copy()

        # if input_comb is a valid key for the scorecard, and if it's already checked
        if input_comb in updated_scorecard and updated_scorecard[input_comb] is None:
            # Update the specific combination score
            updated_scorecard[input_comb] = get_checked_scorecard(
                updated_scorecard, thrown_d()
            )[input_comb]

            # Reset dice and reroll state
            set_d_need_rolling(True)
            set_d_rerolls(0)
            set_locked_d([False, False, False, False, False])

            # Update the full scorecard list with the modified player scorecard
            all_scores = all_scorecards()
            all_scores[p_turn_i()] = updated_scorecard
            set_all_scorecards(all_scores)
            rotate_players()
            return "successfully checked"
        elif input_comb not in updated_scorecard:
            return "invalid combination name"
        elif updated_scorecard[input_comb] is None:
            return "combination is already checked"

    # r.use_effect(init_player_scorecards, [players()])

    def rotate_players():
        set_p_turn_i((p_turn_i() + 1) % len(players()))

        # handle bot stuffs
        match players()[p_turn_i()]:
            case "bot_easy" | "bot_normal" | "bot_hard":
                # TODO write code for bot all different bots

                # this is a recursive function, it does not have a base-case, but in it should never loop infinitely as long as "scorecards_are_filled" works and is correctly called
                def check_scorecard():
                    score_card_len = len(create_scorecard())
                    random_key_index = rnd.randint(0, score_card_len - 1)
                    random_key = list(create_scorecard().keys())[random_key_index]
                    if check_comb_on_scorecard(random_key) != "successfully checked":
                        check_scorecard()

                check_scorecard()

    # initiate state for datetime
    date_time, set_date_time = r.use_state()
    r.use_effect(lambda: set_date_time(datetime.now().strftime("%d-%m-%Y_%H:%M:%S")))

    err_msg, set_err_msg = r.use_state("")

    # set players
    if not game_is_running():
        usr_input = prompt(
            "Enter player names separated by commas. To add bots, use 'bot_easy', 'bot_normal', or 'bot_hard': "
        )
        set_players([player_name.strip() for player_name in usr_input.split(",")])
        set_game_is_running(True)
        init_player_scorecards()
        return  # needs to be returned in-order for the effect (that sets the scorecards) to run, otherwise there will be an error :(

    # check if game is finished
    if scorecards_are_filled(all_scorecards()) and game_is_running():
        set_game_is_running(False)
        print("players()", players())
        print("all_scorecards()", all_scorecards())
        for i, player in enumerate(players()):
            add_score_to_file(player, get_total_p(all_scorecards()[i]))
            pass
        # TODO print who actually won
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

        print(
            make_scorecards_pretty(
                all_scorecards(),
                players(),
                p_turn_i(),
                thrown_d(),
            )
        )

        if err_msg():
            print(err_msg())
        print(f"it's {players()[p_turn_i()]}'s turn!")
        prompt_text = (
            "press enter to re-roll, specify dice indices to lock/unlock, or "
            if d_rerolls() <= 2
            else ""
        )
        prompt_text += "type a combination name to select: "
        usr_input = prompt(prompt_text)
        set_err_msg("")

        # if input is combination name
        if usr_input in create_scorecard():
            check_comb_on_scorecard(usr_input)

        # if input is lock-in / unlock
        elif not usr_input == "":
            set_d_need_rolling(False)
            indexes_to_switch = []
            for c in list(usr_input):
                if c.isnumeric():
                    indexes_to_switch.append(int(c) - 1)
            if len(indexes_to_switch) == 0:
                set_err_msg(
                    "please enter a numeric value if you want to lock/unlock the dice"
                )
            new_l_d_state = []
            for i, e in enumerate(locked_d()):
                if i in indexes_to_switch:
                    new_l_d_state.append(not e)
                else:
                    new_l_d_state.append(e)
            set_locked_d(new_l_d_state)
        # if input is re-roll
        else:
            if d_rerolls() <= 2:
                set_d_need_rolling(True)
            else:
                set_d_need_rolling(False)
