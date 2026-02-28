import pygame

class Display:
    # manual init only when first created so we can call this class over and over
    def init(screen_width=700, screen_height=500):
        pygame.display.init()
        pygame.display.set_mode([screen_width, screen_height])

        Display.set_caption("Scratchesque")
        # Display.set_icon(r"Path/ICON.jpg")
        
      
    def set_caption(text):
        pygame.display.set_caption(text)

    def set_icon(path):
        icon = pygame.image.load(path)
        pygame.display.set_icon(icon)
    
    def get_screen():
        return pygame.display.get_surface()

    def update_screen(list=None):
        return pygame.display.update(list)
    
    def quit_screen():
        input('Enter any key to exit > ')
        pygame.display.quit()
        exit()
