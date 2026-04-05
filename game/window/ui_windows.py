from pygame_gui.elements import UIImage, UIWindow, UILabel, UITextEntryLine, UIScreenSpaceHealthBar, UIHorizontalSlider
import pygame

class ScalingWindow(UIWindow):
    def __init__(self, rect, ui_manager):
        super().__init__(rect, ui_manager,
                         window_display_title='Scale',
                         object_id='#scaling_window',
                         resizable=True)

        loaded_test_image = pygame.image.load('game/assets/SproutLands/Tilesets/Wooden House.png').convert_alpha()
        self.test_image = UIImage(pygame.Rect((10, 10), (self.get_container().get_size()[0] - 20,
                                                         self.get_container().get_size()[1] - 20)),
                                  loaded_test_image, self.ui_manager,
                                  container=self,
                                  anchors={'top': 'top', 'bottom': 'bottom',
                                           'left': 'left', 'right': 'right'})

        self.set_blocking(True)

class EverythingWindow(UIWindow):
    def __init__(self, rect, ui_manager):
        super().__init__(rect, ui_manager,
                         window_display_title='Everything Container',
                         object_id='#everything_window',
                         resizable=True)

        self.test_slider = UIHorizontalSlider(pygame.Rect((int(self.rect.width / 2),
                                                           int(self.rect.height * 0.70)),
                                                          (240, 25)),
                                              50.0,
                                              (0.0, 100.0),
                                              self.ui_manager,
                                              container=self,
                                              click_increment=5)

        self.slider_label = UILabel(pygame.Rect((int(self.rect.width / 2) + 250,
                                                 int(self.rect.height * 0.70)),
                                                (28, 25)),
                                    str(int(self.test_slider.get_current_value())),
                                    self.ui_manager,
                                    container=self)

        self.test_text_entry = UITextEntryLine(pygame.Rect((int(self.rect.width / 2),
                                                            int(self.rect.height * 0.50)),
                                                           (200, -1)),
                                               self.ui_manager,
                                               container=self)
        self.test_text_entry.set_forbidden_characters('numbers')

        self.health_bar = UIScreenSpaceHealthBar(pygame.Rect((int(self.rect.width / 9),
                                                              int(self.rect.height * 0.7)),
                                                             (200, 30)),
                                                 self.ui_manager,
                                                 container=self)

        loaded_test_image = pygame.image.load('game/assets/SproutLands/Tilesets/Wooden House.png').convert_alpha()

        self.test_image = UIImage(pygame.Rect((int(self.rect.width / 9),
                                               int(self.rect.height * 0.3)),
                                              loaded_test_image.get_rect().size),
                                  loaded_test_image, self.ui_manager,
                                  container=self)

    def update(self, time_delta):
        super().update(time_delta)

        if self.alive() and self.test_slider.has_moved_recently:
            self.slider_label.set_text(str(int(self.test_slider.get_current_value())))
