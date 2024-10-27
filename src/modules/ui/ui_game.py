from modules.helpers import *
from modules import renderer as r
from modules.assets import yatzy_banner
from datetime import datetime
from ..assets import dice
import random as rnd

import time


def get_total_p(scoreboard):
    total = 0
    for k, v in scoreboard.items():
        if v is not None:
            total += v
    total += get_upper_section_bonus(scoreboard)
    return total


def scorecards_are_filled(all_scorecards):
    if all_scorecards is not type(all_scorecards) == list:
        return False
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


def make_scorecards_pretty(all_scorecards, players, p_turn_i, thrown_d):
    rs = ""

    table_l_side_width = 17
    player_n_width = 12

    # header of the table
    rs += f"{' ' : <{table_l_side_width-1}}|"
    for name in players:
        rs += f"{name:^{player_n_width-1}}|"
    rs += "\n"

    # # contents of the table
    for i, (k, v) in enumerate(create_scorecard().items()):
        rs += f"{k:{" "}<{table_l_side_width-2}} |"
        for it, name in enumerate(players):
            # if combination is already checked
            if get_checked_scorecard(all_scorecards[it], thrown_d)[k] is None:
                rs += f"{(str(all_scorecards[it][k]) + " X"):^{player_n_width-1}}|"
            elif it == p_turn_i:
                rs += f"{get_checked_scorecard(all_scorecards[it], thrown_d)[k]:^{player_n_width-1}}|"
            else:
                rs += f"{" ":^{player_n_width-1}}|"
        rs += "\n"

    # final line of the table
    rs += f"{"total" : <{table_l_side_width-1}}|"
    for i, name in enumerate(players):
        rs += f"{get_total_p(all_scorecards[i]):^{player_n_width-1}}|"
    rs += "\n"

    # rs += f"{'total':{" "}<16}| {get_total_p_from_scorecard(scorecard):<5} \n"
    # for p in players:
    #     rs += f"{p:{" "}>16}"

    return rs


def ui_game(navigator):
    game_difficulty, set_game_difficulty = r.use_state(None)

    players, set_players = r.use_state(["balazs", "johnny d", "john pork"])
    p_turn_i, set_p_turn_i = r.use_state(0)
    game_is_running, set_game_is_running = r.use_state(False)

    # initiate state for dice
    d_rerolls, set_d_rerolls = r.use_state(0)
    thrown_d, set_thrown_d = r.use_state([])
    locked_d, set_locked_d = r.use_state([False, False, False, False, False])
    d_need_rolling, set_d_need_rolling = r.use_state(True)

    all_scorecards, set_all_scorecards = r.use_state()

    def init_player_scorecards():
        new_state_for_all_scorecards = []
        for i in players():
            new_state_for_all_scorecards.append(create_scorecard())
        set_all_scorecards(new_state_for_all_scorecards)

    r.use_effect(init_player_scorecards, [players()])

    def rotate_players():
        set_p_turn_i((p_turn_i() + 1) % len(players()))

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

        # print(f"{players()[p_turn_i()]}'s scorecard:")
        print(
            make_scorecards_pretty(
                # get_checked_scorecard(all_scorecards()[p_turn_i()], thrown_d()),
                # all_scorecards()[p_turn_i()],
                # players(),
                # p_turn_i(),
                all_scorecards(),
                players(),
                p_turn_i(),
                thrown_d(),
            )
        )

        print(f"it's {players()[p_turn_i()]}'s turn!")
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
            players_new_scorecard = {}
            for k, v in all_scorecards()[p_turn_i()].items():
                if k == usr_input:
                    if all_scorecards()[p_turn_i()][k] is None:
                        players_new_scorecard[k] = get_checked_scorecard(
                            all_scorecards()[p_turn_i()], thrown_d()
                        )[usr_input]
                        set_d_need_rolling(True)
                        set_d_rerolls(0)
                        set_locked_d([False, False, False, False, False])
                    else:
                        players_new_scorecard[k] = v
                else:
                    players_new_scorecard[k] = v
            new_scorecard_state = all_scorecards()
            new_scorecard_state[p_turn_i()] = players_new_scorecard
            set_all_scorecards(new_scorecard_state)
            if not all_scorecards()[p_turn_i()] == new_scorecard_state:
                rotate_players()

        # if input is lock-in or unlock
        elif not usr_input == "":
            set_d_need_rolling(False)
            indexes_to_switch = []
            for c in list(usr_input):
                if c.isnumeric():
                    indexes_to_switch.append(int(c) - 1)
            new_scorecard_state = []
            for i, e in enumerate(locked_d()):
                if i in indexes_to_switch:
                    new_scorecard_state.append(not e)
                else:
                    new_scorecard_state.append(e)
            set_locked_d(new_scorecard_state)
        # if input is re-roll
        else:
            if d_rerolls() <= 2:
                set_d_need_rolling(True)
            else:
                set_d_need_rolling(False)
