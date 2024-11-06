from modules.helpers import prompt
from modules import renderer as r


def ui_navigate(navigator, question: str, lst_of_alts: list):
    err_msg, set_err_msg = r.use_state("")

    print(question)
    print()
    print("0 - back")
    for i, e in enumerate(lst_of_alts):
        print(f"{i+1} - {e[0]}")
    print()
    print(err_msg())
    usr_input = prompt("enter your choice: ")
    try:
        usr_input = int(usr_input)
        lst_of_alts[usr_input - 1]
        if usr_input == 0:
            set_err_msg("")
            navigator["go_back"]()
        else:
            set_err_msg("")
            navigator["go_forward"](lst_of_alts[usr_input - 1][1])
            return usr_input
    except:
        navigator["reload"]()
        set_err_msg("please enter a valid number")
