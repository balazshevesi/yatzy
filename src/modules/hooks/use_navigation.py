from .. import renderer as r


def use_navigation(initial_path=""):
    nav, set_nav = r.use_state(initial_path)

    def go_back():
        back_state_value = nav().split("/")
        back_state_value.pop()
        set_nav("/".join(back_state_value))

    def go_forward(path: str):
        forward_state_value = nav() + "/" + path
        set_nav(forward_state_value)

    def reload():
        set_nav(nav())

    return {
        "get_path": nav,
        "set_path": set_nav,
        "go_back": go_back,
        "go_forward": go_forward,
        "reload": reload,
    }
