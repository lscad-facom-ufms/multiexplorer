import numpy as np
from typing import Dict, Tuple
from matplotlib.figure import Figure


class DSDSEPresenter(object):
    figsize = (12, 4)

    dpi = 100

    bar_height = .7

    ticks_font_size = 9

    bar_text_font_size = 9

    axis_font_size = 12

    perf_color = 'darkblue'

    density_color = 'orange'

    @staticmethod
    def plot_population(population_results, original_performance, original_power_density):
        # type: (Dict, Tuple, Tuple) -> Figure
        solutions = population_results.keys()

        solutions.sort()

        performance_values = []

        power_density_values = []

        nbr_of_solutions = 0

        for s in solutions:
            nbr_of_solutions += 1

            solution = population_results[s]

            performance_values.append(round(float(solution['performance']), 2))

            power_density_values.append(round(solution['power_density'], 2))

        ind = np.arange(nbr_of_solutions)
        height = DSDSEPresenter.bar_height

        fig = Figure(figsize=DSDSEPresenter.figsize, dpi=DSDSEPresenter.dpi)

        ax = fig.add_subplot(111)

        ax.set_yticks(range(0, int(nbr_of_solutions) * 2, 2))

        ax.set_yticklabels(solutions, wrap=True, fontdict={'fontsize': DSDSEPresenter.ticks_font_size,
                                                           'verticalalignment': 'center',
                                                           'horizontalalignment': 'right'})

        ax2 = ax.twiny()

        performance_bars = ax2.barh(ind * 2 + .5 * height, performance_values, height, align='center',
                                    color=DSDSEPresenter.perf_color)

        for bar in performance_bars:
            ax2.text(
                bar.get_x() + bar.get_width(),
                bar.get_y() + bar.get_height() * .5,
                '%.2f' % round(bar.get_width(), 2),
                ha='left',
                va='center',
                fontsize=DSDSEPresenter.bar_text_font_size,
                color=DSDSEPresenter.perf_color
            )

        power_density_bars = ax.barh(ind * 2 - .5 * height, power_density_values,
                                     height=height, align='center', color=DSDSEPresenter.density_color)

        for bar in power_density_bars:
            ax.text(
                bar.get_x() + bar.get_width(),
                bar.get_y() + bar.get_height() * .5,
                '%.2f' % round(bar.get_width(), 2),
                ha='left',
                va='center',
                fontsize=DSDSEPresenter.bar_text_font_size,
                color=DSDSEPresenter.density_color
            )

        ax2.set_xlabel("Performance (1/s)", fontsize=DSDSEPresenter.axis_font_size)

        ax.set_xlabel("Power Density (W/mm^2)", fontsize=DSDSEPresenter.axis_font_size)

        ax2.axvline(x=original_performance[0], color=DSDSEPresenter.perf_color)

        ax.axvline(x=original_power_density[0], color=DSDSEPresenter.density_color)

        ylim = ax2.get_ylim()

        ax2.text(
            original_performance[0],
            ylim[1]*.99,
            '%.2f' % round(original_performance[0], 2),
            ha='left',
            va='top',
            fontsize=DSDSEPresenter.bar_text_font_size * 5 / 6,
            color=DSDSEPresenter.perf_color
        )

        xlim = ax.get_xlim()

        ax.text(
            original_power_density[0]+.001*xlim[1],
            ylim[0],
            '%.2f' % round(original_power_density[0], 2),
            ha='left',
            va='bottom',
            fontsize=DSDSEPresenter.bar_text_font_size * 5 / 6,
            color=DSDSEPresenter.density_color
        )

        fig.subplots_adjust(
            top=0.8,
            bottom=0.2,
            left=0.35,
            right=0.95
        )

        return fig
