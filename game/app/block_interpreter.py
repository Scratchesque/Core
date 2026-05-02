from pygame import Rect, Vector2, MOUSEBUTTONUP
from pygame_gui.elements import UIPanel, UITextBox

from game.app.block_registry import get_block_library
from game.support.ui import UIFactory

class Interpreter:
    GAP = ' ' * 4
    MIN_CODE_LINES = 40

    def _change_min_lines(self, amm):
        self.MIN_CODE_LINES = amm

    def _translate_blocks(self):

        program_blocks = self.class_list + self.block_list

        while len(program_blocks) < self.MIN_CODE_LINES:
            program_blocks.append('')

        script_str = ""
        for index, string in enumerate(program_blocks):
            number_index = index + 1
            script_str += f'{(number_index):2} |  <b>{string}</b>\n'
            
        return script_str

    def _format_spec_class(self, spec):
        class_font = self._type_to_font(f'{self.GAP}{(spec.label).replace(' ','')}',spec.action)
        class_text = [f'{class_font}():']

        player_font = self._type_to_font('Player', 'main')
        x_font = self._type_to_font('X', 'vars')
        y_font = self._type_to_font('Y', 'vars')

        text_list = []
        if 'loop' == spec.id:
            return []
        if 'jump' == spec.id:
            jump_font = f'{self.GAP*2}{player_font}.{y_font}'
            text_list.append(f'{jump_font} = 1')
            text_list.append(f'{jump_font} = -1')
        elif 'jump' in spec.id:
            jump_font = self._type_to_font('Jump', spec.action)
            text_list.append(f'{self.GAP*2}{jump_font}()')
        if spec.x != 0:
            text_list.append(f'{self.GAP*2}{player_font}.{x_font} = {spec.x}')
        elif spec.y != 0:
            text_list.append(f'{self.GAP*2}{player_font}.{y_font} = {spec.y}')

        return class_text + text_list + ['']

    def _format_spec_code(self, spec, func_gap=False):
        func_gap_str = self.GAP*2 if func_gap else self.GAP

        class_font = self._type_to_font('Blocks','main')
        spec_font = self._type_to_font(f'{(spec.label).replace(' ','')}', spec.action)
        return f'{func_gap_str}{class_font}.{spec_font}()'
    
    @staticmethod
    def _type_to_font(text, type):
        match type:
            case 'main':
                colour = '687078'
            case 'vars':
                colour = '76E01F'
            case 'loop':
                colour = 'C20017'
            case 'jump':
                colour = 'B603FC'
            case _:
                colour = '4C97FF'

        return f'<font color=#{colour}>{text}</font>'

class InterpreterPanel(UIPanel, Interpreter):
    PANEL_WIDTH = 350
    PULL_BUTTON_SIZE = (30, 30) 

    def __init__(self, panel_pos, panel_size, manager, allowed_blocks, level_title):
        self.level_title = level_title 
        self.size = Vector2(self.PANEL_WIDTH, panel_size[1])
        self.pos = Vector2(panel_pos)

        super().__init__(
            relative_rect=Rect(panel_pos,self.size),
            starting_height=3,
            manager=manager,
            object_id="#interpreter_panel"
        )

        self.block_library = get_block_library(allowed_blocks)
        self.is_moving = False
        self.is_visible = False
        self.move_timer = 0

        self.create_ui()

        self._make_classes()
        self._make_blocks([])
        
        block_text = self._translate_blocks()
        self.text_box.set_text(block_text)

    def create_ui(self):
        padding = 10
        text_size = (self.size.x-padding*2, self.size.y-padding*2)

        self.text_box = UITextBox(
            relative_rect=Rect(
                (padding-5, padding-5), 
                text_size
            ), 
            html_text='', 
            manager=self.ui_manager, 
            container=self, 
            object_id='#text_code',
            visible=0
        )
        self.pull_button = UIFactory.button_img(
            pos=(0,0),
            size=self.PULL_BUTTON_SIZE,
            image_path="game/assets/SproutLands/cropped/brown_block.png",
            text='<',
            manager=self.ui_manager,
            object_id='#transparent'
        )
        self.pull_button.change_layer(5)
        self._update_button_pos()

    def process_event(self, event):
        if self.is_moving:
            return
        
        if self.pull_button.on_click(event):
            if self.is_visible == True:
                self.is_visible = False
                self.pull_button.set_text('<')
            else:
                self.text_box.visible = 1
                self.is_visible = True
                self.pull_button.set_text('>')
            self.move_timer = 10
            self.is_moving = True
            pass

    def update(self, time_delta):
        if not self.is_moving:
            return
        
        self.move_timer -= 1
        self.progress = 1 - (self.move_timer / 10)

        if self.move_timer <= 0:
            self.is_moving = False
            if not self.is_visible:
                self.text_box.visible = 0
            return
        
        self._update_pos()

    def update_text(self, program_blocks):
        self._make_blocks(program_blocks)
        block_text = self._translate_blocks()
        self.text_box.set_text(block_text)

    def _update_pos(self):
        distance = self.PANEL_WIDTH/4.5
        offset = self.progress * (distance if self.is_visible else -distance)

        self.pos.x-=int(offset)

        self.set_relative_position(self.pos)
        self._update_button_pos()

    def _update_button_pos(self):
        rect = self.get_relative_rect() 
        left = (rect.left)
        center = (rect.center)[1]
        self.pull_button.set_relative_position((left-self.PULL_BUTTON_SIZE[1]-10,center))

    def _make_classes(self):
        font_text = self._type_to_font('Blocks', 'main')
        self.class_list = [f'Class {font_text}:']
        for spec in self.block_library:
            self.class_list += self._format_spec_class(spec) 

    def _make_blocks(self, program_blocks):
        font_text = self._type_to_font(self.level_title, 'main')
        self.block_list =  [f'Script {font_text}:']
        for block in program_blocks:
            if 'loop' == block.spec.id:
                loop_font = self._type_to_font('Loop', block.spec.id)
                self.block_list.append(f'{self.GAP}{loop_font} ({block.repeat_count}):')

                for child in block.children_blocks:
                    self.block_list.append(self._format_spec_code(child.spec, func_gap=True))
            else:
                self.block_list.append(self._format_spec_code(block.spec))
        