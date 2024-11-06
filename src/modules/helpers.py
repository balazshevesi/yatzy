import random as rnd

from modules.scoring import *
from .assets import dice


def prompt(str: str):
    """input wrapper, let's the user exit the program whenever"""
    input_value = input(str)
    match input_value:
        case "exit" | "quit" | "close" | ":q":
            raise SystemExit
    return input_value


def get_longest_s_in_lst(lst):
    """returns the longest string in a list"""
    longest_string = ""
    for string in lst:
        if len(string) > len(longest_string):
            longest_string = string
    return longest_string


def create_scorecard():
    """
    returns a dict with all the possible combinations as keys
    since these scorecards are blank at first, all the values are set to None
    """

    return {
        "ones": 11,  # the sum of all dice showing the number 1
        "twos": 11,  # the sum of all dice showing the number 2
        "threes": 11,  # the sum of all dice showing the number 3
        "fours": 11,  # the sum of all dice showing the number 4
        "fives": 11,  # the sum of all dice showing the number 5
        "sixes": 11,  # the sum of all dice showing the number 6
        "one_pair": 11,  # two dice showing the same number, score: sum of those two dice
        "two_pair": 11,  # two different pairs of dice. score: sum of dice in those two pairs
        "three_of_a_kind": 11,  # three dice showing the same number, score: sum of those three dice
        "four_of_a_kind": 11,  # four dice with the same number, score: Sum of those four dice
        "small_straight": 11,  # the combination 1-2-3-4-5, score: 15 points (sum of all the dice)
        "large_straight": 11,  # the combination 2-3-4-5-6, score: 20 points (sum of all the dice)
        "full_house": 11,  # any set of three combined with a different pair, score: Sum of all the dice
        "chance": 11,  # any combination of dice, score: sum of all the dice
        "yatzy": None,  # all five dice with the same number, score: 50 points
        # "upper_section_bonus": None,  # all five dice with the same number, score: 50 points
    }


def get_checked_scorecard(scoreboard, thrown_d):
    """
    returns a dictionary that includes the same keys as "create_scorecard()"
    the values for the keys are the points that that combination of dice will yield if they are chosen
    if the value returned a key is None, then that's because the scoreboard already has that combination locked-in
    """

    return {
        "ones": thrown_d.count(1) * 1 if scoreboard["ones"] is None else None,
        "twos": thrown_d.count(2) * 2 if scoreboard["twos"] is None else None,
        "threes": thrown_d.count(3) * 3 if scoreboard["threes"] is None else None,
        "fours": thrown_d.count(4) * 4 if scoreboard["fours"] is None else None,
        "fives": thrown_d.count(5) * 5 if scoreboard["fives"] is None else None,
        "sixes": thrown_d.count(6) * 6 if scoreboard["sixes"] is None else None,
        "one_pair": (
            get_one_pair(thrown_d) if scoreboard["one_pair"] is None else None
        ),
        "two_pair": (
            get_two_pair(thrown_d) if scoreboard["two_pair"] is None else None
        ),
        "three_of_a_kind": (
            get_three_of_a_kind(thrown_d)
            if scoreboard["three_of_a_kind"] is None
            else None
        ),
        "four_of_a_kind": (
            get_four_of_a_kind(thrown_d)
            if scoreboard["four_of_a_kind"] is None
            else None
        ),
        "small_straight": (
            get_small_straight(thrown_d)
            if scoreboard["small_straight"] is None
            else None
        ),
        "large_straight": (
            get_large_straight(thrown_d)
            if scoreboard["large_straight"] is None
            else None
        ),
        "full_house": (
            get_full_house(thrown_d) if scoreboard["full_house"] is None else None
        ),
        "chance": get_chance(thrown_d) if scoreboard["chance"] is None else None,
        "yatzy": get_yatzy(thrown_d) if scoreboard["yatzy"] is None else None,
        # "upper_section_bonus": (get_upper_section_bonus(thrown_d)),
    }


def make_scorecards_pretty(all_scorecards, players, p_turn_i, thrown_d) -> str:
    """returns a table of all the scorecards, shows and "X" next to the combination that has already been chosen"""

    rs = ""

    table_l_side_width = 17
    player_n_width = len(get_longest_s_in_lst(players)) + 5

    # header of the table
    rs += f"{' ' : <{table_l_side_width-1}}┃"
    for name in players:
        rs += f"{name:^{player_n_width-1}}┃"
    rs += "\n"

    # contents of the table
    for i, (k, v) in enumerate(create_scorecard().items()):
        rs += f"{k:{" "}<{table_l_side_width-2}} ┃"
        for it, name in enumerate(players):
            # if combination is already checked
            if get_checked_scorecard(all_scorecards[it], thrown_d)[k] is None:
                rs += f"{(str(all_scorecards[it][k]) + " X"):^{player_n_width-1}}┃"
            elif it == p_turn_i:  # if combination is not the current players turn
                rs += f"{get_checked_scorecard(all_scorecards[it], thrown_d)[k]:^{player_n_width-1}}┃"
            else:  # if combination is not the current players turn
                rs += f"{" ":^{player_n_width-1}}┃"
        rs += "\n"

    # bonus row of table
    rs += f"{"bonus" : <{table_l_side_width-1}}┃"
    for i, name in enumerate(players):
        rs += f"{get_upper_section_bonus(all_scorecards[i]):^{player_n_width-1}}┃"
    rs += "\n"

    # total row of table
    rs += f"{"total" : <{table_l_side_width-1}}┃"
    for i, name in enumerate(players):
        rs += f"{get_total_p(all_scorecards[i]):^{player_n_width-1}}┃"
    rs += "\n"

    return rs


def scorecards_are_filled(all_scorecards: list) -> bool:
    """returns true if all scorecards are filled, meaning if the game is finished"""

    vals = []
    for scorecard in all_scorecards:
        for k, v in create_scorecard().items():
            vals.append(scorecard[k])
    if not None in vals:
        return True
    return False


def make_dice_pretty(dice_lst, locked_dice_lst):
    """returns a big string that all the dice"""

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
    """rolls the dice, and also updates their state"""

    def throw_dice():
        return rnd.randint(1, 6)

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
