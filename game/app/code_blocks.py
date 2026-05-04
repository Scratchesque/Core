from pygame import MOUSEBUTTONUP, MOUSEMOTION, Rect
from pygame.math import Vector2
from pygame_gui.elements import UIButton, UILabel, UIPanel, UITextBox
from pygame_gui._constants import UI_BUTTON_PRESSED, UI_BUTTON_START_PRESS

from game.app.block_registry import get_block_library
from game.core.events import *


class ScriptBlock(UIPanel):
    REMOVE_BUTTON_SIZE = 24
    REMOVE_BUTTON_OFFSET = 6
    SCRIPT_BLOCK_LAYER = 6

    def __init__(self, position, size, manager, container, spec):
        super().__init__(Rect((0,0),(0,0)), 0, manager)
        self.container = container
        self.spec = spec
        self.size = Vector2(size)
        self.position = Vector2(position)
        self.target_position = Vector2(position)
        self.parent_block = None

        self.create_ui()

    def create_ui(self):
        self.button = UIButton(
            relative_rect=Rect(self.position, self.size),
            text=self.spec.label,
            manager=self.ui_manager,
            container=self.container,
            object_id=self.spec.object_id,
            starting_height=self.SCRIPT_BLOCK_LAYER,
        )
        self.remove_button = UIButton(
            relative_rect=Rect(
                (
                    self.position.x + self.size.x - self.REMOVE_BUTTON_SIZE - self.REMOVE_BUTTON_OFFSET,
                    self.position.y + self.REMOVE_BUTTON_OFFSET,
                ),
                (self.REMOVE_BUTTON_SIZE, self.REMOVE_BUTTON_SIZE),
            ),
            text="X",
            manager=self.ui_manager,
            container=self.container,
            object_id="#remove_block_button",
            starting_height=self.SCRIPT_BLOCK_LAYER + 1,
        )

    def process_event(self, event):
        if event.type == UI_BUTTON_PRESSED:
            if event.ui_element == self.remove_button:
                self.container.remove_script_block(self)

    def sync_controls(self):
        x = int(self.position.x)
        y = int(self.position.y)

        if self.parent_block is None:
            self.button.set_dimensions(self.size)
        else: 
            self.button.set_dimensions((self.size.x-LoopBlock.CHILD_INDENT_X, self.size.y))

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

    def update(self, delta_time):
        if self.position.distance_squared_to(self.target_position) < 1:
            self.position = self.target_position.copy()
        else:
            self.position += (self.target_position - self.position) * 0.35
        self.sync_controls()

    def kill(self):
        super().kill()
        self.button.kill()
        self.remove_button.kill()

class LoopBlock(ScriptBlock):
    FOOTER_HEIGHT = 10
    CHILD_INDENT_X = 24
    MIN_REPEAT = 1
    MAX_REPEAT = 4
    CHILD_SLOT_SPACING = 55

    def __init__(self, position, size, manager, container, spec):

        self.children_blocks = []
        self.repeat_count = 2
        self.position = Vector2(position)
        self.target_position = Vector2(position)

        super().__init__(position, size, manager, container, spec)
        
    def create_ui(self):
        super().create_ui()

        self.dec_button = UIButton(
            relative_rect=Rect((self.position.x + 110, self.position.y + 8), (24, 24)),
            text="−",
            manager=self.ui_manager,
            container=self.container,
            object_id="#loop_count_btn",
            starting_height=self.SCRIPT_BLOCK_LAYER + 1,
        )
        self.inc_button = UIButton(
            relative_rect=Rect((self.position.x + 166, self.position.y + 8), (24, 24)),
            text="+",
            manager=self.ui_manager,
            container=self.container,
            object_id="#loop_count_btn",
            starting_height=self.SCRIPT_BLOCK_LAYER + 1,
        )
        self.footer_panel = UIPanel(
            relative_rect=Rect((self.position.x, self.position.y + self.size.y), (self.size.x, self.FOOTER_HEIGHT)),
            manager=self.ui_manager,
            container=self.container,
            starting_height=self.SCRIPT_BLOCK_LAYER,
        )
        self.count_label = UILabel(
            relative_rect=Rect((self.position.x + 136, self.position.y + 10), (28, 20)),
            text=str(self.repeat_count),
            manager=self.ui_manager,
            container=self.container,
            object_id="#loop_count_txt"
        )
        self.count_label.change_layer(self.SCRIPT_BLOCK_LAYER + 1)

    def total_height(self):
        child_area = len(self.children_blocks) * self.CHILD_SLOT_SPACING if self.children_blocks else self.CHILD_SLOT_SPACING
        return self.size.y + child_area + self.FOOTER_HEIGHT

    def child_slot_y(self, child_index):
        return self.size.y + child_index * self.CHILD_SLOT_SPACING

    def update_count(self, ammount):
        if self.container.is_running:
            return
        self.repeat_count += ammount
        if self.repeat_count > self.MAX_REPEAT: 
            self.repeat_count = self.MAX_REPEAT
        elif self.repeat_count < self.MIN_REPEAT:
            self.repeat_count = self.MIN_REPEAT
        self.count_label.set_text(str(self.repeat_count))
        self.container.refresh_status()

    def sync_controls(self):
        super().sync_controls()
        x = int(self.position.x)
        y = int(self.position.y)

        btn_size = 24
        label_w = 28
        group_x = x + 75
        btn_y = y + 13

        self.dec_button.set_relative_position((group_x, btn_y))
        self.count_label.set_relative_position(((group_x + btn_size + 2, btn_y + 2)))
        self.inc_button.set_relative_position((group_x + btn_size + 2 + label_w + 2, btn_y))

        footer_y = y + self.total_height() - self.FOOTER_HEIGHT
        self.footer_panel.set_relative_position((x, footer_y))

        child_x = x + self.CHILD_INDENT_X
        for i, child in enumerate(self.children_blocks):
            cy = y + self.child_slot_y(i)
            child.set_target((child_x, cy))

    def process_event(self, event):
        super().process_event(event)
        if event.type == UI_BUTTON_PRESSED:
            if event.ui_element == self.dec_button:
                self.update_count(-1)
            if event.ui_element == self.inc_button:
                self.update_count(1)

    def update(self, delta_time):
        super().update(delta_time)
        for child in self.children_blocks:
            child.update(delta_time)

    def kill(self):
        super().kill()
        self.dec_button.kill()
        self.inc_button.kill()
        self.count_label.kill()
        self.footer_panel.kill()
        for child in self.children_blocks:
            child.kill()
        self.children_blocks.clear()

class CodeBlocks(UIPanel):
    SCRIPT_PROGRAM_LIMIT = 8
    LOOP_PROGRAM_LIMIT = 2
    LOOP_CHILD_LIMIT = 4
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

    def __init__(self, panel_pos, panel_size, manager, player, allowed_blocks=None, level_script=None):
        super().__init__(
            Rect(panel_pos, panel_size),
            manager=manager,
            object_id="#code_panel",
            starting_height=4,
        )

        self.player = player
        self.interpreter = None
        self.block_library = get_block_library(allowed_blocks)
        self.starting_blocks = level_script
        self.program_blocks = []
        self._exec_steps: list = []
        self.next_step_index = 0
        self.is_running = False
        self.dragged_block = None
        self.drag_offset = Vector2()
        self.drag_original_index = None
        self.drag_original_loop = None
        self.drag_was_new = False
        self.panel_size = panel_size
        self.palette_button_to_spec = {}
        self.script_button_to_block = {}
        self.palette_drag_source = None

        self.configure_layout()
        self.create_ui()
        self._make_start_script()
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
            object_id="#title",
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
                object_id=spec.object_id,
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

        lane_text_width = self.script_area_rect.width - (self.LANE_PADDING_X * 2)

        UILabel(
            relative_rect=Rect((self.LANE_PADDING_X, 12), (lane_text_width, 30)),
            text="Script Lane",
            manager=self.ui_manager,
            container=self.script_lane,
            object_id="#lane_title",
        )

        UILabel(
            relative_rect=Rect((self.LANE_PADDING_X, 42), (lane_text_width, 24)),
            text="Drag blocks here. Use x to remove one.",
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

    def set_interpreter(self, interpreter):
        self.interpreter = interpreter

    def update_interpreter(self):
        if self.interpreter is None: 
            return
        self.interpreter.update_text(self.program_blocks)

    def refresh_status(self):
        total_steps, total_blocks, _ = self._count_total_steps()
        if self.is_running:
            current_step = min(self.next_step_index + 1, len(self._exec_steps))
            status = (
                "<b>Status:</b> Running your script.<br>"
                f"Step {current_step} of {len(self._exec_steps)}."
            )
        elif total_blocks != 0:
            status = (
                "<b>Status:</b> Script ready.<br>"
                f"{total_blocks} Movement Blocks(s) in lane — {total_steps} total step(s)."
            )
            self.update_interpreter()
        else:
            status = (
                "<b>Status:</b> Build a short program.<br>"
                "Drag blocks into the lane. Add a Loop block to repeat steps."
            )
            self.update_interpreter()
        self.status_display.set_text(status)
 
    def _count_total_steps(self):
        count = 0
        blocks = 0
        loops = 0
        for item in self.program_blocks:
            if isinstance(item, LoopBlock):
                loops += 1
                count += len(item.children_blocks) * item.repeat_count
                blocks += len(item.children_blocks)
            else:
                count += 1
                blocks += 1
        return count, blocks, loops
    
    def _build_exec_steps(self):
        steps = []
        for item in self.program_blocks:
            if isinstance(item, LoopBlock):
                for _ in range(item.repeat_count):
                    for child in item.children_blocks:
                        steps.append(child.spec)
            else:
                steps.append(item.spec)
        return steps

    def create_script_block(self, spec, pos):
        args = dict(
            position=pos, 
            size=self.slot_size, 
            manager=self.ui_manager, 
            container=self, 
            spec=spec
        )
        if spec.id == 'loop':
            block = LoopBlock(**args)
        else:
            block = ScriptBlock(**args)
        self.script_button_to_block[block.button] = block
        return block

    def destroy_script_block(self, block):
        self.script_button_to_block.pop(block.button, None)
        if isinstance(block, LoopBlock):
            for child in block.children_blocks:
                self.script_button_to_block.pop(child.button, None)
        block.kill()

    def panel_local_pos(self, mouse_pos):
        panel_rect = self.get_abs_rect()
        return (mouse_pos[0] - panel_rect.x, mouse_pos[1] - panel_rect.y)

    def relayout_program_blocks(self):
        y = self.script_area_rect.y + self.LANE_HEADER_HEIGHT
        x = self.script_area_rect.x + self.LANE_PADDING_X
        for item in self.program_blocks:
            if isinstance(item, LoopBlock):
                item.set_target((x, y))
                y += item.total_height()
            else:
                item.set_target((x, y))
                y += self.slot_spacing

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
            self.drag_original_loop = None
        else:
            parent_block = block.parent_block
            if parent_block is not None and block in parent_block.children_blocks:
                self.drag_original_index = parent_block.children_blocks.index(block)
                self.drag_original_loop = parent_block
                parent_block.children_blocks.remove(block)
                block.parent_block = None
                self.relayout_program_blocks()
            elif block in self.program_blocks:
                self.drag_original_index = self.program_blocks.index(block)
                self.drag_original_loop = None
                self.program_blocks.pop(self.drag_original_index)
                self.relayout_program_blocks()
            else:
                self.drag_original_index = None
                self.drag_original_loop = None
                self.drag_was_new = True

        self.move_dragged_block(mouse_pos)
        self.refresh_status()

    def move_dragged_block(self, mouse_pos):
        if self.dragged_block is None:
            return

        self.dragged_block.set_position(self.drag_position(mouse_pos))

    def get_drop_index(self, mouse_pos):
        if self.dragged_block is None:
            return None, None

        dragged_rect = self.dragged_block.button.get_relative_rect()
        block_center = dragged_rect.center
        drop_rect = self.script_drop_rect().inflate(24, 12)

        if not drop_rect.collidepoint(block_center) and not drop_rect.colliderect(dragged_rect):
            return None, None
        
        if not self.script_lane.panel_container.rect.collidepoint(mouse_pos):
            return None, None

        running_y = self.script_area_rect.y + self.LANE_HEADER_HEIGHT
        for item in self.program_blocks:
            if isinstance(item, LoopBlock):
                child_top = running_y + self.slot_size[1]
                child_bottom = running_y + item.total_height() - LoopBlock.FOOTER_HEIGHT
                if (child_top <= block_center[1] < child_bottom
                        and self.script_area_rect.x <= block_center[0] < self.script_area_rect.right
                        and len(item.children_blocks) < self.LOOP_CHILD_LIMIT):
                    rel_y = block_center[1] - child_top
                    child_index = max(0, min(round(rel_y / LoopBlock.CHILD_SLOT_SPACING), len(item.children_blocks)))
                    return child_index, item
                running_y += item.total_height()
            else:
                running_y += self.slot_spacing

        lane_top = drop_rect.y
        lane_bottom = min(
            drop_rect.bottom - self.slot_size[1],
            lane_top + ((self.SCRIPT_PROGRAM_LIMIT - 1) * self.slot_spacing),
        )
        clamped_y = max(lane_top, min(block_center[1] - (self.slot_size[1] // 2), lane_bottom))
        relative_y = clamped_y - lane_top
        index = round(relative_y / self.slot_spacing)
        return max(0, min(index, len(self.program_blocks))), None

    def finish_drag(self, mouse_pos):
        if self.dragged_block is None:
            return

        dragged_block = self.dragged_block
        drop_index, target_loop = self.get_drop_index(mouse_pos)

        placed = False
        if drop_index is not None:
            _, total_blocks, total_loops = self._count_total_steps()
            if isinstance(dragged_block, LoopBlock):
                if total_loops >= self.LOOP_PROGRAM_LIMIT:
                    drop_index = None
            else:
                if total_blocks >= self.SCRIPT_PROGRAM_LIMIT:
                    drop_index = None

            if drop_index is not None and target_loop is not None:
                if isinstance(dragged_block, LoopBlock):
                    drop_index = None
                else:
                    target_loop.children_blocks.insert(drop_index, dragged_block)
                    dragged_block.parent_block = target_loop
                    self.relayout_program_blocks()
                    placed = True
            elif drop_index is not None:
                self.program_blocks.insert(drop_index, dragged_block)
                self.relayout_program_blocks()
                placed = True

        if not placed:
            if self.drag_was_new:
                self.destroy_script_block(dragged_block)
            else:
                if self.drag_original_loop is not None:
                    restore_index = min(self.drag_original_index, len(self.drag_original_loop.children_blocks))
                    self.drag_original_loop.children_blocks.insert(restore_index, dragged_block)
                    dragged_block.parent_block = self.drag_original_loop
                else:
                    restore_index = min(self.drag_original_index, len(self.program_blocks))
                    self.program_blocks.insert(restore_index, dragged_block)
                self.relayout_program_blocks()

        if dragged_block.button.alive():
            dragged_block.button.change_layer(ScriptBlock.SCRIPT_BLOCK_LAYER)
            dragged_block.remove_button.change_layer(ScriptBlock.SCRIPT_BLOCK_LAYER + 1)

        self.dragged_block = None
        self.drag_offset = Vector2()
        self.drag_original_index = None
        self.drag_original_loop = None
        self.drag_was_new = False
        self.refresh_status()

    def _make_start_script(self):
        if self.starting_blocks is None: return 
        for element_block in self.starting_blocks:
            spec = get_block_library([element_block])
            new_block = self.create_script_block(spec[0], (0, 0))
            self.program_blocks.append(new_block)
        self.relayout_program_blocks()
        self.refresh_status()
    
    def clear_program(self):
        if self.is_running:
            return
        for item in self.program_blocks:
            self.destroy_script_block(item)
        self.program_blocks.clear()
        self.next_step_index = 0
        self.refresh_status()

    def remove_script_block(self, block):
        if self.is_running:
            return

        if block.parent_block is not None:
            loop = block.parent_block
            if block in loop.children_blocks:
                loop.children_blocks.remove(block)
                block.parent_block = None
                self.destroy_script_block(block)
                self.relayout_program_blocks()
        else:
            self.program_blocks.remove(block)
            self.destroy_script_block(block)
            self.relayout_program_blocks()
        self.destroy_script_block(block)
        self.relayout_program_blocks()
        self.refresh_status()

    def start_program(self):
        if self.is_running or not self.program_blocks:
            return

        self._exec_steps = self._build_exec_steps()
        if not self._exec_steps:
            return
        self.is_running = True
        self.next_step_index = 0
        self.refresh_status()

    def reset_current_level(self):
        reset_event = pygame.event.Event(RESET_ENV_REQUESTED)
        pygame.event.post(reset_event)

    def run_next_step(self):
        if not self.is_running or self.player.is_moving:
            return

        if self.next_step_index >= len(self._exec_steps):
            self.is_running = False
            self.next_step_index = 0
            self._exec_steps = []
            self.player.deplete_energy()
            self.refresh_status()
            return

        spec = self._exec_steps[self.next_step_index]
        self.player.do_action(spec.action, x=spec.x, y=spec.y)
        self.next_step_index += 1
        self.refresh_status()

    def undo_step(self):
        if self.is_running or not self.program_blocks:
            return
        last = self.program_blocks[-1]
        if isinstance(last, LoopBlock):
            if last.children_blocks:
                child = last.children_blocks.pop()
                child.parent_block = None
                self.destroy_script_block(child)
            else:
                self.program_blocks.pop()
                self.destroy_script_block(last)
        else:
            self.program_blocks.pop()
            self.destroy_script_block(last)
        self.relayout_program_blocks()
        self.refresh_status()

    def process_event(self, event):
        if self.is_running:
            return

        if event.type == MOUSEMOTION and self.dragged_block is not None:
            self.move_dragged_block(event.pos)
            return

        if event.type == MOUSEBUTTONUP and event.button == 1 and self.dragged_block is not None:
            self.finish_drag(event.pos)
            return

        if event.type == UI_BUTTON_START_PRESS:
            if event.ui_element in self.palette_button_to_spec:
                spec = self.palette_button_to_spec[event.ui_element]
                self.palette_drag_source = event.ui_element
                mouse_pos = getattr(event, "mouse_pos", event.ui_element.get_abs_rect().center)
                if self.dragged_block is not None:
                    self.finish_drag(mouse_pos)
                new_block = self.create_script_block(spec, self.panel_local_pos(mouse_pos))
                self.start_drag(new_block, mouse_pos, was_new=True)
                return
            if event.ui_element in self.script_button_to_block:
                block = self.script_button_to_block[event.ui_element]
                mouse_pos = getattr(event, "mouse_pos", event.ui_element.get_abs_rect().topleft)
                if self.dragged_block is not None:
                    self.finish_drag(mouse_pos)
                self.start_drag(block, mouse_pos, was_new=False)
                return

        if event.type != UI_BUTTON_PRESSED:
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
        self.run_next_step()
