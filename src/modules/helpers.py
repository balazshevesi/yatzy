def prompt(str: str):
    input_value = input(str)
    match input_value:
        case "exit" | "quit" | "close" | ":q":
            quit()
    return input_value


# * yatzy score helpers:


def get_score_one_pair(thrown_d):
    return_value = 0
    for i in range(1, 7, 1):
        if thrown_d.count(i) >= 2:
            pair_sum = i * 2
            if pair_sum > return_value:
                return_value = pair_sum
    return return_value


def get_score_two_pair(thrown_d):
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
    pair_sum = get_score_one_pair(thrown_d)
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
    return 50


def get_upper_section_bonus(thrown_d):
    bonus_sum += thrown_d.count(1) * 1
    bonus_sum += thrown_d.count(2) * 2
    bonus_sum += thrown_d.count(3) * 3
    bonus_sum += thrown_d.count(4) * 4
    bonus_sum += thrown_d.count(5) * 5
    bonus_sum += thrown_d.count(6) * 6
    if bonus_sum >= 63:
        return 50
