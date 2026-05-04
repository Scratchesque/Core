from pygame import Rect
from pygame_gui.elements import UIPanel

from game.core.events import *
from game.core.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from game.environments.base import BaseEnvironment
from game.support.ui import UIFactory


class CompletionScreen(BaseEnvironment):
    PANEL_SIZE = (1400, 660)
    BUTTON_SIZE = (240, 72)
    BUTTON_GAP = 24

    def __init__(self, level_file="completion"):
        super().__init__(level_file)
        self.replay_button = None
        self.menu_button = None
        self.quit_button = None

    def create_ui(self):
        UIFactory.image(
            pos=(SCREEN_WIDTH // 2, 50),
            size=(620, 220),
            image_path="game/assets/menu/logo.png",
            manager=self.ui_manager,
            object_id="#menu_logo",
            anchor="midtop",
        )
        UIFactory.label(
            pos=(SCREEN_WIDTH // 2, 292),
            size=(700, 40),
            text="Every carrot found. Kevin made it home.",
            manager=self.ui_manager,
            object_id="#menu_subtitle",
            anchor="center",
        )

        panel_pos = (
            (SCREEN_WIDTH - self.PANEL_SIZE[0]) // 2,
            285,
        )
        panel = UIPanel(
            Rect(panel_pos, self.PANEL_SIZE),
            manager=self.ui_manager,
            object_id="#dialogue_panel",
            starting_height=3,
        )

        UIFactory.label(
            pos=(36, 24),
            size=(self.PANEL_SIZE[0] - 72, 42),
            text="Journey Complete",
            manager=self.ui_manager,
            container=panel,
            object_id="#title",
        )

        UIFactory.text_box(
            pos=(36, 80),
            size=(620, 400),
            html_text=self._build_details_html(),
            manager=self.ui_manager,
            container=panel,
            object_id="#body",
        )

        UIFactory.text_box(
            pos=(688, 80),
            size=(676, 400),
            html_text=self._build_credits_html(),
            manager=self.ui_manager,
            container=panel,
            object_id="#body",
        )

        button_y = self.PANEL_SIZE[1] - 102
        total_width = (self.BUTTON_SIZE[0] * 3) + (self.BUTTON_GAP * 2)
        start_x = (self.PANEL_SIZE[0] - total_width) // 2

        self.replay_button = UIFactory.button_img(
            pos=(start_x, button_y),
            size=self.BUTTON_SIZE,
            image_path="game/assets/SproutLands/cropped/brown_button.png",
            text="Replay from Start",
            manager=self.ui_manager,
            container=panel,
            object_id="#button",
        )
        self.menu_button = UIFactory.button_img(
            pos=(start_x + self.BUTTON_SIZE[0] + self.BUTTON_GAP, button_y),
            size=self.BUTTON_SIZE,
            image_path="game/assets/SproutLands/cropped/grey_button.png",
            text="Main Menu",
            manager=self.ui_manager,
            container=panel,
            object_id="#button",
        )
        self.quit_button = UIFactory.button_img(
            pos=(start_x + (self.BUTTON_SIZE[0] + self.BUTTON_GAP) * 2, button_y),
            size=self.BUTTON_SIZE,
            image_path="game/assets/SproutLands/cropped/grey_button.png",
            text="Quit",
            manager=self.ui_manager,
            container=panel,
            object_id="#button",
        )

    def on_ui_event(self, event):
        super().on_ui_event(event)

        change_env_data = {} 
        if self.replay_button and self.replay_button.on_click(event):
            change_env_data = {'change_env': 'Start'}

        if self.menu_button and self.menu_button.on_click(event):
            change_env_data = {'change_env': 'Main Menu'}

        if self.quit_button and self.quit_button.on_click(event):
            change_env_data = {'change_env': 'QUIT'}

        if change_env_data != {}:
            env_event = pygame.event.Event(CHANGE_ENV_CONFIRMED, change_env_data)
            pygame.event.post(env_event)

    def _get_story_envs(self):
        story_envs = []
        for env in self.game_manager.envs_list:
            title = env.title
            if title == "Main Menu" or title == self.title:
                continue
            if title == "Start" or title.startswith("Level "):
                story_envs.append(env)

        def env_sort_key(env):
            if env.title == "Start":
                return (0, 0)
            suffix = env.title.removeprefix("Level ")
            return (1, int(suffix) if suffix.isdigit() else 999)

        return sorted(story_envs, key=env_sort_key)

    def _build_details_html(self):
        story_envs = self._get_story_envs()
        completed_titles = {
            env.title
            for env in story_envs
            if self.game_manager.player_data.is_completed(env.title)
        }
        total_levels = len(story_envs)
        last_level = story_envs[-1].title if story_envs else "the final level"

        lines = [
            "<b>Run summary</b>",
            f"Completed <b>{len(completed_titles)} / {total_levels}</b> campaign levels.",
            f"Final clear: <b>{last_level}</b>.",
            "Movement, jumping, loops, and energy management all made it into the run.",
            "",
            "<b>What now?</b>",
            "Replay from Start to run the full route again, or jump back to the menu and revisit any unlocked level.",
        ]
        return "<br>".join(lines)

    def _build_credits_html(self):
        lines = [
            "<b>Credits</b>",
            "Created by <b>Will</b>, <b>Albert</b>, <b>Harry</b>, <b>Kamran</b>, <b>Tafara</b>, and <b>Vlad</b>.",
            "",
            "<b>References</b>",
            "pygame. GitHub (2020). Available at: github.com/pygame/pygame.",
            "Sprout Lands Asset Pack. itch.io by Cup Nooble.",
            "Sprout Lands UI Pack. itch.io (2023).",
            "pygame_gui documentation at pygame-gui.readthedocs.io.",
            "Tiled map editor at mapeditor.org.",
            "",
            "Thanks for playing through the whole set.",
        ]
        return "<br>".join(lines)
