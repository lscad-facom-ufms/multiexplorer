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


class CanvasFrame(Tkinter.Frame, object):
    def __init__(self, master=None, cnf={}, **kw):
        super(CanvasFrame, self).__init__(master, cnf, **kw)

        self.canvas = Tkinter.Canvas(self)

        self.canvas.pack(
            fill=FILL_BOTH,
            expand=True,
        )


class CanvasTable(object):
    default_settings = {
        'cell_height': 25,
        'cell_width': 100,
        'nbr_of_columns': 6,
        'nbr_of_rows': 6,
        'pos': (1, 1),  # type: Tuple[float, float]
    }

    def __init__(self, canvas, options=None):
        # type: (Tkinter.Canvas, Optional[Dict]) -> None

        self.canvas = canvas

        self.table = None

        self.cells = None

        self.settings = CanvasTable.default_settings.copy()

        if options is not None:
            self.settings.update(options)

        rows = self.settings['nbr_of_rows']

        columns = self.settings['nbr_of_columns']

        cell_width = self.settings['cell_width']

        cell_height = self.settings['cell_height']

        self.height = cell_height * rows

        self.width = cell_width * columns

        self.adjust_position()

        self.draw()

    def adjust_position(self):
        canvas = self.canvas

        canvas.update_idletasks()

        canvas.update()

        cw = canvas.winfo_width()

        ch = canvas.winfo_height()

        ox = self.settings['pos'][0]

        oy = self.settings['pos'][1]

        x = ox

        y = oy

        if cw > self.width:
            x = (cw - self.width) / 2

        if ch > self.height:
            y = (ch - self.height) / 2

        self.settings['pos'] = (
            x,
            y
        )

        mx = x - ox
        my = y - oy

        if self.table is not None:
            canvas.move(self.table, mx, my)

            canvas.move('cells', mx, my)

    def draw(self):
        canvas = self.canvas

        x = self.settings['pos'][0]

        y = self.settings['pos'][1]

        self.table = canvas.create_rectangle(
            x, y,
            x + self.width, y + self.height
        )

        rows = self.settings['nbr_of_rows']

        columns = self.settings['nbr_of_columns']

        cell_width = self.settings['cell_width']

        cell_height = self.settings['cell_height']

        self.cells = []

        for r in range(0, rows):
            self.cells.append([])

            for c in range(0, columns):
                self.cells[r].append(canvas.create_rectangle(x, y, x + cell_width, y + cell_height, tags="cells"))

                x = x + cell_width

            x = self.settings['pos'][0]

            y = y + cell_height
