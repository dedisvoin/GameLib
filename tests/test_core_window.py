import importer

from src.core import window

win = window._Window()

while win.is_opened:
    win._update()
    win._update_state()
