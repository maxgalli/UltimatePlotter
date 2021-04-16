#!/usr/bin/env python3
import argparse
import matplotlib.pyplot as plt
import mplhep as hep
import coffea.hist as hist

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

    variables_specs = config["variables"]
    samples_specs = config["samples"]
    if "selections" in config:
        selections = config["selections"]

    # Name that goes on Y axis in coffea histograms
    density = config["density"]
    if density:
        y_axis_name = "Density"
    else:
        y_axis_name = "Events"

    # Create histograms (one histogram per variable)
    histos = {}
    for vs in variables_specs:
        histo = hist.Hist(
                y_axis_name,
                hist.Cat(**config["category"]),
                hist.Bin(**vs)
                )
        histos[vs["name"]] = histo

    # Read ROOT input files as awkward arrays in batches
    # Fill histograms in the process
    for var, histo in histos.items():
        variables = [var]
        for sample in samples_specs:
            if "weight" in sample:
                variables.extend(sample["weight"])
            generator = extract_batches(sample["files"], sample["tree"], variables)
            for batch in generator:
                kwd_arg = {config["category"]["name"]: sample["name"]}
                histo.fill(**kwd_arg, **batch)

    # One plot for each variable, so we loop over the variable specs
    for var, histo in histos.items():
        logger.info("Drawing histogram for variable {}".format(var))

        # Setup figure
        bin_from_histo = histo.axis(var)
        output_name = "_".join([var, "{}bins".format(len(bin_from_histo.edges())), str(bin_from_histo._lo), str(bin_from_histo._hi)])

        fig, ax = plt.subplots()

        # Colors
        try:
            ax.set_prop_cycle(color=[ss["color"] for ss in samples_specs])
        except KeyError:
            continue

        hist.plot1d(
                hist=histo,
                ax=ax,
                clear=False,
                density=density
                )

        hep.cms.label(loc=0, data=True, llabel="Work in Progress", rlabel="", ax=ax, pad=.05)
        fig.savefig("{}/{}.pdf".format(output_dir, output_name), bbox_inches='tight')
        fig.savefig("{}/{}.png".format(output_dir, output_name), bbox_inches='tight')



if __name__ == "__main__":
    args = parse_arguments()
    main(args)
