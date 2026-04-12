from pygame import image, Rect, Surface
from pygame_gui.elements import UIImage, UIPanel, UILabel
from pygame_gui import *
from game.core.constants import *
from game.core.ui import TypingTextBox, UIFactory
from game.core.csv_support import *

# The popup that comes up at the start of every game in 'environments/game.py'
class DialoguePanel(UIPanel):
    def __init__(self, panel_pos, panel_size, text, manager):
        # Setting the starting height to 5 here since it should be above any other ui panels to be rendered
        super().__init__(Rect(panel_pos, panel_size), manager=manager, object_id="#dialouge_panel", starting_height=5)
        
        self.create_ui(text, panel_size)

    def create_ui(self, text, panel_size):    
        # this is prlly not the best for now of setting pos/size but its only as a temp measure untill we decide how we want to talk to the user to look like
        padding = 10
        ui_size = (panel_size[0]-padding*2, panel_size[1]//3-padding*2) 

        # Renders the typing text box that updates the typing every frame
        text_pos = (padding,padding)
        self.text_box = TypingTextBox(
            pos=text_pos,
            size=ui_size,
            html_text=text,
            manager=self.ui_manager,
            container=self,
            object_id="#dialogue",
            typing_speed=30,)

        # Confirmation button to exit the panel
        conf_pos = (padding, panel_size[1] - ui_size[1] - padding)
        self.confirm = UIFactory.button_img(
            pos=conf_pos, 
            size=ui_size, 
            image_path="game/assets/menu/button.png", 
            text="Confirm", 
            manager=self.ui_manager,
            container=self,
            object_id="#transparent_button")

    def process_event(self, event):
        super().process_event(event)
        if self.confirm.button.on_click(event):
            # Deletes this panel
            self.kill()

    def update(self, delta_time):
        super().update(delta_time)
        # Moving the scrolling text 
        self.text_box.update_typing(delta_time)
        pass

# The main class that each tile is using so that they can be rendered on the board map
class Tile(UIImage):
    def __init__(self, start_pos, tiles_size, tiles_amm, img_path, manager, container=None, tile=None):
        self.x = start_pos[0]
        self.y = start_pos[1]

        self.tiles_size = tiles_size
        self.tiles_amm = tiles_amm
        
        self.create_ui(img_path, tile, manager, container)

    # Renders the image on the screen based on values, if tile value is passed through, the image is cropped to the tile value
    def create_ui(self, img_path, tile, manager, container):
        root_path = f'game/assets/{img_path}'
        if tile == None:
            loaded_image = image.load(root_path).convert_alpha()
        else:
            loaded_image = cut_graphics(root_path, tile)

        rect = Rect((0,0),(self.tiles_size))
        super().__init__(relative_rect=rect, image_surface=loaded_image, manager=manager, container=container)
        self.update_screen_pos()

    # Sets self.x,y values to make sure it cant go out of bounds
    def set_screen_inbounds(self):
        if self.x < 0:
            self.x = 0
        elif self.x > self.tiles_amm[0] - 1:
            self.x = self.tiles_amm[0] -1
        if self.y < 0:
            self.y = 0
        elif self.y > self.tiles_amm[1] - 1:
            self.y = self.tiles_amm[1] -1

    # This is called when the element is to be updated on the screen
    def update_screen_pos(self):
        self.set_screen_inbounds()
        x = self.x * self.tiles_size[0]
        y = self.y * self.tiles_size[1]
        self.set_relative_position((x, y))

    # This is a temp function of how the player can move, this is called in 'app/code_blocks.py'
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
    
    # Check if element is ontop of another
    def collision_check(self, obj):
        x = self.x == obj.x
        y = self.y == obj.y
        if x and y: 
            return True
        return False

    def update(self, delta_time):
        super().update(delta_time)
        # Here possibly update tiles that will be animated, but dont update all the time
        # Needs to be a conditioned or else every single tile is being updated every frame

# Making the level text a ui panel so that it can change heights and not be lost in the rendering order
class LevelText(UIPanel):
    def __init__(self, panel_pos, panel_size, text, manager):
        # Setting the starting height to 4 here since it should be above any other ui panels to be rendered, but below the dialouge text
        super().__init__(Rect(panel_pos, panel_size), manager=manager, object_id="#transparent_panel", starting_height=4)

        # for some reason im having trouble using the theme.json aswell for this panel to set the image so ive just put the image as an element
        img = image.load('game/assets/menu/button.png').convert_alpha()
        UIImage(
            relative_rect=Rect((0,0), panel_size), 
            image_surface=img, 
            manager=self.ui_manager, 
            container=self)
        UILabel(relative_rect=Rect((0,0),panel_size),
            text=text,
            manager=self.ui_manager,
            container=self)