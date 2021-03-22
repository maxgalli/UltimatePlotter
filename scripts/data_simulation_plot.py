#!/usr/bin/env python3
import argparse

from ultimate_plotter import DataSimulationPlot
from ultimate_plotter import setup_logging
from ultimate_plotter import universal_parser


def parse_arguments():
    parser = argparse.ArgumentParser(
            description="Plot Data vs Simulation shapes and ratio plot"
            )

    parser.add_argument(
            "--config",
            required=True,
            type=str,
            help="JSON file with the configurations for each variable"
            )

    parser.add_argument(
            "--data_file",
            required=True,
            type=str,
            help="ROOT file containing data TTree"
            )

    parser.add_argument(
            "--data_tree",
            required=True,
            type=str,
            help="Name of TTree in data_file"
            )

    parser.add_argument(
            "--sim_file",
            required=True,
            type=str,
            help="ROOT file containing simulation TTree"
            )

    parser.add_argument(
            "--sim_tree",
            required=True,
            type=str,
            help="Name of TTree in sim_file"
            )

    parser.add_argument(
            "--output_dir",
            required=True,
            type=str,
            help="Output directory"
            )

    parser.add_argument(
            "--pkl_output",
            required=False,
            type=str,
            default="output",
            help="Pickle file in which information used to make the plots are dumped"
            )

    return parser.parse_args()


def main(args):
    config = args.config
    data_file = args.data_file
    data_tree = args.data_tree
    sim_file = args.sim_file
    sim_tree = args.sim_tree
    output_dir = args.output_dir
    pkl_output = args.pkl_output

    config = universal_parser(config)

    plotter = DataSimulationPlot(data_file, data_tree, sim_file, sim_tree, **config)
    plotter.draw(output_dir)
    plotter.dump_info(output_dir, pkl_output)


if __name__ == "__main__":
    logger = setup_logging()
    args = parse_arguments()
    main(args)
