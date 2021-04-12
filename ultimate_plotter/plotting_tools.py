from .histo import Histo1D

import logging
logger = logging.getLogger(__name__)



def plot_1d(histo, axes, histtype="step", color=None, bottom_histo=None):
    logger.info("Drawing plot for variable {}, sample {}".format(histo.variable.name, histo.sample.name))

    # Create empty bottom_histogram for stacked plots
    if not bottom_histo:
        bottom_histo = Histo1D(variable=histo.variable, sample=histo.sample, binning=histo.nbins, range=histo.range)

    histtypes = ["stepfilled", "step", "datalike"]
    if histtype not in histtypes:
        raise ValueError("Option histtype must be in {}".format(histtypes))

    if histtype == "datalike":
        _centres = (histo.edges[:-1] + histo.edges[1:]) / 2
        axes.plot(_centres, histo.sum_events, "k.", label=histo.sample.expression)

    else:
        # When dealing with bars, the only way to draw a proper edge is with plt.step
        edge_color = color
        step_label = histo.sample.expression
        if histtype == "stepfilled":
            step_label = None
            edge_color = "black"

        _edges = [histo.edges[0], *histo.edges]
        sum_events = histo.sum_events + bottom_histo.sum_events
        _h = [0, *sum_events, 0]
        axes.step(_edges, _h, color=edge_color, linestyle='-', linewidth=1, where='post', label=step_label)

        # Plot histogram as set of bars (if histtype == stepfilled)
        if histtype == "stepfilled":
            axes.bar(
                    histo.edges[:-1],
                    histo.sum_events,
                    width=histo.widths_from_edges(histo.edges),
                    align="edge",
                    label=histo.sample.expression,
                    color=color,
                    bottom=bottom_histo.sum_events
                    )

    # Set labels
    if histo.norm:
        axes.set_ylabel("Density", loc="center")
    else:
        axes.set_ylabel("Events", loc="center")

    axes.set_xlabel(histo.variable.expression, loc="center")
    axes.legend(fontsize=16)

    return axes
