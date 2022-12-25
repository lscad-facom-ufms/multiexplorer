import Tkconstants
import Tkinter

from MultiExplorer.src.GUI.Styles import DefaultStyle

from Tkconstants import DISABLED as STATE_DISABLED, NORMAL as STATE_NORMAL
from Tkconstants import HORIZONTAL as HORIZONTAL_ORIENTATION, VERTICAL as VERTICAL_ORIENTATION
from Tkconstants import X as FILL_X, Y as FILL_Y, BOTH as FILL_BOTH
from Tkconstants import W as STICKY_WEST, E as STICKY_EAST
from Tkconstants import CENTER as ANCHOR_CENTER, NE as ANCHOR_NE, S as ANCHOR_SOUTH, W as ANCHOR_WEST
from Tkconstants import S as ANCHOR_S, N as ANCHOR_N, NW as ANCHOR_NW, SW as ANCHOR_SW, SE as ANCHOR_SE
from Tkconstants import BOTTOM as SIDE_BOTTOM, TOP as SIDE_TOP, LEFT as SIDE_LEFT, RIGHT as SIDE_RIGHT

from typing import Optional, Dict, Tuple


class WrappingLabel(Tkinter.Label, object):
    """
    A type of Label that automatically adjusts the wrap to the size
    """
    def __init__(self, master=None, cnf={}, **kw):
        super(WrappingLabel, self).__init__(master, cnf, **kw)

        self.bind('<Configure>', lambda e: self.config(wraplength=self.winfo_width()))


class ScreenTitle(Tkinter.Label, object):
    def __init__(self, title, master=None, cnf={}, **kw):
        super(ScreenTitle, self).__init__(master, cnf, **kw)

        self.place(relx=0.5, anchor="n", height=50, relwidth=1)
        self.configure(activebackground=DefaultStyle.bg_color)
        self.configure(text=title)


class ScrollableCanvasFrame(Tkinter.Frame, object):
    """
    This class represents a frame containing a canvas with scrollbars.
    Scrollbars are optional and must be enabled through the boolean parameters "scroll_x" and "scroll_y".
    An existing canvas can be passed through the parameter "canvas", otherwise a new canvas will be created.
    """
    def __init__(self, master=None, cnf={}, **kw):
        super(ScrollableCanvasFrame, self).__init__(master, cnf, **kw)

        self.canvas = None  # type: Tkinter.Canvas

        if 'canvas' in cnf:
            self.set_canvas(cnf['canvas'])
        else:
            self.set_canvas(Tkinter.Canvas(self))

        if 'scroll_x' in cnf and cnf['scroll_x'] is True:
            self.h_scroll = Tkinter.Scrollbar(self, orient=HORIZONTAL_ORIENTATION, command=self.canvas.xview)

            self.canvas.config(
                xscrollcommand=self.h_scroll.set,
            )

            self.h_scroll.pack(
                fill=FILL_X,
                expand=True,
                side=SIDE_BOTTOM,
            )

        if 'scroll_y' in cnf and cnf['scroll_y'] is True:
            self.v_scroll = Tkinter.Scrollbar(self, orient=VERTICAL_ORIENTATION, command=self.canvas.yview)

            self.canvas.config(
                yscrollcommand=self.v_scroll.set,
            )

            self.v_scroll.pack(
                fill=FILL_Y,
                expand=True,
                side=SIDE_RIGHT,
            )

    def set_canvas(self, canvas):
        self.canvas = canvas

        self.canvas.master = self

        self.canvas.pack(
            fill=FILL_BOTH,
            expand=True,
            anchor=ANCHOR_CENTER,
        )


class CanvasTable(object):
    default_settings = {
        'cell_height': 25,
        'cell_width': 100,
        'nbr_of_columns': 6,
        'nbr_of_rows': 6,
        'pos': (15, 15),  # type: Tuple[float, float]
    }

    def __init__(self, canvas, options=None):
        # type: (Tkinter.Canvas, Optional[Dict]) -> None

        self.canvas = canvas

        self.settings = CanvasTable.default_settings.copy()

        if options is not None:
            self.settings.update(options)

        self.height = self.settings['cell_height'] * self.settings['nbr_of_rows']

        self.width = self.settings['cell_width'] * self.settings['nbr_of_columns']

        self.canvas.create_rectangle(
            self.settings['pos'][0], self.settings['pos'][1],
            self.settings['pos'][0] + self.width, self.settings['pos'][1] + self.height
        )
