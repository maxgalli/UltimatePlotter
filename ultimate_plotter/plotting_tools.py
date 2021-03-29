import logging
logger = logging.getLogger(__name__)



def plot_1d(histo, axes, histtype="step", color=None):
    logger.info("Drawing plot for variable {}".format(histo.variable.name))

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
        _h = [0, *self.sum_events, 0]
        axes.step(_edges, _h, color=edge_color, linestyle='-', linewidth=1, where='post', label=step_label)

        # Plot histogram as set of bars (if histtype == stepfilled)
        if histtype == "stepfilled":
            axes.bar(
                    histo.edges[:-1],
                    self.sum_events,
                    width=histo.widths_from_edges(histo.edges),
                    align="edge",
                    label=histo.sample.expression,
                    color=color
                    )

    # Set labels
    if histo.norm:
        axes.set_ylabel("Density")
    else:
        axes.set_ylabel("Events")

    axes.set_xlabel(histo.variable.expression, loc="center")
    axes.legend(fontsize=16)

    return axes
