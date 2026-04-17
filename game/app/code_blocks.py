import pygame
from pygame import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, Rect
from pygame.math import Vector2
from pygame_gui.elements import UIButton, UILabel, UIPanel, UITextBox
from pygame_gui._constants import UI_BUTTON_PRESSED, UI_BUTTON_START_PRESS

from game.app.block_registry import get_block_library
from game.core.constants import RESET_ENV_CONFIRMED


class ScriptBlock:
    REMOVE_BUTTON_SIZE = 24
    REMOVE_BUTTON_OFFSET = 6

    def __init__(self, spec, button, remove_button, position):
        self.spec = spec
        self.button = button
        self.remove_button = remove_button
        self.position = Vector2(position)
        self.target_position = Vector2(position)

    def sync_controls(self):
        x = int(self.position.x)
        y = int(self.position.y)
        self.button.set_relative_position((x, y))
        self.remove_button.set_relative_position(
            (
                x + self.button.get_relative_rect().width - self.REMOVE_BUTTON_SIZE - self.REMOVE_BUTTON_OFFSET,
                y + self.REMOVE_BUTTON_OFFSET,
            )
        )

    def set_target(self, pos):
        self.target_position = Vector2(pos)

    def set_position(self, pos):
        self.position = Vector2(pos)
        self.target_position = Vector2(pos)
        self.sync_controls()

    def update(self):
        if self.position.distance_squared_to(self.target_position) < 1:
            self.position = self.target_position.copy()
        else:
            self.position += (self.target_position - self.position) * 0.35
        self.sync_controls()

    def kill(self):
        self.button.kill()
        self.remove_button.kill()


class CodeBlocks(UIPanel):
    PROGRAM_LIMIT = 8
    SCRIPT_BLOCK_LAYER = 6
    PANEL_PADDING = 18
    SECTION_GAP = 16
    PALETTE_BUTTON_HEIGHT = 50
    PALETTE_BUTTON_GAP = 12
    LANE_PADDING_X = 18
    LANE_HEADER_HEIGHT = 76
    LANE_BOTTOM_PADDING = 18
    STATUS_HEIGHT = 82
    ACTION_BUTTON_HEIGHT = 54
    ACTION_BUTTON_GAP = 12
    RESET_BUTTON_HEIGHT = 50
    PALETTE_MIN_WIDTH = 176
    PALETTE_MAX_WIDTH = 208
    PALETTE_FALLBACK_MIN_WIDTH = 116
    LANE_MIN_WIDTH = 220

    def __init__(self, panel_pos, panel_size, manager, player, allowed_blocks=None):
        super().__init__(
            Rect(panel_pos, panel_size),
            manager=manager,
            object_id="#code_panel",
            starting_height=2,
        )

        self.player = player
        self.block_library = get_block_library(allowed_blocks)
        self.program_blocks = []
        self.next_step_index = 0
        self.is_running = False
        self.dragged_block = None
        self.drag_offset = Vector2()
        self.drag_original_index = None
        self.drag_was_new = False
        self.panel_size = panel_size
        self.script_area_rect = Rect((0, 0), (0, 0))
        self.slot_size = (0, self.PALETTE_BUTTON_HEIGHT)
        self.slot_spacing = self.slot_size[1] + self.PALETTE_BUTTON_GAP
        self.palette_button_to_spec = {}
        self.script_button_to_block = {}
        self.remove_button_to_block = {}
        self.palette_drag_source = None
        self.block_specs = {spec.id: spec for spec in self.block_library}
        self.configure_layout()

        self.create_ui()
        self.refresh_status()

    def configure_layout(self):
        panel_width, panel_height = self.panel_size
        inner_width = panel_width - (self.PANEL_PADDING * 2)
        controls_height = (
            self.STATUS_HEIGHT
            + self.SECTION_GAP
            + self.ACTION_BUTTON_HEIGHT
            + self.SECTION_GAP
            + self.RESET_BUTTON_HEIGHT
        )
        content_top = self.PANEL_PADDING
        content_height = panel_height - controls_height - (self.PANEL_PADDING * 3)

        preferred_palette_width = min(self.PALETTE_MAX_WIDTH, int(inner_width * 0.34))
        max_palette_width = max(
            self.PALETTE_FALLBACK_MIN_WIDTH,
            inner_width - self.SECTION_GAP - self.LANE_MIN_WIDTH,
        )
        self.palette_width = max(
            self.PALETTE_FALLBACK_MIN_WIDTH,
            min(preferred_palette_width, max_palette_width),
        )
        if inner_width >= self.PALETTE_MIN_WIDTH + self.SECTION_GAP + self.LANE_MIN_WIDTH:
            self.palette_width = max(self.palette_width, self.PALETTE_MIN_WIDTH)

        lane_width = max(
            self.LANE_MIN_WIDTH if inner_width >= self.PALETTE_FALLBACK_MIN_WIDTH + self.SECTION_GAP + self.LANE_MIN_WIDTH else 0,
            inner_width - self.palette_width - self.SECTION_GAP,
        )

        self.palette_title_rect = Rect((self.PANEL_PADDING, content_top), (self.palette_width, 30))
        self.palette_y = self.palette_title_rect.bottom + 12
        self.palette_button_width = self.palette_width
        self.script_area_rect = Rect(
            (self.PANEL_PADDING + self.palette_width + self.SECTION_GAP, content_top),
            (lane_width, content_height),
        )
        self.slot_size = (
            self.script_area_rect.width - (self.LANE_PADDING_X * 2),
            self.PALETTE_BUTTON_HEIGHT,
        )
        self.slot_spacing = self.slot_size[1] + self.PALETTE_BUTTON_GAP
        self.status_rect = Rect(
            (self.PANEL_PADDING, self.script_area_rect.bottom + self.SECTION_GAP),
            (inner_width, self.STATUS_HEIGHT),
        )

        button_width = (inner_width - (self.ACTION_BUTTON_GAP * 2)) // 3
        buttons_y = self.status_rect.bottom + self.SECTION_GAP
        self.run_button_rect = Rect(
            (self.PANEL_PADDING, buttons_y),
            (button_width, self.ACTION_BUTTON_HEIGHT),
        )
        self.undo_button_rect = Rect(
            (self.run_button_rect.right + self.ACTION_BUTTON_GAP, buttons_y),
            (button_width, self.ACTION_BUTTON_HEIGHT),
        )
        clear_button_width = inner_width - (button_width * 2) - (self.ACTION_BUTTON_GAP * 2)
        self.clear_button_rect = Rect(
            (self.undo_button_rect.right + self.ACTION_BUTTON_GAP, buttons_y),
            (clear_button_width, self.ACTION_BUTTON_HEIGHT),
        )
        self.reset_button_rect = Rect(
            (self.PANEL_PADDING, buttons_y + self.ACTION_BUTTON_HEIGHT + self.SECTION_GAP),
            (inner_width, self.RESET_BUTTON_HEIGHT),
        )

    def create_ui(self):
        self.palette_buttons = {}

        UILabel(
            relative_rect=self.palette_title_rect,
            text="Motion Blocks",
            manager=self.ui_manager,
            container=self,
            object_id="#lane_title",
        )

        for index, spec in enumerate(self.block_library):
            button_y = self.palette_y + (
                index * (self.PALETTE_BUTTON_HEIGHT + self.PALETTE_BUTTON_GAP)
            )
            button = UIButton(
                relative_rect=Rect(
                    (self.PANEL_PADDING, button_y),
                    (self.palette_button_width, self.PALETTE_BUTTON_HEIGHT),
                ),
                text=spec.label,
                manager=self.ui_manager,
                container=self,
                object_id="#motion_block",
                starting_height=4,
            )
            self.palette_buttons[spec.id] = button
            self.palette_button_to_spec[button] = spec

        self.script_lane = UIPanel(
            relative_rect=self.script_area_rect,
            manager=self.ui_manager,
            container=self,
            object_id="#script_lane",
            starting_height=1,
        )

        UILabel(
            relative_rect=Rect((self.LANE_PADDING_X, 12), (240, 30)),
            text="Script Lane",
            manager=self.ui_manager,
            container=self.script_lane,
            object_id="#lane_title",
        )

        UILabel(
            relative_rect=Rect((self.LANE_PADDING_X, 42), (320, 24)),
            text="Drag here. Use the x button on a block to remove it.",
            manager=self.ui_manager,
            container=self.script_lane,
            object_id="#lane_hint",
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
        self.undo_button = UIButton(
            relative_rect=self.undo_button_rect,
            text="Undo",
            manager=self.ui_manager,
            container=self,
            object_id="#edit_button",
        )
        self.clear_button = UIButton(
            relative_rect=self.clear_button_rect,
            text="Clear",
            manager=self.ui_manager,
            container=self,
            object_id="#edit_button",
        )
        self.reset_button = UIButton(
            relative_rect=self.reset_button_rect,
            text="Reset Level",
            manager=self.ui_manager,
            container=self,
            object_id="#edit_button",
        )

    def refresh_status(self):
        if self.is_running:
            current_step = min(self.next_step_index + 1, len(self.program_blocks))
            status = (
                "<b>Status:</b> Running your script.<br>"
                f"Step {current_step} of {len(self.program_blocks)}."
            )
        elif self.program_blocks:
            status = (
                "<b>Status:</b> Script ready.<br>"
                f"{len(self.program_blocks)} block(s) snapped into the lane."
            )
        else:
            status = (
                "<b>Status:</b> Build a short program.<br>"
                "Drag blocks into the lane. Use the x button to remove one."
            )

        self.status_display.set_text(status)

    def create_script_block(self, spec, pos):
        button = UIButton(
            relative_rect=Rect(pos, self.slot_size),
            text=spec.label,
            manager=self.ui_manager,
            container=self,
            object_id="#motion_block",
            starting_height=self.SCRIPT_BLOCK_LAYER,
        )
        remove_button = UIButton(
            relative_rect=Rect(
                (
                    pos[0] + self.slot_size[0] - ScriptBlock.REMOVE_BUTTON_SIZE - ScriptBlock.REMOVE_BUTTON_OFFSET,
                    pos[1] + ScriptBlock.REMOVE_BUTTON_OFFSET,
                ),
                (ScriptBlock.REMOVE_BUTTON_SIZE, ScriptBlock.REMOVE_BUTTON_SIZE),
            ),
            text="x",
            manager=self.ui_manager,
            container=self,
            object_id="#remove_block_button",
            starting_height=self.SCRIPT_BLOCK_LAYER + 1,
        )
        block = ScriptBlock(spec, button, remove_button, pos)
        self.script_button_to_block[button] = block
        self.remove_button_to_block[remove_button] = block
        return block

    def destroy_script_block(self, block):
        self.script_button_to_block.pop(block.button, None)
        self.remove_button_to_block.pop(block.remove_button, None)
        block.kill()

    def panel_local_pos(self, mouse_pos):
        panel_rect = self.get_abs_rect()
        return (mouse_pos[0] - panel_rect.x, mouse_pos[1] - panel_rect.y)

    def slot_position(self, index):
        return (
            self.script_area_rect.x + self.LANE_PADDING_X,
            self.script_area_rect.y + self.LANE_HEADER_HEIGHT + (index * self.slot_spacing),
        )

    def relayout_program_blocks(self):
        for index, block in enumerate(self.program_blocks):
            block.set_target(self.slot_position(index))

    def script_drop_rect(self):
        return Rect(
            (
                self.script_area_rect.x + 6,
                self.script_area_rect.y + self.LANE_HEADER_HEIGHT,
            ),
            (
                self.script_area_rect.width - 12,
                self.script_area_rect.height - self.LANE_HEADER_HEIGHT - self.LANE_BOTTOM_PADDING,
            ),
        )

    def drag_position(self, mouse_pos):
        local_x, local_y = self.panel_local_pos(mouse_pos)
        return (
            local_x - self.drag_offset.x,
            local_y - self.drag_offset.y,
        )

    def start_drag(self, block, mouse_pos, was_new):
        self.dragged_block = block
        self.drag_was_new = was_new
        block.button.change_layer(30)
        block.remove_button.change_layer(31)
        local_x, local_y = self.panel_local_pos(mouse_pos)
        button_rect = block.button.get_relative_rect()
        self.drag_offset = Vector2(
            local_x - button_rect.x,
            local_y - button_rect.y,
        )

        if was_new:
            self.drag_original_index = None
        elif block in self.program_blocks:
            self.drag_original_index = self.program_blocks.index(block)
            self.program_blocks.pop(self.drag_original_index)
            self.relayout_program_blocks()
        else:
            self.drag_original_index = None
            self.drag_was_new = True

        self.move_dragged_block(mouse_pos)
        self.refresh_status()

    def move_dragged_block(self, mouse_pos):
        if self.dragged_block is None:
            return

        self.dragged_block.set_position(self.drag_position(mouse_pos))

    def get_drop_index(self, mouse_pos):
        if self.dragged_block is None:
            return None

        dragged_rect = self.dragged_block.button.get_relative_rect()
        block_center = dragged_rect.center
        drop_rect = self.script_drop_rect().inflate(24, 12)

        if not drop_rect.collidepoint(block_center) and not drop_rect.colliderect(dragged_rect):
            return None

        lane_top = drop_rect.y
        lane_bottom = min(
            drop_rect.bottom - self.slot_size[1],
            lane_top + ((self.PROGRAM_LIMIT - 1) * self.slot_spacing),
        )
        clamped_y = max(lane_top, min(block_center[1] - (self.slot_size[1] // 2), lane_bottom))
        relative_y = clamped_y - lane_top
        index = round(relative_y / self.slot_spacing)
        return max(0, min(index, len(self.program_blocks)))

    def finish_drag(self, mouse_pos):
        if self.dragged_block is None:
            return

        dragged_block = self.dragged_block
        drop_index = self.get_drop_index(mouse_pos)
        if drop_index is not None and len(self.program_blocks) < self.PROGRAM_LIMIT:
            self.program_blocks.insert(drop_index, dragged_block)
            dragged_block.set_position(self.slot_position(drop_index))
            self.relayout_program_blocks()
        elif self.drag_was_new:
            self.destroy_script_block(dragged_block)
        else:
            restore_index = min(self.drag_original_index, len(self.program_blocks))
            self.program_blocks.insert(restore_index, dragged_block)
            self.relayout_program_blocks()

        if dragged_block.button.alive():
            dragged_block.button.change_layer(self.SCRIPT_BLOCK_LAYER)
            dragged_block.remove_button.change_layer(self.SCRIPT_BLOCK_LAYER + 1)

        self.dragged_block = None
        self.drag_offset = Vector2()
        self.drag_original_index = None
        self.drag_was_new = False
        self.refresh_status()

    def append_block_to_program(self, spec):
        if len(self.program_blocks) >= self.PROGRAM_LIMIT:
            self.refresh_status()
            return

        new_block = self.create_script_block(spec, self.slot_position(len(self.program_blocks)))
        self.program_blocks.append(new_block)
        self.relayout_program_blocks()
        self.refresh_status()

    def script_block_at_pos(self, mouse_pos):
        for block in reversed(self.program_blocks):
            if block.button.get_abs_rect().collidepoint(mouse_pos):
                return block
        return None

    def palette_spec_at_pos(self, mouse_pos):
        for button, spec in self.palette_button_to_spec.items():
            if button.get_abs_rect().collidepoint(mouse_pos):
                return spec
        return None

    def clear_program(self):
        if self.is_running:
            return

        for block in self.program_blocks:
            self.destroy_script_block(block)
        self.program_blocks.clear()
        self.next_step_index = 0
        self.refresh_status()

    def remove_program_block(self, block):
        if self.is_running or block not in self.program_blocks:
            return

        self.program_blocks.remove(block)
        self.destroy_script_block(block)
        self.relayout_program_blocks()
        self.refresh_status()

    def start_program(self):
        if self.is_running or not self.program_blocks:
            return

        self.is_running = True
        self.next_step_index = 0
        self.refresh_status()

    def reset_current_level(self):
        reset_event = pygame.event.Event(RESET_ENV_CONFIRMED)
        pygame.event.post(reset_event)

    def run_next_step(self):
        if not self.is_running or self.player.is_moving:
            return

        if self.next_step_index >= len(self.program_blocks):
            self.is_running = False
            self.next_step_index = 0
            self.refresh_status()
            return

        block = self.program_blocks[self.next_step_index]
        self.player.do_action(block.spec.action, x=block.spec.x, y=block.spec.y)
        self.next_step_index += 1
        self.refresh_status()

    def undo_step(self):
        if self.is_running or not self.program_blocks:
            return

        block = self.program_blocks.pop()
        self.destroy_script_block(block)
        self.refresh_status()

    def process_event(self, event):
        super().process_event(event)

        if self.is_running:
            return

        if event.type == MOUSEMOTION and self.dragged_block is not None:
            self.move_dragged_block(event.pos)
            return

        if event.type == MOUSEBUTTONUP and event.button == 1 and self.dragged_block is not None:
            self.finish_drag(event.pos)
            return

        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos

            block = self.script_block_at_pos(mouse_pos)
            if block is not None:
                self.start_drag(block, mouse_pos, was_new=False)
                return

        if event.type == UI_BUTTON_START_PRESS and event.ui_element in self.palette_button_to_spec:
            spec = self.palette_button_to_spec[event.ui_element]
            self.palette_drag_source = event.ui_element
            mouse_pos = getattr(event, "mouse_pos", event.ui_element.get_abs_rect().center)
            new_block = self.create_script_block(spec, self.panel_local_pos(mouse_pos))
            self.start_drag(new_block, mouse_pos, was_new=True)
            return

        if event.type != UI_BUTTON_PRESSED:
            return

        if event.ui_element == self.palette_drag_source:
            self.palette_drag_source = None
            return

        if event.ui_element in self.palette_button_to_spec:
            self.palette_drag_source = None
            self.append_block_to_program(self.palette_button_to_spec[event.ui_element])
            return

        if event.ui_element in self.remove_button_to_block:
            self.remove_program_block(self.remove_button_to_block[event.ui_element])
            return

        if event.ui_element == self.run_button:
            self.start_program()
            return

        if event.ui_element == self.undo_button:
            self.undo_step()
            return

        if event.ui_element == self.clear_button:
            self.clear_program()
            return

        if event.ui_element == self.reset_button:
            self.reset_current_level()
            return

    def update(self, delta_time):
        super().update(delta_time)

        for block in self.program_blocks:
            if block is not self.dragged_block:
                block.update()

        if self.dragged_block is not None:
            self.dragged_block.update()

        self.run_next_step()
