import random as rnd
from .assets import dice


def prompt(str: str):
    input_value = input(str)
    match input_value:
        case "exit" | "quit" | "close" | ":q":
            quit()
    return input_value


# * yatzy score helpers:


def get_one_pair(thrown_d):
    return_value = 0
    for i in range(1, 7, 1):
        if thrown_d.count(i) >= 2:
            pair_sum = i * 2
            if pair_sum > return_value:
                return_value = pair_sum
    return return_value


def get_two_pair(thrown_d):
    first_pair_sum = 0
    for i in range(1, 7, 1):
        if thrown_d.count(i) == 2:
            pair_sum = i * 2
            if pair_sum > first_pair_sum:
                first_pair_sum = pair_sum
    second_pair_sum = 0
    for i in range(1, 7, 1):
        if thrown_d.count(i) == 2 and not i * 2 == first_pair_sum:
            pair_sum = i * 2
            if pair_sum > second_pair_sum:
                second_pair_sum = pair_sum
    if first_pair_sum == 0 or second_pair_sum == 0:  # if it's only a one pair, return 0
        return 0
    return first_pair_sum + second_pair_sum


def get_three_of_a_kind(thrown_d):
    return_value = 0
    for i in range(1, 7, 1):
        if thrown_d.count(i) >= 3:
            three_o_a_k_sum = i * 3
            if three_o_a_k_sum > return_value:
                return_value = three_o_a_k_sum
    return return_value


def get_four_of_a_kind(thrown_d):
    return_value = 0
    for i in range(1, 7, 1):
        if thrown_d.count(i) >= 4:
            four_o_a_k_sum = i * 4
            if four_o_a_k_sum > return_value:
                return_value = four_o_a_k_sum
    return return_value


def get_small_straight(thrown_d):
    required_numbers = {1, 2, 3, 4, 5}
    if required_numbers.issubset(thrown_d):
        return 15
    return 0


def get_large_straight(thrown_d):
    required_numbers = {2, 3, 4, 5, 6}
    if required_numbers.issubset(thrown_d):
        return 20
    return 0


def get_full_house(thrown_d):
    three_of_a_kind_sum = get_three_of_a_kind(thrown_d)
    pair_sum = get_one_pair(thrown_d)
    if three_of_a_kind_sum == 0 or pair_sum == 0:
        return 0
    if three_of_a_kind_sum / 3 == pair_sum / 2:
        return 0
    return three_of_a_kind_sum + pair_sum


def get_chance(thrown_d):
    sum = 0
    for e in thrown_d:
        sum += e
    return sum


def get_yatzy(thrown_d):
    is_yatzy = (
        thrown_d.count(1) == 5
        or thrown_d.count(2) == 5
        or thrown_d.count(3) == 5
        or thrown_d.count(4) == 5
        or thrown_d.count(5) == 5
        or thrown_d.count(6) == 5
    )
    if is_yatzy:
        return 50
    else:
        return 0


def get_upper_section_bonus(scorecard):
    bonus_sum = 0
    for k, v in scorecard.items():
        match k:
            case "ones" | "twos" | "threes" | "fours" | "fives" | "sixes":
                if v is not None:
                    bonus_sum += v
    if bonus_sum >= 63:
        return 50
    else:
        return 0


# * yatzy scorecard helpers


def create_scorecard():
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
        # "upper_section_bonus": None,  # all five dice with the same number, score: 50 points
    }


# returns a dictionary that includes the same keys as "create_scorecard()"
# the values are the points that that combination of dice would yield
# if the value returned any key is None, then that's because the scoreboard already has that combination locked-in
def get_checked_scorecard(scoreboard, thrown_d):
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


# * dice helpers


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
