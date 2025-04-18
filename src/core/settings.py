import pygame
from typing import Any, Final
pygame.init()

"""
This 'settings.py' file contains global configuration parameters for the game:

This file serves as a central location for game settings and constants that can be
imported and used throughout the project. Having settings in a separate file makes
it easier to modify game parameters without changing the main game logic.
"""



# WINDOW SETTINGS ==============================================================================

WINDOW_SIZE = [1500, 800]                                             # ( standart window size )
WINDOW_TITLE = "GameLib"                                             # ( standart window title )
WINDOW_RESIZIBLE = True                                                   # ( window resizable )
WINDOW_VSYNC = True                                                           # ( window vsync )
WINDOW_QUIT_KEY = 'esc'                                                    # ( window quit key )    
WINDOW_WAITED_FPS = 60                                                # ( window max framerate )
WINDOW_BG_COLOR = (255, 255, 255)                                 # ( window back ground color )
WINDOW_DELTA_MATCH_FPS = 60                                            # ( fps for match delta )


# 'CONST_WINDOW_RESIZABLE' constant for window can be resized
CONST_WINDOW_RESIZABLE: Final = pygame.RESIZABLE 

# 'CONST_WINDOW_FULLSCREEN' constant for window can be fullscreen
CONST_WINDOW_FULLSCREEN: Final = pygame.FULLSCREEN

# 'CONST_WINDOW_NOFRAME' constant for window can be noframe
CONST_WINDOW_NOWRAME: Final = pygame.NOFRAME

# `CONST_WINDOW_MAX_FPS` constant for window can be max fps
CONST_WINDOW_MAX_FPS: Final = 10000

# `CONST_WINDOW_CONSOLE_FPS` constant for window can be `30` fps
CONST_WINDOW_CONSOLE_FPS: Final = 30

# WINDOW SETTINGS ==============================================================================

# MOUSE SETTINGS ===============================================================================

# 'CONST_MOUSE_BUTTON_LEFT' constant for mouse button left
CONST_MOUSE_BUTTON_LEFT: Final = 'mouse_btn_left'

# 'CONST_MOUSE_BUTTON_RIGHT' constant for mouse button right
CONST_MOUSE_BUTTON_RIGHT: Final = 'mouse_btn_right'

# 'CONST_MOUSE_BUTTON_MIDDLE' constant for mouse button middle
CONST_MOUSE_BUTTON_MIDDLE: Final = 'mouse_btn_middle'

# MOUSE SETTINGS ===============================================================================

# INPUT EVENT TYPES ============================================================================

# 'CONST_NOUSE_BUTTON_CLICK_EVENT' constant for button click event type
CONST_MOUSE_BUTTON_CLICK_EVENT: Final = 'btn_click_event'

# 'CONST_MOUSE_BUTTON_PRESS_EVENT' constant for button press event type
CONST_MOUSE_BUTTON_PRESS_EVENT: Final = 'btn_press_event'

# 'CONST_KEY_CLICK_EVENT' constant for mouse click event type
CONST_KEY_CLICK_EVENT: Final = 'key_click_event'

# 'CONST_KEY_PRESS_EVENT' constant for mouse press event type
CONST_KEY_PRESS_EVENT: Final = 'key_press_event'

# 'CONST_MOUSE_BUTTON_DOUBLE_CLICK_EVENT' constant for mouse double click event type
CONST_MOUSE_BUTTON_DOUBLE_CLICK_EVENT: Final = 'btn_double_click_event'

# 'CONST_KEY_DOUBLE_CLICK_EVENT' constant for key double click event type
CONST_KEY_DOUBLE_CLICK_EVENT: Final = 'key_double_click_event'

DOUBLE_CLICK_INTERVAL = 500                                          # ( double click interval )
 
# INPUT EVENT TYPES ============================================================================