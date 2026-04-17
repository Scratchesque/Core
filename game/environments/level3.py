from game.environments.base import GameEnv
from game.core.ui import UIFactory

# making each file seperate again cause i realise sometimes there will be different elements being rendered depending on the level, 
# so like this should be easier to make changes on individual levels
class Level3(GameEnv):
    def __init__(self):
        super().__init__(level_file="level2")

    def create_ui(self):
        super().create_ui()
        # This is temporarily in the test_panel container untill it finds a proper place on the screen or we replace it
        # As if its not in a container, it can get lost between the layers
        self.menu_button = UIFactory.button(
            pos=(500, 500),
            size=(100, 50), 
            text="Menu", 
            manager=self.ui_manager, 
            container=self.blocks.panel_container)
        

    def on_ui_event(self, event):
        super().on_ui_event(event)
        if self.menu_button.on_click(event):
            self.game_manager.change_env("Main Menu")

    def update_frame(self, delta_time):
        pass
