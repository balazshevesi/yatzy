from modules.helpers import (
    prompt,
    get_score_one_pair,
    get_score_two_pair,
    get_three_of_a_kind,
    get_chance,
    get_full_house,
    get_large_straight,
    get_small_straight,
    get_upper_section_bonus,
    get_yatzy,
)
from modules import renderer as r
from modules.assets import yatzy_banner
from datetime import datetime
from ..assets import dice
import random as rnd

import time


def throw_dice():
    return rnd.randint(1, 6)


def make_dice_pretty(dice_lst, locked_dice_lst):
    sprite_height = 6
    sprite_width = 11

    final_string = ""

    for i in range(1, sprite_height, 1):
        final_string += f"{str(i) + (' LOCKED' if locked_dice_lst[i - 1] else ''):^11}"

    for i in range(sprite_height):  # loop through the height of the sprite
        for e in dice_lst:  # loop through all the dice
            final_string += dice[e - 1].split("\n")[i]
        final_string += "\n"  # after each line is complete, add a new-line character
    return final_string


def roll_dice(set_thrown_d, thrown_d, locked_d, set_d_rerolls, d_rerolls):
    set_thrown_d(
        [
            throw_dice() if not locked_d[0] else thrown_d[0],
            throw_dice() if not locked_d[1] else thrown_d[1],
            throw_dice() if not locked_d[2] else thrown_d[2],
            throw_dice() if not locked_d[3] else thrown_d[3],
            throw_dice() if not locked_d[4] else thrown_d[4],
        ]
    )
    set_d_rerolls(d_rerolls + 1)


def get_scoreboard_template():
    return {
        "ones": None,  # the sum of all dice showing the number 1
        "twos": None,  # the sum of all dice showing the number 2
        "threes": None,  # the sum of all dice showing the number 3
        "fours": None,  # the sum of all dice showing the number 4
        "fives": None,  # the sum of all dice showing the number 5
        "sixes": None,  # the sum of all dice showing the number 6
        "one_pair": None,  # two dice showing the same number, score: sum of those two dice
        "two_pair": None,  # two different pairs of dice. score: sum of dice in those two pairs
        "three_of_a_kind": None,  # three dice showing the same number, score: sum of those three dice
        "four_of_a_kind": None,  # four dice with the same number, score: Sum of those four dice
        "small_straight": None,  # the combination 1-2-3-4-5, score: 15 points (sum of all the dice)
        "large_straight": None,  # the combination 2-3-4-5-6, score: 20 points (sum of all the dice)
        "full_house": None,  # any set of three combined with a different pair, score: Sum of all the dice
        "chance": None,  # any combination of dice, score: sum of all the dice
        "yatzy": None,  # all five dice with the same number, score: 50 points
    }


def get_scoreboard_status(score_board, thrown_d):
    ones = thrown_d.count(1) * 1
    twos = thrown_d.count(2) * 2
    threes = thrown_d.count(3) * 3
    fours = thrown_d.count(4) * 4
    fives = thrown_d.count(5) * 5
    sixes = thrown_d.count(6) * 6
    one_pair = get_score_one_pair(thrown_d)
    two_pair = get_score_two_pair(thrown_d)
    three_of_a_kind = get_three_of_a_kind(thrown_d)
    small_straight = get_small_straight(thrown_d)
    large_straight = get_large_straight(thrown_d)
    full_house = get_full_house(thrown_d)
    chance = get_chance(thrown_d)
    yatzy = get_yatzy(thrown_d)
    upper_section_bonus = get_upper_section_bonus(thrown_d)


def ui_game(navigator):
    game_difficulty, set_game_difficulty = r.use_state(None)

    game_is_running, set_game_is_running = r.use_state(False)
    is_players_turn, set_is_players_turn = r.use_state(True)

    # initiate state for dice
    d_rerolls, set_d_rerolls = r.use_state(0)
    thrown_d, set_thrown_d = r.use_state([])
    locked_d, set_locked_d = r.use_state([False, False, False, False, False])
    d_need_rolling, set_d_need_rolling = r.use_state(True)

    all_scoreboards, set_all_scoreboards = r.use_state(
        [get_scoreboard_template(), get_scoreboard_template()]
    )

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

    if game_is_running() and is_players_turn():
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

        usr_input = prompt(
            "press enter to re-roll or input the index of the dice you wish to lock or unlock: "
        )
        if not usr_input == "":
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
        else:
            set_d_need_rolling(True)
