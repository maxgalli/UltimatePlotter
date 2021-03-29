import numpy as np

import logging
logger = logging.getLogger(__name__)



class Label:
    """Container for useful labels.

    Parameters
    ----------
        name: string
            name used to find the specified quantities inside TTrees or Histo1D objects
        expression: string
            how we want 'name' to be written in a plot (e.g. Latex style)
    """
    def __init__(self, name, expression=None):
        self.name = name
        if expression:
            self.expression = expression
        else:
            self.expression = name

    def __eq__(self, other):
        return self.name == other.name and self.expression == other.expression

    def __hash__(self):
        return hash((self.name, self.expression))


class Histo1D:
    """
    Create 1-dimensional histogram np.histogram-like.

    Parameters
    ----------
        variable: Label
            variable whose values are contained in the histogram
        sample: Label
            which sample the histogram belongs to
        binning: int or list/tuple/nd.array
            if int, it's the number of bins; if array-style it's the edges
        range: list, optional
            list containing min and max (i.e., first and last edge)
        norm: bool, optional
            parameter to pass to arg density in np.histogram

    Examples
    --------
        h = ultimate_plotter.Histo1D()
    """
    def __init__(self, variable, sample, binning, range=None, norm=False):
        self.variable = variable
        self.sample = sample
        if isinstance(binning, int):
            self.edges = None
            self.nbins = binning
        elif isinstance(binning, (list, tuple, np.ndarray)):
            self.edges = binning
            self.nbins = len(self.edges) - 1
        else:
            raise ValueError("Wrong value passed for binning argument")
        self.sum_events = np.zeros(self.nbins)
        self.range = range
        self.norm = norm

    def __add__(self, other):
        if not isinstance(other, Histo1D):
            raise ValueError
        if not np.array_equal(other.nbins, self.nbins):
            raise ValueError("The histograms have inconsistent binning")
        out = myTH1(self.nbins)
        out.sum_events = self.sum_events + other.sum_events
        return out

    def __iadd__(self, other):
        if not isinstance(other, Histo1D):
            raise ValueError
        if not np.array_equal(other.nbins, self.nbins):
            raise ValueError("The histograms have inconsistent binning")
        self.sum_events += other.sum_events
        return self

    def widths_from_edges(self, edges):
        widths = []
        prev_edge = edges[0]
        for edge in edges[1:]:
            widths.append(edge - prev_edge)
            prev_edge = edge
        return np.asarray(widths)

    def fill(self, values, weights=None):
        if self.edges:
            sum_events, _ = np.histogram(values, bins=self.edges, weights=weights, density=self.norm)
        else:
            sum_events, edges = np.histogram(values, bins=self.nbins, range=self.range, weights=weights, density=self.norm)
            self.edges = edges
        self.sum_events += sum_events
