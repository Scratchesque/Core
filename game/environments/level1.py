from game.core.constants import *
from game.environments.base import BaseEnvironment
from game.window.ui import TypingTextBox, UIFactory


class Level1(BaseEnvironment):
    def __init__(self, title):
        background_hex = "ffffff"
        theme = "level1"
        super().__init__(title, background_hex, theme)

    def create_ui(self, ui_manager):
        self.title_label = UIFactory.label(
            (20, 20), (660, 30), "Title", ui_manager, object_id="title"
        )
        self.dialogue_box = TypingTextBox(
            (20, 60),
            (660, 160),
            "<b>Guide</b>: Welcome. <a>https://google.com</a> This is a small dialogue box example.",
            ui_manager,
            object_id="#test_font",
            typing_speed=30,
        )
        self.quit_button = UIFactory.button(
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40),
            (100, 50),
            "Quit",
            ui_manager,
            object_id="quit",
            anchor="midbottom",
        )

    def on_ui_event(self, event):
        quit_result = self.quit_button.on_click(event)
        url_clicked = self.dialogue_box.url_click(event)
        if url_clicked:
            print("Pressed url box!")
        if quit_result:
            print("Quit Game!")
            return False
            # pygame.quit() # try not to exit from inside the environment but if you have to there is an exception so it doesnt crash

    def update_frame(self, delta_time):
        self.dialogue_box.update_typing(delta_time)
