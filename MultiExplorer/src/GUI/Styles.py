import sys
from ttk import Style
from Tkinter import PhotoImage
from PIL import Image, ImageTk

from MultiExplorer.src.config import PATH_IMG


class MultiStyle(object):
    @staticmethod
    def get_image(file_name, size):
        # type: (str, tuple) -> PhotoImage
        photo = Image.open(PATH_IMG + "/" + file_name)

        return ImageTk.PhotoImage(photo.resize(size))


class DefaultStyle(Style, MultiStyle):
    padx = 50

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

    def __init__(self):
        super(DefaultStyle, self).__init__()

        if sys.platform == "win32":
            self.theme_use('winnative')

        self.configure('.', background=DefaultStyle.bg_color)

        self.configure('.', foreground=DefaultStyle.fg_color)

        self.configure('.', font=DefaultStyle.font)

        self.map('.', background=[('selected', DefaultStyle.selected_color),
                                  ('active', DefaultStyle.active_color)])
