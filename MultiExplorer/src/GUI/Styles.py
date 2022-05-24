import sys
import ttk
from enum import Enum


class DefaultStyleSettings:
    bg_color = '#d9d9d9'  # X11 color: 'gray85'
    fg_color = '#000000'  # X11 color: 'black'
    selected_color = '#d9d9d9'  # X11 color: 'gray85'
    active_color = '#ececec'  # Closest X11 color: 'gray92'
    font = "TkDefaultFont"

    input_bg_color = "white"
    input_font = "TkFixedFont"
    input_selected_bg_color = "blue"
    input_selected_fg_color = "white"

    button_active_bg_color = "#f9f9f9"
    button_border_width = "2"


class DefaultStyle(ttk.Style):
    def __init__(self):
        super(DefaultStyle, self).__init__()

        if sys.platform == "win32":
            self.theme_use('winnative')

        self.configure('.', background=DefaultStyleSettings.bg_color)

        self.configure('.', foreground=DefaultStyleSettings.fg_color)

        self.configure('.', font=DefaultStyleSettings.font)

        self.map('.', background=[('selected', DefaultStyleSettings.selected_color),
                                  ('active', DefaultStyleSettings.active_color)])
