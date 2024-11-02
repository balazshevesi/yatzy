from modules import renderer as r
from ui_app import ui_app
import sys
import os


# to fix import paths, maybe not needed actually?
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def main():
    try:
        r.render(ui_app)
    except SystemExit:
        print("exited the program")
    except:
        print("something went wrong")


main()
