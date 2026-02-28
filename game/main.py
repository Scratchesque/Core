from game.window.display import Display as main_window
from game.window.controls import testing

if __name__ == '__main__':
    main_window.init(200,200)

    testing()

    main_window.quit_screen()
   
    