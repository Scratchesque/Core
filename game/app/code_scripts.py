import re
from dataclasses import replace
import pygame
from pygame import K_ESCAPE, K_RETURN, KEYUP, Rect, Vector2
from pygame_gui._constants import UI_BUTTON_PRESSED
from pygame_gui.elements import UIButton, UILabel, UIPanel, UITextBox, UITextEntryLine

from game.app.block_interpreter import Interpreter
from game.app.block_registry import get_block_library
from game.core.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from game.core.events import RESET_ENV_REQUESTED
from game.support.ui import Button, UIFactory


class ProblemPanel(UIPanel):
    PANEL_SIZE = (625, 300)
    PANEL_POS = (
        (SCREEN_WIDTH - PANEL_SIZE[0]) // 2,
        (SCREEN_HEIGHT - PANEL_SIZE[1]) // 2,
    )

    def __init__(self, spec_str_list, manager):
        super().__init__(
            relative_rect=Rect(self.PANEL_POS, self.PANEL_SIZE),
            starting_height=8,
            manager=manager,
            object_id="#problem_panel",
        )

        self.method_string = f"<b>{spec_str_list[0]}</b>"
        self.fix_string = self.replace_string_html(spec_str_list[1])

        self.value = 0

        self.create_ui()

    @staticmethod
    def replace_string_html(string):
        temp_str = string.replace("  ", "")
        return re.sub(r"<[^>]+>", "", temp_str)

    def create_ui(self):
        padding = 24
        button_gap = 18
        button_size = (160, 54)
        button_y = self.PANEL_SIZE[1] - 78
        total_button_width = (button_size[0] * 2) + button_gap
        buttons_x = (self.PANEL_SIZE[0] - total_button_width) // 2

        UILabel(
            relative_rect=Rect((padding, 25), (self.PANEL_SIZE[0] - (padding * 2), 36)),
            text="Fix the Code!",
            manager=self.ui_manager,
            container=self,
            object_id="#title",
        )

        self.help_text = UITextBox(
            relative_rect=Rect((padding, 65), (self.PANEL_SIZE[0] - (padding * 2), 52)),
            html_text="Can you find the bug that breaks the player?",
            manager=self.ui_manager,
            container=self,
            object_id="#body",
        )

        UITextBox(
            relative_rect=Rect(
                (padding, 105), (self.PANEL_SIZE[0] - (padding * 2), 52)
            ),
            html_text=self.method_string,
            manager=self.ui_manager,
            container=self,
            object_id="#body",
        )

        self.entry_box = UITextEntryLine(
            relative_rect=Rect(
                (padding, 155), (self.PANEL_SIZE[0] - (padding * 2), 52)
            ),
            manager=self.ui_manager,
            container=self,
            object_id="#entry_box",
        )
        self.entry_box.set_text(self.fix_string)

        self.cancel_button = UIFactory.button_img(
            pos=(buttons_x, button_y),
            size=button_size,
            image_path="game/assets/SproutLands/cropped/grey_button.png",
            text="Cancel",
            manager=self.ui_manager,
            container=self,
        )
        self.confirm_button = UIFactory.button_img(
            pos=(buttons_x + button_size[0] + button_gap, button_y),
            size=button_size,
            image_path="game/assets/SproutLands/cropped/brown_button.png",
            text="Confirm",
            manager=self.ui_manager,
            container=self,
        )
        pass

    def get_values(self, string):
        string_list = string.split(" ")
        r_value = string_list.pop()
        l_value = " ".join(string_list)
        return l_value, r_value

    def check_code_complete(self):
        l_og_value, r_og_value = self.get_values(self.fix_string)
        l_box_value, r_box_value = self.get_values(self.entry_box.get_text())
        if l_og_value != l_box_value:
            self.help_text.set_text(
                Interpreter._type_to_font(
                    "You cannot change the Player Assignment!", "loop"
                )
            )
            return

        if r_og_value == r_box_value:
            self.help_text.set_text(
                Interpreter._type_to_font(
                    "You haven't tried changing the ammount!", "loop"
                )
            )
            return

        try:
            value = int(r_box_value)
        except ValueError:
            self.help_text.set_text(
                Interpreter._type_to_font("The player can't move with text!", "loop")
            )
            return

        if True:
            self.value = value
            self.kill()

    def process_event(self, event):
        if (
            event.type == KEYUP and event.key == K_ESCAPE
        ) or self.cancel_button.on_click(event):
            self.kill()
            return
        if (
            event.type == KEYUP and event.key == K_RETURN
        ) or self.confirm_button.on_click(event):
            self.check_code_complete()
            return


class ProblemButton(Button):
    def __init__(self, spec, spec_str_list, pos, line, manager, container=None):
        self.spec = spec
        self.spec_str_list = spec_str_list
        self.size = Vector2(30, 30)
        self.pos = Vector2(self.get_line_pos(pos, line))
        self.line = line
        self.container = container

        self.img = UIFactory.image(
            pos=self.pos,
            size=self.size,
            image_path="game/assets/SproutLands/cropped/brown_block.png",
            manager=manager,
            container=container,
        )

        super().__init__(
            self.pos,
            self.size,
            "!",
            manager,
            object_id="#transparent",
            container=container,
        )

        self.problem_panel = None
        self.solved = False

    def get_line_pos(self, block_pos, line):
        font_size = 21
        line_y = block_pos[1] + 5 + (line - 1) * font_size
        return (block_pos[0] - self.size.x - 10, line_y)

    def process_event(self, event):
        super().process_event(event)
        if self.on_click(event) and (
            self.problem_panel is None or not self.problem_panel.alive()
        ):
            self.problem_panel = ProblemPanel(
                spec_str_list=self.spec_str_list, manager=self.ui_manager
            )

        if self.problem_panel == None:
            return

        if not self.problem_panel.alive() and self.problem_panel.value != 0:
            if self.spec.x != 0:
                spec = replace(self.spec, x=self.problem_panel.value)
            elif self.spec.y != 0:
                spec = replace(self.spec, y=self.problem_panel.value)

            self.solved = True
            self.container.change_block(spec)
            self.img.kill()
            self.kill()


class CodePanel(UIPanel, Interpreter):
    BTN_SIZE = (30, 30)

    PANEL_PADDING = 18
    SCRIPT_LANE_PADDING = 30
    SECTION_GAP = 16
    STATUS_HEIGHT = 75
    ACTION_BUTTON_HEIGHT = 54
    RESET_BUTTON_HEIGHT = 50

    def __init__(
        self, player, panel_pos, panel_size, level_script, manager, level_title
    ):
        self.player = player
        self._change_min_lines(34)
        self.size = Vector2(panel_size)
        self.pos = Vector2(panel_pos)
        self.level_title = level_title
        super().__init__(
            relative_rect=Rect(panel_pos, panel_size),
            starting_height=3,
            manager=manager,
            object_id="#code_panel",
        )

        self.is_running = False
        self.program_blocks = []
        self._exec_steps = []
        self.problem_buttons = []

        self.configure_layout()

        self._make_start_script(level_script)
        self._make_classes(make_problem=True)
        self._make_blocks()

        self.create_ui()
        self.refresh_status()

    def configure_layout(self):
        inner_width = self.size[0] - (self.PANEL_PADDING * 2)
        controls_height = (
            self.STATUS_HEIGHT
            + self.SECTION_GAP
            + self.ACTION_BUTTON_HEIGHT
            + self.SECTION_GAP
            + self.RESET_BUTTON_HEIGHT
        )
        content_top = self.PANEL_PADDING
        content_height = self.size[1] - controls_height - (self.PANEL_PADDING * 3)

        self.script_area_rect = Rect(
            (self.PANEL_PADDING + self.SCRIPT_LANE_PADDING, content_top),
            (inner_width - self.SCRIPT_LANE_PADDING, content_height),
        )
        self.status_rect = Rect(
            (self.PANEL_PADDING, self.script_area_rect.bottom + self.SECTION_GAP),
            (inner_width, self.STATUS_HEIGHT),
        )

        buttons_y = self.status_rect.bottom + self.SECTION_GAP
        self.run_button_rect = Rect(
            (self.PANEL_PADDING, buttons_y),
            (inner_width, self.RESET_BUTTON_HEIGHT),
        )
        self.reset_button_rect = Rect(
            (
                self.PANEL_PADDING,
                buttons_y + self.ACTION_BUTTON_HEIGHT + self.SECTION_GAP,
            ),
            (inner_width, self.RESET_BUTTON_HEIGHT),
        )

        self.text_rect = Rect(
            (self.script_area_rect.x + 5, self.script_area_rect.y + 5),
            (self.script_area_rect.size[0], self.script_area_rect.size[1] + 50),
        )

    def create_ui(self):

        self.script_lane = UIPanel(
            relative_rect=self.script_area_rect,
            manager=self.ui_manager,
            container=self,
            object_id="#script_lane",
            starting_height=1,
        )
        self.status_display = UITextBox(
            html_text="",
            relative_rect=self.status_rect,
            manager=self.ui_manager,
            container=self,
            object_id="#script_status",
        )
        self.run_button = UIButton(
            relative_rect=self.run_button_rect,
            text="Run",
            manager=self.ui_manager,
            container=self,
            object_id="#run_button",
        )

        self.reset_button = UIButton(
            relative_rect=self.reset_button_rect,
            text="Reset Level",
            manager=self.ui_manager,
            container=self,
            object_id="#edit_button",
        )

        block_text = self._translate_blocks()
        self.text_box = UITextBox(
            relative_rect=self.text_rect,
            html_text=block_text,
            manager=self.ui_manager,
            container=self,
            object_id="#text_code",
        )

    def process_event(self, event):
        if self.is_running:
            return

        if event.type != UI_BUTTON_PRESSED:
            return

        if event.ui_element == self.run_button:
            self._exec_steps = self._build_exec_steps()
            if not self._exec_steps:
                return
            self.is_running = True
            self.next_step_index = 0
            return

        if event.ui_element == self.reset_button:
            reset_event = pygame.event.Event(RESET_ENV_REQUESTED)
            pygame.event.post(reset_event)
            return

    def update(self, delta_time):
        self.run_next_step()

    def _build_exec_steps(self):
        steps = []
        for script_list in self.program_blocks:
            spec_list = script_list[0]
            repeat_amm = script_list[1]
            for _ in range(repeat_amm):
                for spec in spec_list:
                    steps.append(spec)
        return steps

    def refresh_status(self):
        problems_left = self._count_problems_left()
        if self.is_running:
            status = (
                "<b>Status:</b> Running your script.<br>"
                f"Step {self.next_step_index} of {len(self._exec_steps)}."
            )
        elif problems_left == 0:
            status = (
                "<b>Status:</b> Script ready.<br>"
                "Run the program to see if you have successfully fixed the code"
            )
        else:
            status = (
                "<b>Status:</b> Fix this program.<br>"
                f"There is {problems_left} problem(s) left for you to solve. Press '!' to attempt."
            )
        self.status_display.set_text(status)

    def change_block(self, block):
        for x in range(len(self.program_blocks)):
            spec_list = self.program_blocks[x][0]
            for y in range(len(spec_list)):
                if spec_list[y].id == block.id:
                    self.program_blocks[x][0][y] = block
                    continue

        self._make_classes()
        block_text = self._translate_blocks()
        self.text_box.set_text(block_text)
        self.refresh_status()

    def run_next_step(self):
        if not self.is_running or self.player.is_moving:
            return

        if self.next_step_index >= len(self._exec_steps):
            self.is_running = False
            self.next_step_index = 0
            self.player.pos = self.player.start_pos.copy()
            self.player.deplete_energy()
            self.refresh_status()
            return

        spec = self._exec_steps[self.next_step_index]
        self.player.do_action(spec.action, x=spec.x, y=spec.y)
        self.next_step_index += 1
        self.refresh_status()

    def _count_problems_left(self):
        total_problems = 0
        problems_solved = 0
        for button in self.problem_buttons:
            total_problems += 1
            if button.solved:
                problems_solved += 1
        return total_problems - problems_solved

    def _make_start_script(self, level_script):
        for script_line in level_script:
            blocks = get_block_library(script_line[0])
            self.program_blocks.append([blocks, script_line[1]])

    def _make_classes(self, make_problem=False):
        font_text = self._type_to_font("Blocks", "main")
        self.class_list = [f"Class {font_text}:"]
        all_specs = []

        for script_list in self.program_blocks:
            for spec in script_list[0]:
                if spec in all_specs:
                    continue
                all_specs.append(spec)

        all_specs.sort(key=lambda p: p.label, reverse=True)

        for spec in all_specs:
            format_spec_list = self._format_spec_class(spec)
            if "fix" in spec.id and make_problem:
                line_type = 2 if spec.action == "jump" else 1
                line_pos = len(self.class_list) + 1 + line_type

                spec_str_list = [format_spec_list[0], format_spec_list[line_type]]

                self.problem_buttons.append(
                    ProblemButton(
                        spec=spec,
                        spec_str_list=spec_str_list,
                        pos=self.script_area_rect.topleft,
                        line=line_pos,
                        manager=self.ui_manager,
                        container=self,
                    )
                )
            self.class_list += format_spec_list

    def _make_blocks(self):
        font_text = self._type_to_font(self.level_title, "main")
        self.block_list = [f"Script {font_text}:"]

        for script_list in self.program_blocks:
            spec_list = script_list[0]
            repeat_amm = script_list[1]
            if repeat_amm != 1:
                loop_font = self._type_to_font("Loop", "loop")
                self.block_list.append(f"{self.GAP}{loop_font} ({repeat_amm}):")

                for spec in spec_list:
                    self.block_list.append(self._format_spec_code(spec, func_gap=True))
            else:
                for spec in spec_list:
                    self.block_list.append(self._format_spec_code(spec))
                pass
