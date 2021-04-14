#!/usr/bin/env python3
import argparse
import matplotlib.pyplot as plt
import mplhep as hep

from ultimate_plotter import Histo1D
from ultimate_plotter import Label
from ultimate_plotter import universal_parser

from ultimate_plotter.utils import setup_logging
from ultimate_plotter.utils import extract_batches
from ultimate_plotter.plotting_tools import plot_1d

hep.set_style("CMS")


def parse_arguments():
    parser = argparse.ArgumentParser(
            description="Plot variables distributions from an input file"
            )

    parser.add_argument(
            "--config",
            required=True,
            type=str,
            help="JSON file with the configurations for each variable"
            )

    parser.add_argument(
            "--output_dir",
            required=True,
            type=str,
            help="Output directory"
            )

    return parser.parse_args()



def main(args):
    # Read input data and options
    config = args.config
    output_dir = args.output_dir

    logger = setup_logging()

    config = universal_parser(config)

    variables_specs = config["variables_specs"]
    samples_specs = config["samples_specs"]
    if "selections" in config:
        selections = config["selections"]

    # Create list of names for variables and samples
    variables = [vs["name"] for vs in variables_specs]
    samples = [ss["process"] for ss in samples_specs]

    """Create histograms
    histos = {
        'var1' : {
            'sample1': Histo1D,
            'sample2': Histo1D,
            ...
        },
        ...
    }
    """
    histos = {}
    for vs in variables_specs:
        variable_label = Label(vs["name"], vs["expression"])
        binning = vs["bins"]
        rng = vs["range"]
        histos[variable_label.name] = {}

        for ss in samples_specs:
            sample_label = Label(ss["process"])
            histos[variable_label.name][sample_label.name] = Histo1D(variable=variable_label, sample=sample_label, binning=binning, range=rng)

    # Read ROOT input files as awkward arrays in batches
    for sample in samples_specs:
        generator = extract_batches(sample["files"], sample["tree"], variables)
        for batch in generator:
            for var in variables:
                histos[var][sample["process"]].fill(batch[var].to_numpy())

    # One plot for each variable, so we loop over the variable specs
    for vs in variables_specs:
        var = vs["name"]
        binning = vs["bins"]
        rng = vs["range"]

        # Setup figure
        output_name = "_".join([var, "{}bins".format(str(binning)), *map(str, rng)])
        fig, ax = plt.subplots()

        for ss in samples_specs:
            histo = histos[var][ss["process"]]
            color = ss["color"] if "color" in ss else None
            plot_1d(histo, ax, histtype=ss["histtype"], color=ss["color"])

        hep.cms.label(loc=0, data=True, llabel="Work in Progress", rlabel="", ax=ax, pad=.05)

        fig.savefig("{}/{}.pdf".format(output_dir, output_name), bbox_inches='tight')
        fig.savefig("{}/{}.png".format(output_dir, output_name), bbox_inches='tight')



if __name__ == "__main__":
    args = parse_arguments()
    main(args)
