import Tkinter

import numpy as np
from typing import Dict, Tuple
from matplotlib.figure import Figure
from scipy.interpolate import interp1d
from MultiExplorer.src.GUI.Presenters import Presenter, PlotbookPresenter
from MultiExplorer.src.GUI.Widgets import CanvasTable


class NSGAPresenter(PlotbookPresenter):
    figsize = (12, 4)

    dpi = 100

    bar_height = .7

    ticks_font_size = 9

    bar_text_font_size = 9

    axis_font_size = 12

    perf_color = 'darkblue'

    density_color = 'orange'

    def get_figures(self, results):
        population_results = results['dsdse']['solutions']

        original_performance = results['performance_simulation']['performance']

        original_power_density = results['physical_simulation']['power_density']

        return {
            "Approximated Paretto Set": self.plot_population(
                population_results,
                original_performance,
                original_power_density
            )
        }

    def get_info(self, step_results, options=None):
        return (
                "NSGA-II generated a paretto frontier aproximation containing "
                + str(len(step_results['solutions']))
                + " distinct points."
        )

    def present_partials(self, frame, step_results, options=None):
        raise NotImplementedError

    @staticmethod
    def get_pd_performance_points(population_results):
        solutions = population_results.keys()

        points = []

        for key in population_results:
            solution = population_results[key]

            points.append((
                round(solution['power_density'], 2),
                round(float(solution['performance']), 2),
                solution['title']
            ))

        return points

    @staticmethod
    def plot_population(population_results, original_performance, original_power_density):
        # type: (Dict, Tuple, Tuple) -> Figure
        points = NSGAPresenter.get_pd_performance_points(population_results)

        power_density_values, performance_values, titles = zip(*points)

        nbr_of_solutions = len(titles)

        ind = np.arange(nbr_of_solutions)
        height = NSGAPresenter.bar_height

        fig = Figure(figsize=NSGAPresenter.figsize, dpi=NSGAPresenter.dpi)

        ax = fig.add_subplot(111)

        ax.set_yticks(range(0, int(nbr_of_solutions) * 2, 2))

        ax.set_yticklabels(titles, wrap=True, fontdict={'fontsize': NSGAPresenter.ticks_font_size,
                                                        'verticalalignment': 'center',
                                                        'horizontalalignment': 'right'})

        ax2 = ax.twiny()

        performance_bars = ax2.barh(ind * 2 + .5 * height, performance_values, height, align='center',
                                    color=NSGAPresenter.perf_color)

        for bar in performance_bars:
            ax2.text(
                bar.get_x() + bar.get_width(),
                bar.get_y() + bar.get_height() * .5,
                '%.2f' % round(bar.get_width(), 2),
                ha='left',
                va='center',
                fontsize=NSGAPresenter.bar_text_font_size,
                color=NSGAPresenter.perf_color
            )

        power_density_bars = ax.barh(ind * 2 - .5 * height, power_density_values,
                                     height=height, align='center', color=NSGAPresenter.density_color)

        for bar in power_density_bars:
            ax.text(
                bar.get_x() + bar.get_width(),
                bar.get_y() + bar.get_height() * .5,
                '%.2f' % round(bar.get_width(), 2),
                ha='left',
                va='center',
                fontsize=NSGAPresenter.bar_text_font_size,
                color=NSGAPresenter.density_color
            )

        ax2.set_xlabel("Performance (1/s)", fontsize=NSGAPresenter.axis_font_size)

        ax.set_xlabel("Power Density (W/mm^2)", fontsize=NSGAPresenter.axis_font_size)

        ax2.axvline(x=original_performance[0], color=NSGAPresenter.perf_color)

        ax.axvline(x=original_power_density[0], color=NSGAPresenter.density_color)

        ylim = ax2.get_ylim()

        ax2.text(
            original_performance[0],
            ylim[1] * .99,
            '%.2f' % round(original_performance[0], 2),
            ha='left',
            va='top',
            fontsize=NSGAPresenter.bar_text_font_size * 5 / 6,
            color=NSGAPresenter.perf_color
        )

        xlim = ax.get_xlim()

        ax.text(
            original_power_density[0] + .001 * xlim[1],
            ylim[0],
            '%.2f' % round(original_power_density[0], 2),
            ha='left',
            va='bottom',
            fontsize=NSGAPresenter.bar_text_font_size * 5 / 6,
            color=NSGAPresenter.density_color
        )

        fig.subplots_adjust(
            top=0.8,
            bottom=0.2,
            left=0.35,
            right=0.95
        )

        return fig

    @staticmethod
    def plot_pareto_front(population_results, original_performance, original_power_density):
        # type: (Dict, Tuple, Tuple) -> Figure
        points = NSGAPresenter.get_pd_performance_points(population_results)

        nbr_of_solutions = len(points)

        points = sorted(points, key=lambda p: p[0])

        power_density_values, performance_values, titles = zip(*points)

        fig = Figure(figsize=NSGAPresenter.figsize, dpi=NSGAPresenter.dpi)

        ax = fig.add_subplot(111)

        x, y = np.array(power_density_values), np.array(performance_values)

        ax.scatter(x, y, color=NSGAPresenter.perf_color)

        original_x = round(original_power_density[0], 2)

        original_y = round(original_performance[0], 2)

        ax.scatter([original_x], [original_y], color=NSGAPresenter.density_color)

        ax.annotate('Original', (original_x + .002, original_y))

        if nbr_of_solutions > 1:
            cubic_interploation_model = interp1d(x, y, kind="cubic")

            splined_x = np.linspace(x.min(), x.max(), 2 * nbr_of_solutions)

            splined_y = cubic_interploation_model(splined_x)

            ax.plot(splined_x, splined_y, color=NSGAPresenter.perf_color)

        ax.set_title("Aproximated Pareto Front")

        ax.set_xlabel("Power Density (W/mm^2)")

        ax.set_ylabel("Performance (1/s)")

        return fig


class SniperPresenter(Presenter):
    def __init__(self):
        super(SniperPresenter, self).__init__()

        self.table = None

        self.canvas_frame = None

    def present_results(self, frame, results, options=None):
        # todo
        return 0

    def present_partials(self, frame, step_results, options=None):
        raise NotImplementedError

    def get_info(self, step_results, options=None):
        return "Performance: " + str(step_results['performance'][0]) + " " + str(step_results['performance'][1])


class McPATPresenter(Presenter):
    def __init__(self):
        super(McPATPresenter, self).__init__()

        self.canvas = None

        self.og_table = None

        self.sol_table = None

    def present_partials(self, frame, step_results, options=None):
        raise NotImplementedError

    def present_results(self, frame, results, options=None):
        profile = results['dsdse']['profile']

        table_data = [
            ['Architecture', 'Frequency', ''],
            [
                str(profile['core_number']) + "x " + profile['model'] + " " + profile['process'],
                str(profile['frequency']) + " Ghz",
                '',
            ],
            ['Power', 'Area', 'Power Density'],
            [
                str(round(profile['power'][0], 2)) + " W",
                str(round(profile['chip_area'][0], 2)) + " mm^2",
                str(round(profile['power_density'][0], 2)) + " W/mm^2",
            ],
            ['Performance', 'DS Area (%)', ''],
            [
                str(round(profile['performance'][0], 2)) + "s^-1",
                str(round(profile['ds_area'][0], 2)) + " mm^2 (" + str(round(profile['ds_percentage'][0], 2)) + "%)",
                '',
            ],
        ]

        table_options = {
            'pos': (2, 27),
            'cells_width': [250, 250, 250],
            'font_height': 12,
            'cell_height': 25,
            'nbr_of_columns': 3,
            'nbr_of_rows': 6,
            'data': table_data,
            'center': False,
        }

        self.canvas = Tkinter.Canvas(frame)

        solutions = results['dsdse']['solutions']

        nbr_of_solutions = len(solutions)

        height = table_options['cell_height'] * (6 + nbr_of_solutions + 6)

        self.canvas.config(width=options['width'], height=height)

        self.canvas.pack(
            fill=Tkinter.BOTH,
            expand=True
        )

        self.canvas.create_text(2, 2, text="Initial Profile", anchor=Tkinter.NW)

        self.og_table = CanvasTable(self.canvas, table_options)

        self.canvas.create_text(2, table_options['cell_height'] * (6 + 3), text="NSGA-II Generated Architectures",
                                anchor=Tkinter.NW)

        table_options['pos'] = (2, table_options['cell_height'] * (6 + 4))

        table_options['cells_width'] = [445, 145, 140, 140]

        table_options['nbr_of_rows'] = nbr_of_solutions + 1

        table_options['nbr_of_columns'] = 4

        solutions_data = [
            ['Architecture', 'Performance', 'Area', 'Power Density'],
        ]

        for s in solutions:
            solutions_data.append([
                s,
                str(round(solutions[s]['performance'], 2)) + " s^-1",
                str(round(solutions[s]['total_area'], 2)) + " mm^2",
                str(round(solutions[s]['power_density'], 2)) + " W/mm^2",
            ])

        table_options['data'] = solutions_data

        self.sol_table = CanvasTable(self.canvas, table_options)

        return height

    def get_info(self, step_results, options=None):
        ds_info = "The dark silicon estimate was negligible."
        if step_results['ds_percentage'] > 0.01:
            ds_info = (
                    "Dark Silicon (area): " + str(step_results['ds_area'][0]) + " mm^2 \n"
                    + "Dark Silicon (percentage): " + str(step_results['ds_percentage'][0]) + "%"
            )

        return (
                "Power density: " + str(step_results['power_density'][0]) + " " + str(step_results['power_density'][1])
                + "\n"
                + "Area: " + str(step_results['area'][0]) + " " + str(step_results['area'][1]) + "\n"
                + ds_info
        )


class BruteForcePresenter(Presenter):
    def get_info(self, step_results, options=None):
        if 'brute_force_solutions' not in step_results:
            return ""

        return (
                "The brute force algorithm found "
                + str(len(step_results['brute_force_solutions']))
                + " viable solutions."
        )

    def __init__(self):
        super(BruteForcePresenter, self).__init__()

        self.canvas = None

        self.sol_table = None

    def present_partials(self, frame, step_results, options=None):
        raise NotImplementedError

    def present_results(self, frame, results, options=None):
        if 'brute_force_solutions' not in results['dsdse']:
            return 0

        cell_height = 25

        table_options = {
            'pos': (2, 3*(cell_height+2)),
            'cells_width': [250, 250, 250],
            'font_height': 12,
            'cell_height': cell_height,
            'nbr_of_columns': 3,
            'nbr_of_rows': 6,
            'center': False,
        }

        self.canvas = Tkinter.Canvas(frame)

        solutions = results['dsdse']['brute_force_solutions']

        nbr_of_solutions = len(solutions)

        height = table_options['cell_height'] * (6 + nbr_of_solutions + 6)

        self.canvas.config(width=options['width'], height=height)

        self.canvas.pack(
            fill=Tkinter.BOTH,
            expand=True
        )

        self.canvas.create_text(2, 2*(cell_height+2), text="Viable Solutions Found through Brute Force",
                                anchor=Tkinter.NW)

        table_options['cells_width'] = [445, 145, 140, 140]

        table_options['nbr_of_rows'] = nbr_of_solutions + 1

        table_options['nbr_of_columns'] = 4

        solutions_data = [
            ['Architecture', 'Performance', 'Area', 'Power Density'],
        ]

        for s in solutions:
            solutions_data.append([
                s,
                str(round(solutions[s]['performance'], 2)) + " s^-1",
                str(round(solutions[s]['total_area'], 2)) + " mm^2",
                str(round(solutions[s]['power_density'], 2)) + " W/mm^2",
            ])

        table_options['data'] = solutions_data

        self.sol_table = CanvasTable(self.canvas, table_options)

        return height
