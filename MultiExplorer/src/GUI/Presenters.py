from typing import Optional, Dict
from Tkinter import Frame, Scrollbar
from ttk import Notebook
from Tkconstants import HORIZONTAL as HORIZONTAL_ORIENTATION, X as FILL_X, BOTTOM as SIDE_BOTTOM, TOP as SIDE_TOP
from matplotlib.figure import Figure as MatplotFigure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Presenter(object):
    def __init__(self):
        self.results = None  # type: Optional[Dict]

        self.frame = None  # type: Optional[Frame]

    def present_partials(self, frame, step_results, options=None):
        # type: (Frame, Dict, Optional[Dict]) -> int
        raise NotImplementedError

    def present_results(self, frame, results, options=None):
        # type: (Frame, Dict, Optional[Dict]) -> int
        raise NotImplementedError

    def get_info(self, step_results, options=None):
        # type: (Dict, Optional[Dict]) -> string
        raise NotImplementedError


class PlotbookPresenter(Presenter):
    FRAME_HEIGHT = 400
    PLOTBOOK_HEIGHT = 420

    def __init__(self):
        super(PlotbookPresenter, self).__init__()

        self.width = None

        self.notebook = None

        self.plots = None

    def get_info(self, results, options=None):
        raise NotImplementedError

    def create_plotbook(self, frame, options):
        self.notebook = Notebook(frame)

        if options and 'width' in options:
            self.width = options['width']
        else:
            self.width = 908

        self.notebook.config(height=PlotbookPresenter.PLOTBOOK_HEIGHT, width=self.width)

        self.notebook.pack(
            fill=FILL_X,
            expand=True,
            side=SIDE_TOP,
        )

        self.plots = {}

    def present_partials(self, frame, step_results, options=None):
        raise NotImplementedError

    """
        From the results, generate the matplot figures.
        This method should be implemented according to each step implementation.
        Should return a dict where each element is a MatplotFigure. The keys are the figures' titles.
    """
    def get_figures(self, results):
        # type: (Dict) -> Dict[str, MatplotFigure]
        raise NotImplementedError

    def add_plot(self, title, figure):
        # type: (str, MatplotFigure) -> None

        frame = Frame(self.notebook, height=PlotbookPresenter.FRAME_HEIGHT, width=self.width)

        figure = FigureCanvasTkAgg(figure, frame)

        xscroll = Scrollbar(frame, orient=HORIZONTAL_ORIENTATION)

        plot = {
            'frame': frame,
            'figure': figure,
            'xscroll': xscroll,
        }

        figure_tk = figure.get_tk_widget()

        height = figure.get_width_height()[1]

        width = figure.get_width_height()[0]

        figure_tk.config(
            height=height,
            width=width,
            xscrollcommand=xscroll.set,
            scrollregion=(0, 0, height, width)
        )

        xscroll.config(
            command=figure_tk.xview
        )

        figure_tk.pack(side=SIDE_TOP)

        xscroll.pack(expand=True, fill=FILL_X, side=SIDE_BOTTOM)

        figure.draw()

        self.plots[title] = plot

        self.notebook.add(frame, text=title)

    def present_results(self, frame, results, options=None):
        figures = self.get_figures(results)

        if not figures:
            # nothing to present
            return

        self.create_plotbook(frame, options)

        for title in figures:
            self.add_plot(title, figures[title])

        return PlotbookPresenter.PLOTBOOK_HEIGHT + 20
