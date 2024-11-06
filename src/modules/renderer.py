# this file implements a similar rendering-system and state-system that is used by React.js (https://react.dev/)
# every time the application state changes, the view gets completely wiped, and a new view is calculated (by invoking ui functions), the ui is effectively a function of state

import os

# we need this flag because if we invoke rerender() directly after a state change python does not finish executing the function (because of recursion), meaning; we can only update one state at a time
rerender_needed = False

# declares the variables for storing state, effects, and the cursors
all_state, all_effects = [], []
effects_cursor, state_cursor = 0, 0


def clear_terminal():
    """clears the terminal, may or may not be cross-plattform compatible"""
    os.system("cls" if os.name == "nt" else "printf '\033c'")


def use_effect(func, dependencies=[]):
    """
    similar to useEffect in React (https://react.dev/reference/react/useEffect)
    it takes two parameters, func, and a dependency list
    if the ui rerenders, and the dependencies differ from the last rerender then the "func" is called

    important note:
        all hooks (functions who's names start with use_) should only be called at the top level of functions,
        meaning not called conditionally, otherwise the cursor logic will be screwed up, similar to "rules of hooks" (https://react.dev/reference/rules#rules-of-hooks)
    """

    global effects_cursor
    global all_effects

    if not len(all_effects) - 1 >= effects_cursor:  # if initializing use_effect
        all_effects.append([func, dependencies])
        func()
    else:  # if use_effect is called for the many-th time
        changed = False
        for i, d in enumerate(dependencies):
            if not d == all_effects[effects_cursor][1]:
                changed = True
                all_effects[effects_cursor][1] = d  # update the dependencies
        if changed:
            # input("deps changed")
            func()

    effects_cursor += 1


def use_state(initial_state="") -> tuple:
    """
    similar to useState in React (https://react.dev/reference/react/useState),
    function for creating state
    returns two functions, one for getting the state, one for setting the state

    important note:
        all hooks (functions who's names start with use_) should only be called at the top level of functions,
        meaning not called conditionally, otherwise the cursor logic will be screwed up, similar to "rules of hooks" (https://react.dev/reference/rules#rules-of-hooks)
    """

    global state_cursor
    global all_state
    # we freeze the cursor because we want the current value for state_cursor to be stored within the create_state closure
    frozen_cursor = state_cursor

    # if a state element does not already exists for the state_cursor
    if not len(all_state) - 1 >= state_cursor:
        all_state.append(initial_state)

    def get_state() -> dict:
        """remember to always call the function to get the value, and always treat it as if it was immutable"""
        global all_state
        return all_state[frozen_cursor]

    def update_state(new_state: dict) -> None:
        """remember to always call the function with the new value"""
        global all_state
        global rerender_needed
        rerender_needed = True
        all_state[frozen_cursor] = new_state

    state_cursor += 1

    return get_state, update_state


def rerender(ui_entry_func):
    """reset the cursors and clear terminal, then call the entry function to render UI"""
    global state_cursor, effects_cursor
    state_cursor, effects_cursor = 0, 0
    clear_terminal()
    ui_entry_func()  # processblockning
    # clear any unused state (probably riddled with buggs because the clearing happens after the rerender, so the wrong state could still be returned)
    if not state_cursor == len(all_state) - 1:
        del all_state[state_cursor:]


def render(ui_entry_func):
    """
    initial render function to start the UI rendering cycle
    takes an "ui_entry_func", that will be the entrypoint of the ui
    kind of like createRoot (or ReactDOM.render() in older versions) in react (https://react.dev/reference/react-dom/client/createRoot)
    """
    global rerender_needed
    another_rerender_needed = True
    while another_rerender_needed:
        rerender_needed = False
        rerender(ui_entry_func)
        if not rerender_needed:
            another_rerender_needed = False
