from modules import renderer as r
from ui_app import ui_app


def main():
    try:
        r.render(ui_app)
    except SystemExit:
        print("exited the program")
    except:
        print(
            "something went wrong please contact the code author if you wish to get it fixed"
        )


main()
