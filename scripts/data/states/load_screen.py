
from scripts.data import setup, tools
from scripts.data import constant as c
from scripts import info

class LoadScreen(tools._State):
    def __init__(self):
        tools._State.__init__(self)

    def startup(self, current_time, persist):
        self.persist = persist
        self.game_info = self.persist
        self.next = self.set_next_state()
        self.start_time = self.current_time

        

        info_state = self.set_overhead_info_state()

        self.overhead_info = info.OverheadInfo(self.game_info, info_state)

    def set_next_state(self):
        return c.LEVEL1

    def set_overhead_info_state(self):
        return c.LOAD_SCREEN


    def update(self, surface, keys, current_time):
        if (current_time - self.start_time) < 2400:
            surface.fill(c.BLACK)
            self.overhead_info.update(self.game_info)
            self.overhead_info.draw(surface)

        elif (current_time - self.start_time) < 2600:
            surface.fill(c.BLACK)

        elif (current_time - self.start_time) < 2635:
            surface.fill((106, 150, 252))

        else:
            self.done = True