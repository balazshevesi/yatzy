# file for storing the scoring logic for yatzy
# reference: https://en.wikipedia.org/wiki/Yatzy#Scoring


def get_one_pair(thrown_d) -> int:
    return_value = 0
    for i in range(1, 7, 1):
        if thrown_d.count(i) >= 2:
            pair_sum = i * 2
            if pair_sum > return_value:
                return_value = pair_sum
    return return_value


def get_two_pair(thrown_d) -> int:
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


def get_three_of_a_kind(thrown_d) -> int:
    return_value = 0
    for i in range(1, 7, 1):
        if thrown_d.count(i) >= 3:
            three_o_a_k_sum = i * 3
            if three_o_a_k_sum > return_value:
                return_value = three_o_a_k_sum
    return return_value


def get_four_of_a_kind(thrown_d) -> int:
    return_value = 0
    for i in range(1, 7, 1):
        if thrown_d.count(i) >= 4:
            four_o_a_k_sum = i * 4
            if four_o_a_k_sum > return_value:
                return_value = four_o_a_k_sum
    return return_value


def get_small_straight(thrown_d) -> int:
    required_numbers = {1, 2, 3, 4, 5}
    if required_numbers.issubset(thrown_d):
        return 15
    return 0


def get_large_straight(thrown_d) -> int:
    required_numbers = {2, 3, 4, 5, 6}
    if required_numbers.issubset(thrown_d):
        return 20
    return 0


def get_full_house(thrown_d) -> int:
    three_of_a_kind_sum = get_three_of_a_kind(thrown_d)
    pair_sum = get_one_pair(thrown_d)

    if three_of_a_kind_sum == 0 or pair_sum == 0:
        return 0
    if three_of_a_kind_sum // 3 == pair_sum // 2:
        return 0
    return three_of_a_kind_sum + pair_sum


def get_chance(thrown_d) -> int:
    return sum(thrown_d)


def get_yatzy(thrown_d) -> int:
    if len(set(thrown_d)) == 1:  # All dice are the same
        return 50
    return 0


def get_upper_section_bonus(scorecard) -> int:
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


def get_total_p(scorecard) -> int:
    total = 0
    for k, v in scorecard.items():
        if v is not None:
            total += v
    total += get_upper_section_bonus(scorecard)
    return total
