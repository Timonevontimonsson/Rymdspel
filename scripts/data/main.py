from scripts.data import setup, tools
from scripts.data import constant as c

from scripts.data.states import main_menu, load_screen, level1, home


def main():
    run_it = tools.Control(setup.ORIGINAL_CAPTION)
    state_dict = {c.MAIN_MENU: main_menu.Menu(),
                  c.LOAD_SCREEN: load_screen.LoadScreen(),
                  c.LEVEL1: level1.Level1(),
                  c.HOME: home.Home()}

    run_it.setup_states(state_dict, c.MAIN_MENU)
    run_it.main()