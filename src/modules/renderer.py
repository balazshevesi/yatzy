import os

ui_entry_func = None
rerender_needed = False

all_state = []
state_cursor = 0

all_effects = []
effects_cursor = 0


def clear_terminal():
    os.system("cls" if os.name == "nt" else "printf '\033c'")


def use_effect(func, dependencies=[]):
    global effects_cursor
    global all_effects

    if not len(all_effects) - 1 >= effects_cursor:
        all_effects.append([func, dependencies])
        if len(dependencies) == 0:
            func()
    else:
        changed = False
        for i, d in enumerate(dependencies):
            if d != all_effects[effects_cursor][1]:
                changed = True
                all_effects[effects_cursor][1] = d
        if changed:
            func()

    effects_cursor += 1


def use_state(initial_state="") -> tuple:
    """function for creating game state, first arg: key, second arg: state"""
    global state_cursor
    global all_state
    # we freeze the cursor because we want the current value for state_cursor to be stored within the create_state closure
    frozen_cursor = state_cursor

    # if a state element does not already exists for the state_cursor
    if not len(all_state) - 1 >= state_cursor:
        all_state.append(initial_state)

    def get_state() -> dict:
        """remember to always call the function to get the value"""
        global all_state
        return all_state[frozen_cursor]

    def update_state(new_state: dict) -> None:
        """remember to always call the function with the new value"""
        global all_state
        global rerender_needed
        rerender_needed = True
        all_state[frozen_cursor] = new_state
        # rerender()

    state_cursor += 1

    return get_state, update_state


def rerender():
    """reset the cursor and clear terminal, then call the entry function to render UI"""
    global state_cursor, effects_cursor
    state_cursor = 0
    effects_cursor = 0
    clear_terminal()
    # print(all_state)
    ui_entry_func()


def render(ui_entry_func_param):
    """initial render function to start the UI rendering cycle"""
    global ui_entry_func
    ui_entry_func = ui_entry_func_param
    global rerender_needed
    while True:
        rerender_needed = False
        rerender()
        if not rerender_needed:
            break
