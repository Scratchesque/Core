from game.core.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from game.support.ui import UIFactory
from game.environments.base import BaseEnvironment
from game.app.panels import DialoguePanel


class LevelSelect(BaseEnvironment):
    LOGO_SIZE = (760, 270)
    SUBTITLE_SIZE = (520, 32)
    BUTTON_SIZE = (360, 84)
    INTRO_SIZE = (1000, 300)
    BUTTON_GAP = 20

    def __init__(self, level_file="menu"):
        super().__init__(level_file)
        self.level_buttons = []
        self.quit_button = None

    def create_ui(self):
        self.level_buttons = []

        UIFactory.image(
            pos=(SCREEN_WIDTH // 2, 150),
            size=self.LOGO_SIZE,
            image_path="game/assets/menu/logo.png",
            manager=self.ui_manager,
            object_id="#menu_logo",
            anchor="midtop",
        )
        UIFactory.label(
            pos=(SCREEN_WIDTH // 2, 400),
            size=self.SUBTITLE_SIZE,
            text="Pick a level and start hopping.",
            manager=self.ui_manager,
            object_id="#menu_subtitle",
            anchor="center",
        )

        playable_envs = self._get_playable_envs()
        total_height = (len(playable_envs) * self.BUTTON_SIZE[1]) + (
            max(0, len(playable_envs) - 1) * self.BUTTON_GAP
        )
        start_y = max(420, (SCREEN_HEIGHT - total_height) // 2 + 100)

        total_unlocked = 0
        for index, env in enumerate(playable_envs):
            button_y = start_y + (index * (self.BUTTON_SIZE[1] + self.BUTTON_GAP))
            is_unlocked = self.game_manager.player_data.is_unlocked(env.title) or getattr(self.game_manager, "debug", False)
            total_unlocked+=1 if is_unlocked else 0
            button_text = env.title if is_unlocked else f"Locked: {env.title}"
            button_path = "game/assets/SproutLands/cropped/"
            button = UIFactory.button_img(
                pos=(SCREEN_WIDTH // 2, button_y),
                size=self.BUTTON_SIZE,
                image_path=f"{button_path}brown_button.png" if is_unlocked else f"{button_path}grey_button.png",
                text=button_text,
                manager=self.ui_manager,
                object_id="#menu_image_button",
                anchor="midtop",
            )
            self.level_buttons.append((button, env.title, is_unlocked))

        
        if total_unlocked == 1:
            # only start level unlocked
            DialoguePanel(
                panel_pos=((SCREEN_WIDTH - self.INTRO_SIZE[0])//2, (SCREEN_HEIGHT - self.INTRO_SIZE[1])//2+ 100),
                panel_size=self.INTRO_SIZE,
                title="Welcome to Rabbit Rush your introduction to computer science!",
                message='''Kevin the Bunny has lost his Carrots and abilities. It's your goal to gain them back. 
Learn how to read and implement code to help Kevin reach his goal!''',
                manager=self.ui_manager)

        self.quit_button = UIFactory.button_img(
            pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80),
            size=(260, 72),
            image_path="game/assets/SproutLands/cropped/grey_button.png",
            text="Quit",
            manager=self.ui_manager,
            object_id="#menu_image_button",
            anchor="midbottom",
        )

    def on_ui_event(self, event):
        super().on_ui_event(event)

        for button, env_title, is_unlocked in self.level_buttons:
            if is_unlocked and button.on_click(event):
                self.game_manager.change_env(env_title)
                return

        if self.quit_button and self.quit_button.on_click(event):
            self.game_manager.change_env("QUIT")

    def _get_playable_envs(self):
        playable_envs = [
            env for env in self.game_manager.envs_list if env.title != self.title
        ]

        def env_sort_key(env):
            if env.title == "Start":
                return (0, 0)
            if env.title.startswith("Level "):
                suffix = env.title.removeprefix("Level ")
                if suffix.isdigit():
                    return (1, int(suffix))
            return (2, env.title)

        return sorted(playable_envs, key=env_sort_key)
