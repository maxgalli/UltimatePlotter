#!/usr/bin/env python3
import argparse
import matplotlib.pyplot as plt
import mplhep as hep

from ultimate_plotter import Histo1D
from ultimate_plotter import Label
from ultimate_plotter import universal_parser

from ultimate_plotter.utils import setup_logging
from ultimate_plotter.utils import extract
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

    # Read ROOT input files as awkward arrays
    variables = [vs["name"] for vs in variables_specs]
    for sample in samples_specs:
        sample["events"] = extract(sample["file"], sample["tree"], variables)

    # Divide sample specs into data and simulation
    data_specs = [ss for ss in samples_specs if ss["type"] == "data"]
    sim_specs = [ss for ss in samples_specs if ss["type"] == "simulation"]

    for vs in variables_specs:
        variable_label = Label(vs["name"], vs["expression"])
        binning = vs["bins"]
        rng = vs["range"]

        # Setup figure
        output_name = "_".join([variable_label.name, "{}bins".format(str(binning)), *map(str, rng)])

        fig, ax = plt.subplots()

        prev_histo = Histo1D(variable=variable_label, sample=Label("placeholder"), binning=binning, range=rng)
        for ss in sim_specs:
            sample_label = Label(ss["process"])

            histo = Histo1D(variable=variable_label, sample=sample_label, binning=binning, range=rng)
            histo.fill(ss["events"][variable_label.name].to_numpy())

            color = ss["color"] if "color" in ss else None
            plot_1d(histo, ax, histtype=ss["histtype"], color=color, bottom_histo=prev_histo)
            prev_histo += histo

        for ss in data_specs:
            sample_label = Label(ss["process"])

            histo = Histo1D(variable=variable_label, sample=sample_label, binning=binning, range=rng)
            histo.fill(ss["events"][variable_label.name].to_numpy())

            color = ss["color"] if "color" in ss else None
            plot_1d(histo, ax, histtype=ss["histtype"], color=color)

        hep.cms.label(loc=0, data=True, llabel="Work in Progress", rlabel="", ax=ax, pad=.001)

        fig.savefig("{}/{}.pdf".format(output_dir, output_name), bbox_inches='tight')
        fig.savefig("{}/{}.png".format(output_dir, output_name), bbox_inches='tight')



if __name__ == "__main__":
    args = parse_arguments()
    main(args)
