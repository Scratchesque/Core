from pygame import image, Rect
from pygame_gui.elements import UIImage, UIWindow, UIButton, UIPanel
from pygame_gui import *
from game.core.constants import *
from game.core.ui import TypingTextBox, UIFactory
import pygame

class DialoguePanel(UIPanel):
    def __init__(self, pos, size, text, ui_manager):
        super().__init__(pygame.Rect(pos, size), starting_height=5, manager=ui_manager, object_id="#dialouge_background")
        
        # this is prlly not the best for now of setting pos/size but its only as a temp measure untill we decide how we want to talk to the user to look like
        padding = 10
        ui_size = (size[0]-padding*2,size[1]//3-padding*2) 

        text_pos = (padding,padding)
        self.text_box = TypingTextBox(
            text_pos,
            ui_size,
            text,
            ui_manager,
            container=self.panel_container,
            object_id="#dialogue",
            typing_speed=30,
        )

        conf_pos = (padding, size[1] - ui_size[1] - padding)
        self.confirm = UIFactory.button_img(conf_pos, ui_size, "game/assets/menu/button.png", "Confirm", ui_manager, object_id="#transparent", container=self.panel_container)

    def on_ui_event(self, event):
        if self.confirm.button.on_click(event):
            self.kill()
        pass

    def update_frame(self, delta_time):
        self.text_box.update_typing(delta_time)
        pass

class MovementWindow(UIWindow):
    def __init__(self, rect, ui_manager, player):
        super().__init__(rect, ui_manager,
                         window_display_title='Movement',
                         object_id='#player_movement_window',
                         resizable=False)
        
        self.player = player

        UIButton(
            Rect((50,0), (100, 50)),
            "Up",
            manager=ui_manager,
            container=self,
            parent_element=self,
            object_id="#up",
        )

        UIButton(
            Rect((50,100), (100, 50)),
            "Down",
            manager=ui_manager,
            container=self,
            parent_element=self,
            object_id="#down",
        )

        UIButton(
            Rect((0,50), (100, 50)),
            "Left",
            manager=ui_manager,
            container=self,
            parent_element=self,
            object_id="#left",
        )

        UIButton(
            Rect((100,50), (100, 50)),
            "Right",
            manager=ui_manager,
            container=self,
            parent_element=self,
            object_id="#right",
        )

    def process_event(self, event):
        super().process_event(event)
        # here ive just used another way like object ids, to not save each button indivudually to their own self.xxxx
        if event.type == UI_BUTTON_PRESSED:
            if event.ui_object_id == '#player_movement_window.#up':
                self.player.move('U')
            if event.ui_object_id == '#player_movement_window.#down':
                self.player.move('D')
            if event.ui_object_id == '#player_movement_window.#left':
                self.player.move('L')
            if event.ui_object_id == '#player_movement_window.#right':
                self.player.move('R')

class TiledElement(UIImage):
    def __init__(self, start_pos, tiles_size, tiles_amm, img_path, ui_manager, container):
        self.pos = start_pos
        self.tiles_size = tiles_size
        self.tiles_amm = tiles_amm

        loaded_image = image.load(f'game/assets/{img_path}').convert_alpha()
        self.image_rect = loaded_image.get_rect()

        # calling this renders it to the screen via the ui_manager
        super().__init__(relative_rect=self.image_rect, image_surface=loaded_image, manager=ui_manager, container=container)
        self.set_dimensions(self.tiles_size)
        self.set_coord(start_pos)

    # sets the position it should be on the screen based on x,y values set earlier
    def set_coord(self, pos):
        x = pos[0]
        y = pos[1]
        if x < 0:
            x = 0
        elif x > self.tiles_amm[0] - 1:
            x = self.tiles_amm[0] -1
        if y < 0:
            y = 0
        elif y > self.tiles_amm[1] - 1:
            y = self.tiles_amm[1] -1

        x = x * self.tiles_size[0]
        y = y * self.tiles_size[1]

        self.set_relative_position((x, y))

    def move(self, direction):
        if direction == 'U':
            self.pos[1] -= 1
        if direction == 'D':
            self.pos[1] += 1           
        if direction == 'L':
            self.pos[0] -= 1
        if direction == 'R':
            self.pos[0] += 1

        self.set_coord(self.pos)
    
    # check if element is ontop of another
    def collision_check(self, obj):
        x = self.pos[0] == obj.pos[0]
        y = self.pos[1] == obj.pos[1]
        if x and y: 
            return True
        return False
