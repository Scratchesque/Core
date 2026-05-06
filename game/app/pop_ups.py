import pygame
from pygame import Rect
from pygame_gui.elements import UIPanel, UILabel

from game.core.constants import SCREEN_WIDTH, SCREEN_HEIGHT 
from game.core.events import MENU_ENV_REQUESTED, QUIT_EMV_REQUESTED, CHANGE_ENV_CONFIRMED
from game.support.ui import TypingTextBox, UIFactory

# A panel to explain to the user in the main menu an introduction
class DialoguePanel(UIPanel):
    PANEL_SIZE = (1000, 300)
    PANEL_POS = (
        (SCREEN_WIDTH - PANEL_SIZE[0])//2, 
        (SCREEN_HEIGHT - PANEL_SIZE[1])//2+ 40
    )

    def __init__(self, title, message, manager):
        super().__init__(Rect(self.PANEL_SIZE, self.PANEL_SIZE), manager=manager, object_id="#dialogue_panel", starting_height=5)
        
        self.create_ui(title, message)

    def create_ui(self, title, message):
        padding = 24
        button_size = (160, 54)

        UILabel(
            relative_rect=Rect((padding, 22), (self.PANEL_SIZE[0] - (padding * 2), 36)),
            text=title,
            manager=self.ui_manager,
            container=self,
            object_id="#title",
        )

        TypingTextBox(
            pos=(padding, 78),
            size=((self.PANEL_SIZE[0] - padding * 2), (self.PANEL_SIZE[1] -  padding * 2 - 125)),
            html_text=message,
            manager=self.ui_manager,
            container=self,
            object_id="#body")
        
        self.confirm_button = UIFactory.button_img(
            pos=((self.PANEL_SIZE[0] - button_size[0]) // 2, self.PANEL_SIZE[1] - 78),
            size=button_size,
            image_path="game/assets/SproutLands/cropped/brown_button.png",
            text="Confirm",
            manager=self.ui_manager,
            container=self,
            object_id="#button",
        )

    def process_event(self, event):
        if self.confirm_button.on_click(event):
            self.kill()

# Notifying the player of any changes, eg the environment being reset/changed 
class MessagePanel(UIPanel):
    PANEL_SIZE = (300,160)
    PANEL_POS = (
        (SCREEN_WIDTH-PANEL_SIZE[0])//2, 
        (SCREEN_HEIGHT-PANEL_SIZE[1])//2,
    )

    def __init__(self, title, message, manager):
        super().__init__(
            Rect(self.PANEL_POS, self.PANEL_SIZE),
            manager=manager,
            object_id="#message_panel",
            starting_height=8,
        )
        self.create_ui(title, message)

    def create_ui(self, title, message):
        padding = 24

        UILabel(
            relative_rect=Rect((padding, 22), (self.PANEL_SIZE[0] - (padding * 2), 36)),
            text=title,
            manager=self.ui_manager,
            container=self,
            object_id="#title",
        )

        UILabel(
            relative_rect=Rect((padding, 78), (self.PANEL_SIZE[0] - (padding * 2), 52)),
            text=message,
            manager=self.ui_manager,
            container=self,
            object_id="#body",
        )

class SpeechPanel(UIPanel):
    PANEL_SIZE = (250,80)

    def __init__(self, panel_pos, message_list, manager):
        super().__init__(
            Rect(panel_pos, self.PANEL_SIZE),
            manager=manager,
            object_id="#speech_panel",
            starting_height=2,
        )
        self.message_list = message_list
        self.message_index = 0
        self.create_ui()

    def create_ui(self):
        padding = 10
        button_size = (35,25)
        button_diff = 30

        UIFactory.image(
            pos=(0,0),
            size=self.PANEL_SIZE,
            image_path="game/assets/SproutLands/UI/Dialouge/dialog box big.png",
            manager=self.ui_manager,
            container=self
        )

        self.text_box = TypingTextBox(
            pos=(padding, padding),
            size=(self.PANEL_SIZE[0] - padding * 2 - button_diff, self.PANEL_SIZE[1]- padding * 2),
            html_text=self.message_list[0],
            manager=self.ui_manager,
            container=self,
            object_id="#body")

        self.next_button = UIFactory.button(
            pos=(
                self.PANEL_SIZE[0]-button_size[0]-padding/2,
                self.PANEL_SIZE[1]-button_size[1]-padding
            ),
            size=button_size,
            text="OK",
            manager=self.ui_manager,
            container=self,
            object_id="#button",
        )

    def process_event(self, event):
        if self.next_button.on_click(event):
            self.message_index += 1
            if self.message_index >= len(self.message_list):
                self.message_index = 0
                self.kill()
                return
            self.text_box.set_full_text(self.message_list[self.message_index])

# Asking if the user is sure that they want to confirm to select their action
class ConfirmationPanel(UIPanel):
    PANEL_SIZE = (525, 220)
    PANEL_POS = (
        (SCREEN_WIDTH-PANEL_SIZE[0])//2, 
        (SCREEN_HEIGHT-PANEL_SIZE[1])//2,
    )

    def __init__(self, title, message, confirm_event_type, manager):
        super().__init__(
            Rect(self.PANEL_POS, self.PANEL_SIZE),
            manager=manager,
            object_id="#confirm_panel",
            starting_height=9,
        )
        self.confirm_event_type = confirm_event_type
        self.create_ui(title, message)

    def create_ui(self, title, message):
        padding = 24
        button_gap = 18
        button_size = (160, 54)
        button_y = self.PANEL_SIZE[1] - 78
        total_button_width = (button_size[0] * 2) + button_gap
        buttons_x = (self.PANEL_SIZE[0] - total_button_width) // 2

        UILabel(
            relative_rect=Rect(
                (padding, 22), 
                (self.PANEL_SIZE[0] - (padding * 2), 36)
            ),
            text=title,
            manager=self.ui_manager,
            container=self,
            object_id="#title",
        )

        UILabel(
            relative_rect=Rect(
                (padding, 78), 
                (self.PANEL_SIZE[0] - (padding * 2), 52)
            ),
            text=message,
            manager=self.ui_manager,
            container=self,
            object_id="#body",
        )

        self.cancel_button = UIFactory.button_img(
            pos=(buttons_x, button_y),
            size=button_size,
            image_path="game/assets/SproutLands/cropped/grey_button.png",
            text="Cancel",
            manager=self.ui_manager,
            container=self
        )
        self.confirm_button = UIFactory.button_img(
            pos=(buttons_x + button_size[0] + button_gap, button_y),
            size=button_size,
            image_path="game/assets/SproutLands/cropped/brown_button.png",
            text="Confirm",
            manager=self.ui_manager,
            container=self
        )

    def process_event(self, event):
        if self.cancel_button.on_click(event):
            self.kill()
            return
        if self.confirm_button.on_click(event):
            self.kill()
            confirm_event = pygame.event.Event(CHANGE_ENV_CONFIRMED, {'change_env': self.confirm_event_type})
            pygame.event.post(confirm_event)

# A settings menu for the user to select to go to menu or quit while playing 
class SettingsMenu(UIPanel):
    PANEL_SIZE = (200,250)
    PANEL_POS = (
        (SCREEN_WIDTH-PANEL_SIZE[0])//2, 
        (SCREEN_HEIGHT-PANEL_SIZE[1])//2
    )

    def __init__(self, manager):
        super().__init__(
            Rect(self.PANEL_POS, self.PANEL_SIZE), 
            manager=manager, 
            object_id="#settings_panel", 
            starting_height=10
        )
        
        self.create_ui()

    def create_ui(self):
        padding_x = 20
        padding_y = 10
        size_x  = self.PANEL_SIZE[0] - padding_x * 2
        label_size = (size_x, 75)
        button_size = (size_x, 54)
        button_y = label_size[1] + padding_y * 2
        button_gap = button_size[1] + padding_y 

        UILabel(
            relative_rect=Rect((padding_x, 0), label_size),
            text="Settings",
            manager=self.ui_manager,
            container=self,
            object_id="#title",
        )

        self.menu_button = UIFactory.button_img(
            pos=(padding_x, button_y),
            size=button_size,
            image_path="game/assets/SproutLands/cropped/brown_button.png",
            text="Menu",
            manager=self.ui_manager,
            container=self,
        )
        self.quit_button = UIFactory.button_img(
            pos=(padding_x, button_y + button_gap),
            size=button_size,
            image_path="game/assets/SproutLands/cropped/grey_button.png",
            text="Quit",
            manager=self.ui_manager,
            container=self,
        )

    def process_event(self, event):
        if self.menu_button.on_click(event):
            menu_event = pygame.event.Event(MENU_ENV_REQUESTED)
            pygame.event.post(menu_event)
            self.kill()
            return
        if self.quit_button.on_click(event):
            quit_event = pygame.event.Event(QUIT_EMV_REQUESTED)
            pygame.event.post(quit_event)
            self.kill()
            return
