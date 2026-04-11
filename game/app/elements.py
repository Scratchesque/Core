from pygame import image, Rect, Surface
from pygame_gui.elements import UIImage, UIPanel
from pygame_gui import *
from game.core.constants import *
from game.core.ui import TypingTextBox, UIFactory
from game.core.csv_support import *

class DialoguePanel(UIPanel):
    def __init__(self, pos, size, text, ui_manager):
        super().__init__(Rect(pos, size), manager=ui_manager, object_id="#dialouge_background", starting_height=5)
        
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

    def process_event(self, event):
        super().process_event(event)
        if self.confirm.button.on_click(event):
            self.kill()

    def update(self, delta_time):
        super().update(delta_time)
        self.text_box.update_typing(delta_time)
        pass
        
class TiledElement(UIImage):
    def __init__(self, start_pos, tiles_size, tiles_amm, img_path, ui_manager, container=None, tile=None):
        self.x = start_pos[0]
        self.y = start_pos[1]

        self.tiles_size = tiles_size
        self.tiles_amm = tiles_amm

        img_path = f'game/assets/{img_path}'
        if tile == None:
            loaded_image = image.load(img_path).convert_alpha()
        else:
            loaded_image = cut_graphics(img_path, tile)
        rect = loaded_image.get_rect()

        # calling this renders it to the screen via the ui_manager
        super().__init__(relative_rect=rect, image_surface=loaded_image, manager=ui_manager, container=container)
        self.set_dimensions(self.tiles_size)
        self.update_screen_pos()

    # sets the position it should be on the screen based on x,y values set earlier
    def set_screen_inbounds(self):
        if self.x < 0:
            self.x = 0
        elif self.x > self.tiles_amm[0] - 1:
            self.x = self.tiles_amm[0] -1
        if self.y < 0:
            self.y = 0
        elif self.y > self.tiles_amm[1] - 1:
            self.y = self.tiles_amm[1] -1

    def update_screen_pos(self):
        self.set_screen_inbounds()
        x = self.x * self.tiles_size[0]
        y = self.y * self.tiles_size[1]
        self.set_relative_position((x, y))

    def move(self, direction):
        if direction == 'U':
            self.y -= 1
        if direction == 'D':
            self.y += 1
        if direction == 'L':
            self.x -= 1
        if direction == 'R':
            self.x += 1

        self.update_screen_pos()
    
    # check if element is ontop of another
    def collision_check(self, obj):
        x = self.x == obj.x
        y = self.y == obj.y
        if x and y: 
            return True
        return False

    def update(self, delta_time):
        super().update(delta_time)
        # this is uncessary cause it updates every frame, but then we can just change .x .y values without calling again
        # but it can be used for animating the player walking jumping etc possibly
        # This was most likely causeing the lag, just update when moving for animations
        